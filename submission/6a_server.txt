"""Flask web application for the Watson emotion detector."""

from flask import Flask, jsonify, render_template, request

from EmotionDetection import emotion_detector

app = Flask(__name__)


@app.get("/")
def home():
    """Render the emotion detector page."""
    return render_template("index.html")


@app.get("/emotionDetector")
def emotion_detector_route():
    """Return emotion scores or a readable error as JSON."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    if not text_to_analyze.strip():
        return jsonify({"error": {"message": "Please enter some text to analyze."}}), 400

    result = emotion_detector(text_to_analyze)
    error = result.get("error")
    if error:
        status_code = error.get("status_code", 502)
        if status_code not in (400, 502):
            status_code = 502
        return jsonify(result), status_code
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
