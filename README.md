# Final Project

Emotion detection with the IBM Watson NLP EmotionPredict service.

- Public repository: https://github.com/PhongLam26/oaqjp-final-project-emb-ai
- Public README: https://github.com/PhongLam26/oaqjp-final-project-emb-ai/blob/main/README.md
- Public package initializer: https://github.com/PhongLam26/oaqjp-final-project-emb-ai/blob/main/EmotionDetection/__init__.py

## Run locally

Install the dependencies and start the Flask app:

```sh
python -m pip install -r requirements.txt
python server.py
```

Open http://127.0.0.1:5000 and enter text. The app calls the IBM Skills Network Watson NLP EmotionPredict endpoint and displays anger, disgust, fear, joy, sadness, and the dominant emotion. An unavailable service or rejected request is shown as an error; the app does not substitute generated scores.

Run the unit tests and static analysis with:

```sh
python -m unittest -v test_emotion_detection.py
pylint server.py
```

The detector's unit tests use mocked HTTP responses to cover parsing, all five dominant emotions, empty input, and HTTP 400 handling without depending on a live network service. Run `python -c "from EmotionDetection.emotion_detection import emotion_detector; print(emotion_detector('I am really mad about this'))"` to make a live service request.
