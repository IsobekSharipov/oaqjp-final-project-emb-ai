"""Unit tests for the EmotionDetection package."""

import unittest
from unittest.mock import Mock, patch

from EmotionDetection import emotion_detector


class TestEmotionDetector(unittest.TestCase):
    """Check all five dominant emotion categories."""

    def check_emotion(self, text, expected):
        """Mock the Watson response and verify the returned emotion."""
        scores = {
            "anger": 0.05,
            "disgust": 0.05,
            "fear": 0.05,
            "joy": 0.05,
            "sadness": 0.05,
        }
        scores[expected] = 0.90

        response = Mock()
        response.status_code = 200
        response.json.return_value = {
            "emotionPredictions": [{"emotion": scores}]
        }

        with patch(
            "EmotionDetection.emotion_detection.requests.post",
            return_value=response,
        ):
            result = emotion_detector(text)

        self.assertEqual(result["dominant_emotion"], expected)
        for emotion, score in scores.items():
            self.assertEqual(result[emotion], score)

    def test_joy(self):
        self.check_emotion("I am glad this happened", "joy")

    def test_anger(self):
        self.check_emotion("I am really mad about this", "anger")

    def test_disgust(self):
        self.check_emotion("I am disgusted by this", "disgust")

    def test_sadness(self):
        self.check_emotion("I am so sad about this", "sadness")

    def test_fear(self):
        self.check_emotion("I am afraid this will happen", "fear")


if __name__ == "__main__":
    unittest.main()
