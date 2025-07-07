"""
Twilio Integration Setup for LiveKit Interview Agent

This script sets up:
1. LiveKit inbound trunk for receiving calls
2. Dispatch rules to route calls to interview agent
3. Instructions for TwiML bin configuration

Prerequisites:
- Twilio account with phone number
- LiveKit project configured
- Environment variables set in ../vapi.env:
  - TWILIO_ACCOUNT_SID
  - TWILIO_AUTH_TOKEN 
  - TWILIO_PHONE_NUMBER
  - LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET
"""

import json
import os
import config  # Import our fixed config

def create_inbound_trunk_config():
    """Create the inbound trunk configuration for LiveKit"""
    
    # Get phone number from config
    phone_number = config.TWILIO_PHONE_NUMBER
    if not phone_number:
        print("❌ Error: TWILIO_PHONE_NUMBER not found in environment")
        print("Please add your Twilio phone number to ../vapi.env")
        return None
        
    # Generate username/password for SIP authentication
    # These will be used in both LiveKit trunk and TwiML bin
    sip_username = "interview_trunk_user"
    sip_password = "secure_trunk_pass_2025"  # Use a secure password
    
    trunk_config = {
        "trunk": {
            "name": f"Interview Agent Inbound Trunk - {phone_number}",
            "auth_username": sip_username,
            "auth_password": sip_password,
            "numbers": [phone_number]
        }
    }
    
    # Save configuration to file
    with open('inbound-trunk.json', 'w') as f:
        json.dump(trunk_config, f, indent=2)
    
    print(f"✅ Created inbound trunk configuration for {phone_number}")
    return trunk_config

def create_dispatch_rule_config():
    """Create dispatch rule to route calls to interview agent"""
    
    dispatch_config = {
        "rule": {
            "dispatchRuleAgentDispatch": {
                "agentName": "interview-agent",  # Matches agent_name in interview_agent.py
                "roomPrefix": "interview"  # Rooms will be named interview-xxx
            }
        }
    }
    
    # Save configuration to file
    with open('dispatch-rule.json', 'w') as f:
        json.dump(dispatch_config, f, indent=2)
    
    print("✅ Created dispatch rule for interview agent")
    return dispatch_config

def create_twiml_bin_instructions(trunk_config):
    """Generate TwiML bin content and setup instructions"""
    
    if not trunk_config:
        return
        
    # Extract SIP credentials
    username = trunk_config["trunk"]["auth_username"]
    password = trunk_config["trunk"]["auth_password"]
    phone_number = trunk_config["trunk"]["numbers"][0]
    
    # Get LiveKit SIP host from URL
    livekit_url = config.LIVEKIT_URL or ''
    if livekit_url.startswith('wss://'):
        sip_host = livekit_url.replace('wss://', '').replace('ws://', '')
    else:
        sip_host = livekit_url
    
    # Generate TwiML content
    twiml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Dial>
    <Sip username="{username}" password="{password}">
      sip:{phone_number}@{sip_host}
    </Sip>
  </Dial>
</Response>'''
    
    # Save TwiML to file (UTF-8 encoding for Windows compatibility)
    with open('twiml-bin-content.xml', 'w', encoding='utf-8') as f:
        f.write(twiml_content)
    
    print("✅ Created TwiML bin content")
    
    # Generate setup instructions
    instructions = f"""
📞 TWILIO SETUP INSTRUCTIONS

1. Create LiveKit Inbound Trunk:
   lk sip inbound create inbound-trunk.json

2. Create Dispatch Rule:
   lk sip dispatch create dispatch-rule.json

3. Setup TwiML Bin in Twilio Console:
   - Go to https://console.twilio.com/us1/develop/runtime/twiml-bins
   - Create new TwiML Bin named "LiveKit Interview Agent"
   - Copy content from twiml-bin-content.xml
   
4. Configure Phone Number:
   - Go to https://console.twilio.com/us1/develop/phone-numbers/manage/incoming
   - Select your phone number: {phone_number}
   - In "Voice Configuration" section:
     - A call comes in: TwiML Bin
     - Select: LiveKit Interview Agent
   - Save configuration

5. Test Setup:
   - Start your interview agent: python interview_agent.py dev
   - Call your Twilio number: {phone_number}
   - You should be connected to the AI interviewer!

SIP Credentials:
- Username: {username}
- Password: {password}
- Phone: {phone_number}
- SIP Host: {sip_host}

💡 Troubleshooting:
- Ensure your LiveKit agent is running with agent_name="interview-agent"
- Check LiveKit dashboard for incoming SIP calls
- Verify TwiML bin credentials match inbound trunk
"""
    
    # Save instructions to file (UTF-8 encoding for Windows compatibility)
    with open('TWILIO_SETUP_GUIDE.txt', 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print("✅ Created setup instructions in TWILIO_SETUP_GUIDE.txt")
    print("\n" + "="*60)
    print(instructions)

def main():
    """Main setup function"""
    print("🚀 Setting up Twilio integration for LiveKit Interview Agent")
    print("="*60)
    
    # Verify environment variables using our config module
    if not config.verify_env_vars():
        print("Please fix missing LiveKit environment variables first")
        return
    
    if not config.verify_twilio_vars():
        print("Please fix missing Twilio environment variables first") 
        return
    
    print(f"✅ Using phone number: {config.TWILIO_PHONE_NUMBER}")
    print(f"✅ Using LiveKit URL: {config.LIVEKIT_URL}")
    
    # Create configuration files
    trunk_config = create_inbound_trunk_config()
    create_dispatch_rule_config()
    create_twiml_bin_instructions(trunk_config)
    
    print("\n🎯 Next Steps:")
    print("1. Install updated requirements: pip install -r requirements.txt")
    print("2. Follow instructions in TWILIO_SETUP_GUIDE.txt")
    print("3. Start agent: python interview_agent.py dev")
    print("4. Call your Twilio number to test!")

if __name__ == "__main__":
    main() 