"""
LiveKit Testing Configuration - OpenAI Integration
Reads from vapi.env file in parent directory
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Get the parent directory path (one level up from weruntesting/)
parent_dir = Path(__file__).parent.parent
vapi_env_path = parent_dir / "vapi.env"

# Load environment variables from parent directory's vapi.env file
load_dotenv(vapi_env_path)

# LiveKit Configuration
LIVEKIT_URL = os.getenv("LIVEKIT_URL")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Twilio Configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# Keep your existing Gemini for transcript analysis
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Verify critical environment variables
def verify_env_vars():
    """Verify that required environment variables are loaded"""
    required_vars = {
        "LIVEKIT_URL": LIVEKIT_URL,
        "LIVEKIT_API_KEY": LIVEKIT_API_KEY,
        "LIVEKIT_API_SECRET": LIVEKIT_API_SECRET,
        "OPENAI_API_KEY": OPENAI_API_KEY,
    }
    
    missing = [var for var, value in required_vars.items() if not value]
    if missing:
        print(f"❌ Missing required environment variables: {', '.join(missing)}")
        print(f"📁 Looking for vapi.env at: {vapi_env_path}")
        return False
    
    print("✅ All required environment variables loaded successfully")
    return True

# Twilio variables for phone integration
def verify_twilio_vars():
    """Verify Twilio environment variables are available"""
    twilio_vars = {
        "TWILIO_ACCOUNT_SID": TWILIO_ACCOUNT_SID,
        "TWILIO_AUTH_TOKEN": TWILIO_AUTH_TOKEN,
        "TWILIO_PHONE_NUMBER": TWILIO_PHONE_NUMBER,
    }
    
    missing = [var for var, value in twilio_vars.items() if not value]
    if missing:
        print(f"❌ Missing Twilio variables: {', '.join(missing)}")
        return False
    
    print("✅ All Twilio environment variables loaded successfully")
    return True

# Debug: Print loaded variables (excluding sensitive ones)
if __name__ == "__main__":
    print(f"📁 Loading environment from: {vapi_env_path}")
    print(f"📁 File exists: {vapi_env_path.exists()}")
    print("🔧 Environment variables loaded:")
    print(f"  LIVEKIT_URL: {LIVEKIT_URL[:30]}..." if LIVEKIT_URL else "  LIVEKIT_URL: None")
    print(f"  LIVEKIT_API_KEY: {LIVEKIT_API_KEY[:10]}..." if LIVEKIT_API_KEY else "  LIVEKIT_API_KEY: None")
    print(f"  OPENAI_API_KEY: {OPENAI_API_KEY[:10]}..." if OPENAI_API_KEY else "  OPENAI_API_KEY: None")
    print(f"  TWILIO_PHONE_NUMBER: {TWILIO_PHONE_NUMBER}" if TWILIO_PHONE_NUMBER else "  TWILIO_PHONE_NUMBER: None")
    verify_env_vars()
    verify_twilio_vars() 