#!/usr/bin/env python3
"""
Test script to verify the setup and dependencies
"""
import sys
import subprocess
import os
from dotenv import load_dotenv

def test_imports():
    """Test if all required packages can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
    except ImportError:
        print("❌ Streamlit not found. Run: pip install streamlit")
        return False
    
    try:
        from langchain.chat_models import init_chat_model
        from langgraph.prebuilt import create_react_agent
        print("✅ LangChain/LangGraph imported successfully")
    except ImportError:
        print("❌ LangChain/LangGraph not found. Run: pip install -r requirements.txt")
        return False
    
    try:
        import requests
        from dotenv import load_dotenv
        print("✅ Other dependencies imported successfully")
    except ImportError:
        print("❌ Some dependencies missing. Run: pip install -r requirements.txt")
        return False
    
    return True

def test_env_vars():
    """Test if environment variables are set"""
    print("\n🔑 Testing environment variables...")
    
    load_dotenv()
    
    openai_key = os.getenv("OPENAI_API_KEY")
    weather_key = os.getenv("WEATHER_API_KEY")
    serp_key = os.getenv("SERP_API_KEY")
    
    if openai_key:
        print("✅ OPENAI_API_KEY is set")
    else:
        print("❌ OPENAI_API_KEY not found in .env file")
    
    if weather_key:
        print("✅ WEATHER_API_KEY is set")
    else:
        print("⚠️  WEATHER_API_KEY not found (optional for basic functionality)")
    
    if serp_key:
        print("✅ SERP_API_KEY is set")
    else:
        print("⚠️  SERP_API_KEY not found (optional for basic functionality)")
    
    return bool(openai_key)

def main():
    """Run all tests"""
    print("🚀 Travel Bot Setup Test")
    print("=" * 40)
    
    imports_ok = test_imports()
    env_ok = test_env_vars()
    
    print("\n" + "=" * 40)
    if imports_ok and env_ok:
        print("🎉 Setup looks good! You can now run the UI with:")
        print("   python run_ui.py")
    else:
        print("❌ Setup incomplete. Please fix the issues above.")
        if not imports_ok:
            print("   Install dependencies: pip install -r requirements.txt")
        if not env_ok:
            print("   Set up your .env file with API keys")

if __name__ == "__main__":
    main()
