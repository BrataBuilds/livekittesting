"""
Quick test to verify config loading is working properly
"""

import config

def main():
    print("🧪 Testing Environment Variable Loading")
    print("=" * 50)
    
    # Test config loading
    print(f"📁 Loading from: {config.vapi_env_path}")
    print(f"📁 File exists: {config.vapi_env_path.exists()}")
    
    print("\n🔧 Environment Variables:")
    print(f"  LIVEKIT_URL: {config.LIVEKIT_URL[:30]}..." if config.LIVEKIT_URL else "  LIVEKIT_URL: ❌ None")
    print(f"  LIVEKIT_API_KEY: {config.LIVEKIT_API_KEY[:10]}..." if config.LIVEKIT_API_KEY else "  LIVEKIT_API_KEY: ❌ None")
    print(f"  OPENAI_API_KEY: {config.OPENAI_API_KEY[:10]}..." if config.OPENAI_API_KEY else "  OPENAI_API_KEY: ❌ None")
    print(f"  TWILIO_PHONE_NUMBER: {config.TWILIO_PHONE_NUMBER}" if config.TWILIO_PHONE_NUMBER else "  TWILIO_PHONE_NUMBER: ❌ None")
    print(f"  TWILIO_ACCOUNT_SID: {config.TWILIO_ACCOUNT_SID[:10]}..." if config.TWILIO_ACCOUNT_SID else "  TWILIO_ACCOUNT_SID: ❌ None")
    
    print("\n📋 Verification Results:")
    livekit_ok = config.verify_env_vars()
    twilio_ok = config.verify_twilio_vars()
    
    if livekit_ok and twilio_ok:
        print("\n🎉 Configuration test PASSED!")
        print("✅ Ready to proceed with Twilio setup")
        return True
    else:
        print("\n❌ Configuration test FAILED!")
        print("Fix the missing environment variables in ../vapi.env")
        return False

if __name__ == "__main__":
    main() 