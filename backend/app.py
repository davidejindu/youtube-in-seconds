from flask_cors import CORS
from flask import Flask, jsonify, request
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import os
from dotenv import load_dotenv
import re
import google.generativeai as genai
import requests
from urllib.parse import parse_qs, urlparse

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
        
        # Try multiple approaches to get transcript
        yt_transcript = None
        error_messages = []
        
        # Method 1: Try with custom headers
        try:
            yt_transcript = YouTubeTranscriptApi.get_transcript(
                yt_id,
                proxies=None,
                cookies=None
            )
        except Exception as e1:
            error_messages.append(f"Method 1 failed: {str(e1)}")
            
            # Method 2: Try with different language codes
            try:
                yt_transcript = YouTubeTranscriptApi.get_transcript(
                    yt_id, 
                    languages=['en', 'en-US', 'en-GB']
                )
            except Exception as e2:
                error_messages.append(f"Method 2 failed: {str(e2)}")
                
                # Method 3: Try to get any available transcript
                try:
                    transcript_list = YouTubeTranscriptApi.list_transcripts(yt_id)
                    transcript = transcript_list.find_transcript(['en', 'en-US', 'en-GB'])
                    yt_transcript = transcript.fetch()
                except Exception as e3:
                    error_messages.append(f"Method 3 failed: {str(e3)}")
                    
                    # Method 4: Try manually generated transcript
                    try:
                        transcript_list = YouTubeTranscriptApi.list_transcripts(yt_id)
                        # Get the first available transcript
                        for transcript in transcript_list:
                            yt_transcript = transcript.fetch()
                            break
                    except Exception as e4:
                        error_messages.append(f"Method 4 failed: {str(e4)}")
        
        if not yt_transcript:
            return jsonify({
                'error': 'Could not retrieve transcript. This might be due to: 1) Video has no transcript/captions, 2) Transcript is disabled, 3) IP blocking by YouTube, or 4) Video is private/restricted.',
                'details': error_messages
            }), 500
    
        complete_transcript = " ".join(item["text"] for item in yt_transcript)
        
        if not complete_transcript.strip():
            return jsonify({'error': 'Retrieved transcript is empty'}), 500
            
        summary = gemini_summary(complete_transcript)
        
        return jsonify({"summary": summary})
    
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500
    
def gemini_summary(transcript):
    try:
        prompt = (
            "Summarize this YouTube transcript into clear, concise paragraphs covering the main points. "
            "Use headers and bullet points to organize the information effectively.\n\n"
            f"Transcript: {transcript}"
        )
        
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        if not response.text:
            return "Unable to generate summary - the AI response was empty."
            
        return response.text.strip()
    except Exception as e:
        return f"Error generating summary: {str(e)}"
    
def get_yt_id(url):
    """Extract YouTube video ID from various URL formats"""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    raise ValueError("Invalid YouTube URL - could not extract video ID")

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "message": "Server is running"}), 200

if __name__ == "__main__":
    app.run(debug=True)