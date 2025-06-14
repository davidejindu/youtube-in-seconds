from flask_cors import CORS
from flask import Flask, jsonify, request
from youtube_transcript_api import YouTubeTranscriptApi
import os
from dotenv import load_dotenv
import re
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)
CORS(app)

@app.route("/summary", methods=["POST"])
def summary():
    data = request.get_json()
    yt_url = data.get('url')
    
    if not yt_url:
        return jsonify({"message": "Url not found"}), 404
    
    try:
        yt_id = get_yt_id(yt_url)
        yt_transcript = YouTubeTranscriptApi.get_transcript(yt_id)
    
        complete_transcript = " ".join(item["text"] for item in yt_transcript)
        summary = gemini_summary(complete_transcript)
        
        return jsonify({"summary": summary})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def gemini_summary(transcipt):
    prompt = ("Summarize this Youtube transcipt into clear concise paragraphs on the main points using headers and bullet points .\n\n"f"{transcipt}")
    
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text.strip()
    
def get_yt_id(url):
    found = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    
    if found:
        return found.group(1)
    raise ValueError("Invalid Youtube URL")

if __name__ == "__main__":
    app.run(debug=True)
        
        