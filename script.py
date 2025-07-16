# app.py
from flask import Flask, jsonify, request
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled, VideoUnavailable
from typing import List, Optional

app = Flask(__name__)

def get_transcript_text_for_api(video_id: str) -> Optional[List[str]]:
    """
    Fetches the transcript for a given YouTube video ID and returns only the text.
    Handles specific errors by returning None.
    """
    try:
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_lines = [item['text'] for item in transcript_data]
        return transcript_lines
    except (NoTranscriptFound, TranscriptsDisabled):
        # Specific errors where no transcript is available/disabled
        return None
    except VideoUnavailable:
        # Video is private, deleted, or otherwise inaccessible
        return None
    except Exception as e:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred for video ID {video_id}: {e}")
        return None

@app.route("/transcript/<string:video_id>", methods=["GET"])
def get_youtube_transcript_text(video_id: str):
    """
    Fetches the transcript for a YouTube video given its `video_id`.
    Returns a JSON array of strings (each string being a line of the transcript).
    Returns an empty array `[]` if no transcript is found or if transcripts are disabled for the video.
    """
    transcript_text = get_transcript_text_for_api(video_id)
    if transcript_text is not None:
        return jsonify(transcript_text), 200
    else:
        # If no transcript is found or it's disabled, return an empty array
        return jsonify([]), 200 # Return 200 OK, as it's a successful response indicating no data

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)