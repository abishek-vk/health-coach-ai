import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    print("🔍 Available Gemini Models:")
    print("=" * 60)
    
    try:
        models = genai.list_models()
        available_models = []
        for model in models:
            if "generateContent" in model.supported_generation_methods:
                print(f"✅ {model.name}: {model.display_name}")
                available_models.append(model.name)
        
        if available_models:
            print("\n" + "=" * 60)
            print("Model IDs for configuration:")
            for m in available_models:
                print(f"  - {m}")
        else:
            print("\n⚠️ No models support generateContent")
    except Exception as e:
        print(f"❌ Error listing models: {e}")
else:
    print("❌ GEMINI_API_KEY not found")
