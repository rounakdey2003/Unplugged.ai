import joblib
import os

pipe_lr = joblib.load(open(os.path.join(os.path.dirname(__file__), "text_emotion.pkl"), "rb"))

emotions_emoji_dict = {"anger": "😠", "disgust": "🤮", "fear": "😱", "happy": "🤗", "joy": "😂", "neutral": "😐", "sad": "😔",
                       "sadness": "😔", "shame": "😳", "surprise": "😮"}


def predict_emotions(docx):
    results = pipe_lr.predict([docx])
    return results[0]


def get_prediction_proba(docx):
    results = pipe_lr.predict_proba([docx])
    return results
