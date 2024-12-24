import json
import os

def load_json(file_path):
    """Load JSON data from a file."""
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    else:
        raise FileNotFoundError(f"{file_path} not found")

def save_json(data, file_path):
    """Save JSON data to a file."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
        
def load_user_settings(settings_path):
    """Load user-specific settings like API key, language, timezone."""
    try:
        return load_json(settings_path)
    except FileNotFoundError:
        print(f"Warning: {settings_path} not found. Using default settings.")
        return {
            "openai_api_key": "YOUR_OPENAI_API_KEY",
            "language": "English",
            "timezone": "UTC"
        }
