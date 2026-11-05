"""Tests for the Flask emotion detection endpoints."""

import unittest
from unittest.mock import patch

from server import app


class TestServer(unittest.TestCase):
    """Validate page loading and input error handling."""

    def setUp(self):
        self.client = app.test_client()

    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"NLP - Emotion Detection", response.data)

    def test_blank_input(self):
        response = self.client.get("/emotionDetector?textToAnalyze=")
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Invalid text", response.data)

    def test_whitespace_input(self):
        response = self.client.get("/emotionDetector?textToAnalyze=%20%20")
        self.assertEqual(response.status_code, 400)

    @patch("server.emotion_detector")
    def test_emotion_result(self, detector):
        detector.return_value = {
            "anger": 0.9, "disgust": 0.02, "fear": 0.02,
            "joy": 0.01, "sadness": 0.05, "dominant_emotion": "anger"
        }
        response = self.client.get("/emotionDetector?textToAnalyze=angry")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"dominant emotion is anger", response.data)


if __name__ == "__main__":
    unittest.main()
