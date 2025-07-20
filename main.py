from flask import Flask, request, jsonify, Response
from google import genai
from google.genai import types
import json
import os
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def load_api_key():
    # Try secrets.json first
    try:
        with open("secrets.json", "r") as f:
            return json.load(f).get("GEMINI_API_KEY")
    except Exception:
        # Fall back to env variable
        return os.environ.get("OPENROUTER_API_KEY")


# Configuration
API_KEY = load_api_key()  # Your API key
client = genai.Client(api_key=API_KEY)


def create_translation_prompt(text, target_lang="en", source_lang="ja"):
    """Create translation prompt based on language pair"""
    
    lang_names = {
        "zh": "Chinese",
        "en": "English", 
        "ja": "Japanese",
        "ko": "Korean",
        "es": "Spanish",
        "fr": "French",
        "de": "German"
    }
    
    source_name = lang_names.get(source_lang, source_lang)
    target_name = lang_names.get(target_lang, target_lang)
    return f"""You are a professional {source_name}-to-{target_name} translator.

        Retain honorifics.
        Preserve tone, emotion and nuances when possible. 
        You must return the result only.

        Translate the following {source_name} text into natural {target_name}:
        {text}"""

@app.route('/translate', methods=['GET'])
def translate():
    """Standard translation endpoint"""
    try:
        text = request.args.get('text', '').strip()
        target_lang = request.args.get('lang', 'en')
        source_lang = request.args.get('source', 'jp')
        
        if not text:
            return "No text provided"
        
        # Create prompt
        prompt = create_translation_prompt(text, target_lang, source_lang)
        
        # Generate translation
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                # Disable Thinking
                thinking_config=types.ThinkingConfig(thinking_budget=0)
            )
        )
        
        # Check if response was blocked
        if not response.text:
            if response.prompt_feedback:
                return "Content was blocked"
            else:
                return "No response was generated"
        
        translation = response.text.strip()
        
        # Clean up translation (remove markers if present)
        translation = re.sub(r'<Start>|<End>', '', translation).strip()

        return translation
    except Exception as e:
        return "Unknown error"

@app.route('/translate/stream', methods=['POST'])
def translate_stream():
    """Streaming translation endpoint"""
    return "API Endpoint WIP"

@app.route('/models', methods=['GET'])
def get_models():
    """Get available models"""
    return jsonify({
        'models': [
            {
                'id': 'flash',
                'name': 'Gemini 2.5 Flash',
                'description': 'Latest and fastest model for real-time translation',
                'version': 'gemini-2.5-flash'
            }
        ]
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🚀 Starting Gemini Translation Server...")
    print("📋 Endpoints:")
    print("  GET/POST /translate - Standard translation")
    print("  POST /translate/stream - Streaming translation")
    print("  GET /models - Available models")
    print()
    print("💡 Example usage:")
    print("  curl 'http://127.0.0.1:5000/translate?text=こんにちは&lang=en'")
    print("  curl -X POST http://127.0.0.1:5000/translate -H 'Content-Type: application/json' -d '{\"text\":\"こんにちは\",\"lang\":\"en\"}'")
    print()
    print("🔄 For streaming:")
    print("  curl -X POST http://127.0.0.1:5000/translate/stream -H 'Content-Type: application/json' -d '{\"text\":\"長いテキスト\",\"lang\":\"en\"}' --no-buffer")
    print()
    
    app.run(host='127.0.0.1', port=5000, debug=True)