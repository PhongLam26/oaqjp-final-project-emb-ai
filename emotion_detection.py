"""Initial Watson NLP request function for the final project."""

import requests

WATSON_URL = (
    "https://sn-watson-emotion.labs.skills.network/v1/"
    "watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
MODEL_ID = "emotion_aggregated-workflow_lang_en_stock"
REQUEST_TIMEOUT = 10


def emotion_detector(text_to_analyze):
    """Return the Watson NLP response text for the submitted sentence."""
    headers = {"grpc-metadata-mm-model-id": MODEL_ID}
    payload = {"raw_document": {"text": text_to_analyze}}
    try:
        response = requests.post(
            WATSON_URL,
            json=payload,
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )
    except requests.RequestException:
        return "Watson NLP service could not be reached. Please try again later."
    return response.text
