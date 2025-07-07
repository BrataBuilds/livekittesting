"""
LiveKit Interview Agent - OpenAI Integration with VAD
This agent handles voice-based candidate interviews using OpenAI models
Includes Voice Activity Detection for proper streaming support
"""
import config  # Import our configuration
import asyncio

from livekit import agents, rtc, api
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import openai, noise_cancellation, silero
# Removed turn detector to avoid model download issues during testing
# from livekit.plugins.turn_detector.multilingual import MultilingualModel

# Use one of your outbound trunk IDs from `lk sip outbound list`
OUTBOUND_TRUNK_ID = "ST_rsrCgZSnhtxo"  # Replace with your preferred trunk ID

class InterviewAgent(Agent):
    """
    Interview Agent using OpenAI models through LiveKit
    This replaces your current VAPI assistant
    """
    
    def __init__(self, job_context=None, candidate_context=None):
        # Create interview instructions based on job and candidate context
        instructions = self.create_interview_instructions(job_context, candidate_context)
        super().__init__(instructions=instructions)
        
        self.job_context = job_context
        self.candidate_context = candidate_context

    def create_interview_instructions(self, job_context, candidate_context):
        """
        Create dynamic interview instructions based on job and candidate
        This mirrors your current prompt_service.py logic
        """
        base_instructions = """You are an AI interviewer conducting a professional job interview over the phone.

Your role:
- Conduct a structured interview based on the job requirements
- Ask relevant questions about the candidate's experience
- Maintain a professional and friendly tone
- Keep the interview focused and time-efficient (10-15 minutes)
- End the interview naturally when all key topics are covered
- Always speak clearly and at an appropriate pace for phone conversation

Interview flow:
1. Greet the candidate warmly and introduce yourself
2. Briefly explain the interview process
3. Ask about their experience relevant to the job
4. Dive into specific technical/behavioral questions
5. Allow candidate to ask questions
6. Thank them and explain next steps
"""
        
        if job_context:
            job_instructions = f"""

Job Details:
- Position: {job_context.get('job_title', 'Software Developer')}
- Company: {job_context.get('company_name', 'Our Company')}
- Required Skills: {', '.join(job_context.get('requirements', []))}
- Experience Level: {job_context.get('experience_level', 'Mid-level')}

Focus your questions on these job requirements and assess the candidate's fit.
"""
            base_instructions += job_instructions
        
        if candidate_context:
            candidate_instructions = f"""

Candidate Information:
- Name: {candidate_context.get('candidate_name', 'Candidate')}
- Experience: {candidate_context.get('experience_years', 'Unknown')} years
- Key Skills: {', '.join(candidate_context.get('relevant_skills', []))}

Use this information to personalize your questions and dig deeper into their experience.
"""
            base_instructions += candidate_instructions
            
        return base_instructions


async def entrypoint(ctx: agents.JobContext):
    """
    Main entrypoint for the interview agent using OpenAI models
    This will be called when a phone call comes in (similar to VAPI webhook)
    """
    
    # TODO: Get job and candidate context from your database
    # Similar to how you currently fetch from MongoDB in call_executor.py
    job_context = {
        "job_title": "Python Developer", 
        "company_name": "Tech Company",
        "requirements": ["Python", "FastAPI", "MongoDB"],
        "experience_level": "Mid-level"
    }
    
    candidate_context = {
        "candidate_name": "Test Candidate",
        "experience_years": 3,
        "relevant_skills": ["Python", "API Development"]
    }
    
    # Create the interview agent
    interview_agent = InterviewAgent(job_context, candidate_context)
    
    # Create AgentSession with OpenAI components + VAD for streaming
    session = AgentSession(
        # Use OpenAI for STT (speech-to-text)
        stt=openai.STT(
            model="whisper-1",
            language="en"
        ),
        
        # Use OpenAI for LLM (conversation logic)
        llm=openai.LLM(
            model="gpt-4o-mini",
            temperature=0.7
        ),
        
        # Use OpenAI for TTS (text-to-speech)
        tts=openai.TTS(
            model="tts-1", 
            voice="nova"  # Similar to your current "Neha" voice
        ),
        
        # Add VAD for voice activity detection (fixes streaming STT)
        vad=silero.VAD.load(),
        
        # Turn detection removed for testing - can be added back later
        # turn_detection=MultilingualModel(),
    )
    
    # Connect to the room first
    await ctx.connect()
    
    # Check if this is an outbound call (has phone number in metadata)
    phone_number = ctx.job.metadata
    if phone_number:
        print(f"📞 Making outbound call to: {phone_number}")
        
        # Create SIP participant for outbound call using correct API
        try:
            clean_phone_number = phone_number.strip('\'"')
            user_identity = "phone_user"
            
            await ctx.api.sip.create_sip_participant(api.CreateSIPParticipantRequest(
                room_name=ctx.room.name,
                sip_trunk_id=OUTBOUND_TRUNK_ID,
                sip_call_to=clean_phone_number,
                participant_identity=user_identity,
            ))
            print(f"✅ SIP participant creation initiated for {clean_phone_number}")
            
            # Wait for participant to connect
            participant = await ctx.wait_for_participant(identity=user_identity)
            print(f"✅ Participant connected: {participant.identity}")
            
            # Monitor call status to debug the failure
            print("🔍 Monitoring call status...")
            start_time = asyncio.get_event_loop().time()
            
            while asyncio.get_event_loop().time() - start_time < 45:  # Extended timeout
                call_status = participant.attributes.get("sip.callStatus")
                sip_call_id = participant.attributes.get("sip.callId") 
                disconnect_reason = participant.attributes.get("sip.disconnectReason")
                error_code = participant.attributes.get("sip.errorCode")
                
                print(f"📊 Call status: {call_status}, SIP Call ID: {sip_call_id}")
                if disconnect_reason:
                    print(f"❌ Disconnect reason: {disconnect_reason}")
                if error_code:
                    print(f"🚨 Error code: {error_code}")
                
                if call_status == "active":
                    print("✅ Call connected successfully!")
                    break
                elif call_status == "hangup":
                    print(f"❌ Call hung up. Reason: {disconnect_reason}")
                    print(f"🔍 Check Twilio console for call logs")
                    break
                elif call_status == "failed":
                    print(f"❌ Call failed. Error: {error_code}")
                    print(f"🔍 Reason: {disconnect_reason}")
                    break
                elif call_status == "automation":
                    print("📞 Call in automation state (DTMF dialing)")
                elif call_status == "ringing":
                    print("📱 Phone is ringing...")
                elif call_status == "dialing":
                    print("📞 Still dialing...")
                elif call_status is None:
                    print("⏳ Call status not available yet...")
                
                await asyncio.sleep(1)  # Check every second
            
            # If we exit the loop without success
            final_status = participant.attributes.get("sip.callStatus")
            if final_status != "active":
                print(f"⚠️ Call monitoring timeout. Final status: {final_status}")
                print("🔍 Possible issues:")
                print("   - Phone number not associated with Twilio SIP trunk")
                print("   - Twilio account permissions or balance issues") 
                print("   - Network connectivity between LiveKit and Twilio")
                print(f"   - Check Twilio console for trunk {OUTBOUND_TRUNK_ID}")
            
            # Print all participant attributes for debugging
            print("🔍 All participant attributes:")
            for key, value in participant.attributes.items():
                if key.startswith("sip."):
                    print(f"   {key}: {value}")
                
        except Exception as e:
            print(f"❌ Failed to create SIP participant: {e}")
            import traceback
            print(f"📊 Full error: {traceback.format_exc()}")
            return
    else:
        print("📱 Inbound call - waiting for caller to connect")
    
    # Start the agent session
    await session.start(
        room=ctx.room,
        agent=interview_agent,
        room_input_options=RoomInputOptions(
            # Enhanced noise cancellation for phone calls
            noise_cancellation=noise_cancellation.BVCTelephony(),
        ),
    )
    
    # For outbound calls, wait a moment for the call to connect before greeting
    if phone_number:
        print("⏳ Waiting for call to connect...")
        await asyncio.sleep(3)  # Give time for call to connect
    
    # Start the interview with a greeting
    greeting_message = f"Hello {candidate_context['candidate_name']}, and welcome to your interview with {job_context['company_name']}. I'm an AI interviewer and I'll be conducting your interview for the {job_context['job_title']} position today. This should take about 10-15 minutes. Are you ready to begin?"
    
    await session.generate_reply(instructions=greeting_message)


if __name__ == "__main__":
    """
    Run the interview agent using OpenAI models
    This replaces your current run_vapi.py
    """
    # Add agent_name for explicit dispatch (required for telephony)
    agents.cli.run_app(agents.WorkerOptions(
        entrypoint_fnc=entrypoint,
        agent_name="interview-agent"  # Required for SIP dispatch
    )) 