"""
LiveKit Outbound Call Testing Script

This script sets up outbound calling capability and creates test scripts
to make outbound calls to specified phone numbers using the interview agent.

Prerequisites:
- LiveKit CLI installed (pip install livekit-cli)
- Twilio outbound trunk configured
- Environment variables set in ../vapi.env
"""

import json
import os
import subprocess
import sys
import config  # Import our config module

def create_outbound_trunk_config():
    """Create outbound trunk configuration for making calls"""
    
    # Get Twilio configuration
    phone_number = config.TWILIO_PHONE_NUMBER
    account_sid = config.TWILIO_ACCOUNT_SID
    auth_token = config.TWILIO_AUTH_TOKEN
    
    if not all([phone_number, account_sid, auth_token]):
        print("❌ Error: Missing Twilio configuration")
        print("Please ensure TWILIO_PHONE_NUMBER, TWILIO_ACCOUNT_SID, and TWILIO_AUTH_TOKEN are set in ../vapi.env")
        return None
    
    # Twilio SIP domain for outbound calls
    # Format: <account_sid>.pstn.twilio.com
    twilio_sip_domain = f"{account_sid}.pstn.twilio.com"
    
    outbound_config = {
        "trunk": {
            "name": f"Interview Agent Outbound Trunk - {phone_number}",
            "address": twilio_sip_domain,
            "numbers": [phone_number],
            "auth_username": account_sid,
            "auth_password": auth_token
        }
    }
    
    # Save configuration to file
    with open('outbound-trunk.json', 'w') as f:
        json.dump(outbound_config, f, indent=2)
    
    print(f"✅ Created outbound trunk configuration")
    print(f"   📞 Phone: {phone_number}")
    print(f"   🌐 SIP Domain: {twilio_sip_domain}")
    return outbound_config

def check_livekit_cli():
    """Check if LiveKit CLI is installed and accessible"""
    try:
        result = subprocess.run(['lk', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ LiveKit CLI found: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ LiveKit CLI not found")
    print("📦 Install with: pip install livekit-cli")
    print("🔧 Or download from: https://github.com/livekit/livekit-cli/releases")
    return False

def create_outbound_call_script(target_phone):
    """Create scripts to make outbound calls"""
    
    # Environment setup for CLI
    env_setup = f"""
# Set LiveKit environment variables
export LIVEKIT_URL="{config.LIVEKIT_URL}"
export LIVEKIT_API_KEY="{config.LIVEKIT_API_KEY}"
export LIVEKIT_API_SECRET="{config.LIVEKIT_API_SECRET}"
"""
    
    # Commands to run
    setup_commands = f"""
echo "🚀 Setting up outbound calling..."

# 1. Create outbound trunk (only needed once)
echo "📞 Creating outbound trunk..."
lk sip outbound create outbound-trunk.json

# 2. Get trunk ID for dispatch (you'll need this)
echo "📋 Getting trunk ID..."
lk sip outbound list

echo "✅ Setup complete! Now you can make test calls."
"""
    
    # Test call command
    call_commands = f"""
echo "📞 Making test call to {target_phone}..."

# Create dispatch with agent and target phone in metadata
lk dispatch create \\
  --new-room \\
  --agent-name interview-agent \\
  --metadata '{target_phone}'

echo "📱 Call should be ringing {target_phone} now!"
echo "🎙️ Make sure your interview agent is running: python interview_agent.py dev"
"""
    
    # Create Linux/Mac script
    linux_script = f"""#!/bin/bash
{env_setup}
{setup_commands}

# Uncomment below to make a test call (after setup is complete)
# {call_commands}
"""
    
    # Create Windows script
    windows_script = f"""@echo off
REM Set LiveKit environment variables
set LIVEKIT_URL={config.LIVEKIT_URL}
set LIVEKIT_API_KEY={config.LIVEKIT_API_KEY}
set LIVEKIT_API_SECRET={config.LIVEKIT_API_SECRET}

echo 🚀 Setting up outbound calling...

REM 1. Create outbound trunk (only needed once)
echo 📞 Creating outbound trunk...
lk sip outbound create outbound-trunk.json

REM 2. Get trunk ID for dispatch
echo 📋 Getting trunk ID...
lk sip outbound list

echo ✅ Setup complete! Now you can make test calls.

REM Uncomment below to make a test call (after setup is complete)
REM echo 📞 Making test call to {target_phone}...
REM lk dispatch create --new-room --agent-name interview-agent --metadata "{target_phone}"
"""
    
    # Save scripts
    with open('test_interview_call.sh', 'w', encoding='utf-8') as f:
        f.write(linux_script)
    
    with open('test_interview_call.bat', 'w', encoding='utf-8') as f:
        f.write(windows_script)
    
    # Make shell script executable on Unix systems
    try:
        os.chmod('test_interview_call.sh', 0o755)
    except:
        pass  # Windows doesn't support chmod
    
    print(f"✅ Created call test scripts for {target_phone}")
    print("   📄 test_interview_call.sh (Linux/Mac)")
    print("   📄 test_interview_call.bat (Windows)")

def create_manual_call_instructions(target_phone):
    """Create manual instructions for making outbound calls"""
    
    instructions = f"""
📞 OUTBOUND CALL TESTING INSTRUCTIONS

Target Phone: {target_phone}

1. SETUP (One-time only):
   
   a) Set environment variables:
      export LIVEKIT_URL="{config.LIVEKIT_URL}"
      export LIVEKIT_API_KEY="{config.LIVEKIT_API_KEY}"
      export LIVEKIT_API_SECRET="{config.LIVEKIT_API_SECRET}"
   
   b) Create outbound trunk:
      lk sip outbound create outbound-trunk.json
   
   c) Verify trunk creation:
      lk sip outbound list
      (Note down the trunk ID for reference)

2. START YOUR AGENT:
   python interview_agent.py dev
   
   (Keep this running in a separate terminal)

3. MAKE TEST CALL:
   lk dispatch create \\
     --new-room \\
     --agent-name interview-agent \\
     --metadata '{target_phone}'

4. EXPECTED BEHAVIOR:
   - Your phone ({target_phone}) should ring within 10-30 seconds
   - Answer the call to speak with the AI interview agent
   - The agent should greet you and start an interview
   - Test the conversation flow and voice quality

5. TROUBLESHOOTING:
   - Ensure agent is running with correct agent_name="interview-agent"
   - Check LiveKit dashboard for active rooms and participants
   - Verify Twilio account has outbound calling enabled
   - Check trunk status: lk sip outbound list

6. MONITORING:
   - LiveKit Dashboard: Check for active rooms and SIP participants
   - Twilio Console: Monitor call logs and billing
   - Agent Logs: Check terminal output for errors

💡 TIP: Run 'lk sip outbound list' to see your trunk ID and status
💡 TIP: Use 'lk room list' to see active rooms during calls
"""

    with open('OUTBOUND_CALL_GUIDE.txt', 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print("✅ Created detailed outbound call guide")
    print("   📖 OUTBOUND_CALL_GUIDE.txt")

def main():
    """Main function to set up outbound calling"""
    target_phone = "+919073554610"  # Your phone number
    
    print("🚀 Setting up LiveKit Outbound Call Testing")
    print("="*60)
    print(f"🎯 Target phone: {target_phone}")
    
    # Verify environment
    if not config.verify_env_vars():
        print("\n❌ Please fix LiveKit environment variables first")
        return False
    
    if not config.verify_twilio_vars():
        print("\n❌ Please fix Twilio environment variables first")
        return False
    
    # Check LiveKit CLI
    if not check_livekit_cli():
        print("\n❌ Please install LiveKit CLI first")
        return False
    
    print(f"\n✅ Using Twilio phone: {config.TWILIO_PHONE_NUMBER}")
    print(f"✅ Calling target: {target_phone}")
    
    # Create configurations and scripts
    outbound_config = create_outbound_trunk_config()
    if outbound_config:
        create_outbound_call_script(target_phone)
        create_manual_call_instructions(target_phone)
    
    print("\n" + "="*60)
    print("🎯 NEXT STEPS:")
    print("1. Run setup script:")
    print("   Linux/Mac: ./test_interview_call.sh")
    print("   Windows: test_interview_call.bat")
    print("")
    print("2. Start your agent:")
    print("   python interview_agent.py dev")
    print("")
    print("3. Make test call manually:")
    print(f"   lk dispatch create --new-room --agent-name interview-agent --metadata '{target_phone}'")
    print("")
    print("4. Check OUTBOUND_CALL_GUIDE.txt for detailed instructions")
    print("")
    print("📱 Your phone should ring within 10-30 seconds!")
    
    return True

if __name__ == "__main__":
    main() 