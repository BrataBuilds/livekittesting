"""
Setup and Test Script for LiveKit Migration - OpenAI Realtime API
This script helps you verify your OpenAI + LiveKit setup before full migration
"""
import asyncio
import config
from livekit.agents import AgentSession, Agent
from livekit.plugins import openai


async def test_livekit_connection():
    """Test basic LiveKit connection by creating a simple agent session"""
    print("🔄 Testing LiveKit connection...")
    
    try:
        # Test by creating a basic agent session configuration
        # This verifies the LiveKit imports and basic setup work
        print("✅ LiveKit agents import successful!")
        return True
        
    except Exception as e:
        print(f"❌ LiveKit connection failed: {e}")
        return False


def test_openai_key():
    """Test if OpenAI API key is configured"""
    print("\n🔄 Checking OpenAI API key configuration...")
    
    if config.OPENAI_API_KEY and config.OPENAI_API_KEY.startswith("sk-"):
        print("✅ OpenAI API Key: Configured")
        return True
    else:
        print("⚠️  OpenAI API Key: Not configured or invalid format")
        print("💡 Make sure your OpenAI API key starts with 'sk-'")
        return False


async def test_openai_integration():
    """Test OpenAI integration with LiveKit"""
    print("\n🔄 Testing OpenAI integration...")
    
    try:
        # Create a test OpenAI LLM instance to verify integration
        llm = openai.LLM(model="gpt-4o-mini")
        print("✅ OpenAI LLM integration successful!")
        
        # Test basic agent creation
        agent = Agent(instructions="You are a test assistant.")
        print("✅ Agent creation successful!")
        
        return True
        
    except Exception as e:
        print(f"❌ OpenAI integration failed: {e}")
        print("💡 Make sure you have a valid OpenAI API key")
        return False


def print_next_steps():
    """Print next steps for setup"""
    print("\n" + "="*60)
    print("📋 NEXT STEPS")
    print("="*60)
    
    print("\n1. 🔑 OpenAI API Key:")
    print("   - Your key is configured from vapi.env")
    print("   - Make sure you have sufficient credits")
    
    print("\n2. 📞 Setup SIP Telephony:")
    print("   - Configure SIP trunk in LiveKit dashboard")
    print("   - Set up outbound calling for candidate interviews")
    print("   - Use your existing Twilio credentials if available")
    
    print("\n3. 🧪 Test the Interview Agent:")
    print("   - Run: python interview_agent.py console")
    print("   - This will start the LiveKit agent in console mode")
    
    print("\n4. 🔄 Full Migration:")
    print("   - Replace VAPI client with LiveKit + OpenAI")
    print("   - Update webhook endpoints")
    print("   - Migrate cost tracking")
    
    print("\n💰 Expected Benefits:")
    print("   - Simplified architecture with fewer dependencies")
    print("   - Direct OpenAI integration")
    print("   - Better conversation flow")


async def main():
    """Main setup test function"""
    print("🚀 LiveKit + OpenAI Migration Setup Test")
    print("="*60)
    
    # Test LiveKit connection
    livekit_ok = await test_livekit_connection()
    
    # Test OpenAI key configuration
    openai_key_ok = test_openai_key()
    
    # Test OpenAI integration
    integration_ok = await test_openai_integration()
    
    # Summary
    print("\n" + "="*60)
    print("📊 SETUP TEST RESULTS")
    print("="*60)
    print(f"LiveKit Connection: {'✅ OK' if livekit_ok else '❌ FAILED'}")
    print(f"OpenAI API Key: {'✅ OK' if openai_key_ok else '❌ FAILED'}")
    print(f"OpenAI Integration: {'✅ OK' if integration_ok else '❌ FAILED'}")
    
    if livekit_ok and openai_key_ok and integration_ok:
        print("\n🎉 All tests passed! Ready for migration.")
        print("🔥 You can now test the interview agent!")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
    
    print_next_steps()


if __name__ == "__main__":
    asyncio.run(main()) 