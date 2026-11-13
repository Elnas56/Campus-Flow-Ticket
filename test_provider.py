import os 

def get_api_key(provider):
    api_keys = {
    "Gemini": "GEMINI_API_KEY",
    "OpenAI": "OPENAI_API_KEY",
    "OpenRouter": "OPENROUTER_API_KEY",
    "Hugging Face": "HF_TOKEN"
    }
    
    if provider not in api_keys:
        print(f"Unsupported AI provider.")
        return
 
    api_key_name = api_keys[provider]
    api_key = os.getenv(api_key_name)
     
    if not api_key:
        print(f"{provider} key is not configured.")
        return

    return api_key
    
provider = "Claude"
key = get_api_key(provider)

print("Key detected" if key else "Key unavailable")