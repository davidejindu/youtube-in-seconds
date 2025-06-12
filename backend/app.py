from flask_cors import CORS
from flask import Flask, jsonify, request
from youtube_transcript_api import YouTubeTranscriptApi
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)