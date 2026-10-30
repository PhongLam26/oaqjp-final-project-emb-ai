"""Unit tests for the Watson emotion detector."""

import unittest
from unittest.mock import Mock, patch

from EmotionDetection.emotion_detection import EMOTION_NAMES, emotion_detector


class EmotionDetectorTests(unittest.TestCase):
    """Verify valid scores and error handling for the detector."""

    def setUp(self):
        """Create a complete score payload with a clear dominant emotion."""
        self.scores = {
            "anger": 0.05,
            "disgust": 0.05,
            "fear": 0.05,
            "joy": 0.8,
            "sadness": 0.05,
        }

    def mock_response(self, status_code=200):
        """Create a Watson-like HTTP response for a unit test."""
        response = Mock()
        response.status_code = status_code
        response.json.return_value = {
            "emotionPredictions": [{"emotion": self.scores}]
        }
        return response

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_detects_each_dominant_emotion(self, post):
        """Map each of the five emotion phrases to its top score."""
        phrases = {
            "anger": "I am very angry",
            "disgust": "That smells disgusting",
            "fear": "I am afraid of what might happen",
            "joy": "I am delighted with the result",
            "sadness": "I feel very sad today",
        }

        for expected in EMOTION_NAMES:
            with self.subTest(expected=expected):
                self.scores = {name: 0.05 for name in EMOTION_NAMES}
                self.scores[expected] = 0.8
                post.return_value = self.mock_response()
                result = emotion_detector(phrases[expected])
                self.assertEqual(result["dominant_emotion"], expected)
                self.assertEqual(set(result), set(EMOTION_NAMES) | {"dominant_emotion"})
                for name in EMOTION_NAMES:
                    self.assertIsInstance(result[name], float)

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_sends_expected_watson_request(self, post):
        """Send text in the Watson raw_document payload."""
        post.return_value = self.mock_response()

        emotion_detector("I am really mad about this")

        arguments = post.call_args.kwargs
        self.assertEqual(
            arguments["json"],
            {"raw_document": {"text": "I am really mad about this"}},
        )
        self.assertEqual(
            arguments["headers"]["grpc-metadata-mm-model-id"],
            "emotion_aggregated-workflow_lang_en_stock",
        )

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_http_400_returns_structured_error(self, post):
        """Report a clear error when Watson rejects a request."""
        post.return_value = self.mock_response(status_code=400)

        result = emotion_detector("Invalid input")

        self.assertEqual(set(result), set(EMOTION_NAMES) | {"dominant_emotion"})
        self.assertTrue(all(result[name] is None for name in EMOTION_NAMES))
        self.assertIsNone(result["dominant_emotion"])

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_empty_input_is_rejected_before_request(self, post):
        """Return an input error without contacting Watson for blank text."""
        result = emotion_detector("   ")

        self.assertEqual(set(result), set(EMOTION_NAMES) | {"dominant_emotion"})
        self.assertIsNone(result["dominant_emotion"])
        post.assert_not_called()

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_connection_failure_returns_service_error(self, post):
        """Report network failures without inventing emotion scores."""
        import requests

        post.side_effect = requests.ConnectionError("unavailable")

        result = emotion_detector("A sample sentence")

        self.assertEqual(result["error"]["status_code"], 502)
        self.assertTrue(all(result[name] is None for name in EMOTION_NAMES))


if __name__ == "__main__":
    unittest.main()
