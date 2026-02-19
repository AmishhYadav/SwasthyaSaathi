#!/usr/bin/env python3
"""Quick test script to verify API key is loaded correctly"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root
project_root = Path(__file__).parent
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if api_key:
    print(f"✅ API Key found! Length: {len(api_key)} characters")
    print(f"✅ First 10 chars: {api_key[:10]}...")
    print(f"✅ Last 10 chars: ...{api_key[-10:]}")
else:
    print("❌ API Key NOT found!")
    print("Please check your .env file in the project root.")

