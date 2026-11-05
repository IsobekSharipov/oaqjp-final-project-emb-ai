"""Flask application for IBM Watson emotion detection."""

from flask import Flask, render_template, request

from EmotionDetection import emotion_detector

app = Flask(__name__)


@app.route("/")
def index():
    """Display the emotion detector web interface."""
    return render_template("index.html")


@app.route("/emotionDetector")
def detect_emotion():
    """Analyze text and return formatted emotion scores."""
    text_to_analyze = request.args.get("textToAnalyze", "").strip()
    if not text_to_analyze:
        return "Invalid text! Please try again!", 400

    try:
        result = emotion_detector(text_to_analyze)
    except (ValueError, KeyError, IndexError, TypeError):
        app.logger.exception("Unexpected emotion detection response")
        return "Emotion detection service returned invalid data.", 502
    except Exception:  # pylint: disable=broad-exception-caught
        app.logger.exception("Emotion detection service unavailable")
        return "Emotion detection service is unavailable.", 503

    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again!", 400

    return (
        "For the given statement, the system response is "
        f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, 'joy': {result['joy']}, "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
