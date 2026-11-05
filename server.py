"""Flask web server for the Emotion Detector application."""

from flask import Flask, request, render_template_string
from EmotionDetection import emotion_detector

app = Flask(__name__)

PAGE = """
<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Emotion Detector</title></head>
<body>
  <h1>Emotion Detector</h1>
  <form action="/emotionDetector" method="get">
    <label for="textToAnalyze">Enter text:</label>
    <input id="textToAnalyze" name="textToAnalyze" required>
    <button type="submit">Analyze</button>
  </form>
</body>
</html>
"""


@app.route("/")
def index():
    """Display the emotion detection form."""
    return render_template_string(PAGE)


@app.route("/emotionDetector")
def detect_emotion():
    """Analyze text and display the dominant emotion."""
    text_to_analyze = request.args.get("textToAnalyze", "").strip()
    if not text_to_analyze:
        return "Invalid text! Please try again!", 400

    try:
        result = emotion_detector(text_to_analyze)
    except Exception:
        app.logger.exception("Emotion detection service failed")
        return "Emotion detection service is unavailable.", 503

    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again!", 400

    return (
        f"For the given statement, the system response is "
        f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, 'joy': {result['joy']}, "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
