import os
import requests

def check_openrouter_key():
    # Retrieve the API key from environment variables
    api_key = ""
    
    if not api_key:
        print("❌ Error: OPENROUTER_API_KEY environment variable is not set.")
        return False

    url = "https://openrouter.ai/api/v1/models"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    try:
        response = requests.get(url, headers=headers)
        
        # Check HTTP Status Code
        if response.status_code == 200:
            print("✅ Success! Your OpenRouter API key is working perfectly.")
            return True
        elif response.status_code == 401:
            print("❌ Invalid Key: Unauthorized access. Please check your API key.")
            return False
        else:
            print(f"⚠️ Unexpected Response: Status Code {response.status_code}")
            print(response.json())
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    check_openrouter_key()
