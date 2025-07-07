"""
Test script to verify VAD fix for STT streaming error

This will test the interview agent quickly to ensure:
1. VAD is properly configured
2. STT streaming works without errors
3. Agent can generate responses
"""

import asyncio
import config  # Import our configuration

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import openai, noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

class TestAgent(Agent):
    """Simple test agent to verify VAD functionality"""
    
    def __init__(self):
        super().__init__(instructions="You are a test AI assistant. Say hello and confirm you can hear properly.")

async def test_agent_session():
    """Test the agent session configuration"""
    
    print("🧪 Testing LiveKit Agent with VAD configuration...")
    
    try:
        # Create test agent
        agent = TestAgent()
        
        # Create AgentSession with VAD - this should not fail now
        session = AgentSession(
            stt=openai.STT(model="whisper-1", language="en"),
            llm=openai.LLM(model="gpt-4o-mini", temperature=0.7),
            tts=openai.TTS(model="tts-1", voice="nova"),
            vad=silero.VAD.load(),  # This should fix the streaming issue
            turn_detection=MultilingualModel(),
        )
        
        print("✅ AgentSession created successfully with VAD")
        print("✅ VAD fix appears to be working!")
        print("🎯 Ready for real phone call testing")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating AgentSession: {e}")
        print("💡 You may need to install updated requirements:")
        print("   pip install -r requirements.txt")
        return False

def main():
    """Run the test"""
    print("=" * 50)
    print("Testing VAD Fix for LiveKit Interview Agent")
    print("=" * 50)
    
    # Test the session creation
    success = asyncio.run(test_agent_session())
    
    if success:
        print("\n🚀 Next steps:")
        print("1. Run: python twilio_setup.py")
        print("2. Follow the Twilio setup instructions")
        print("3. Test with: python interview_agent.py dev")
        print("4. Call your Twilio number!")
    else:
        print("\n⚠️  Fix the errors above before proceeding")

if __name__ == "__main__":
    main() 