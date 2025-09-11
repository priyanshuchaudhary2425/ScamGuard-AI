from flask import Flask, request, jsonify, render_template
import os
import torch
import time
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F

app = Flask(__name__)
app.secret_key = os.urandom(24)  # keep a secret key for Flask sessions if needed

MODEL_NAME = "Priyanshuchaudhary2425/ScamGuard"

# Attempt to load from local cache if available, otherwise download from HF hub
model_cache_path = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "hub", MODEL_NAME.replace("/", "_"))

if os.path.exists(model_cache_path):
    print("✅ Loading model from local cache...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, local_files_only=True)
else:
    print("🔄 Downloading model from Hugging Face Hub...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

model.eval()
print("✅ ScamGuard model ready")

# Map label ids to readable labels
label_map = {0: "Not Scam", 1: "Scam"}


def predict_scam(texts: list[str]):
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
    start = time.time()
    with torch.inference_mode():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=-1)
        confidences, predicted_classes = torch.max(probs, dim=1)
    end = time.time()
    inference_time = (end - start) * 1000

    results = []
    for i in range(len(texts)):
        label = label_map[predicted_classes[i].item()]
        confidence = confidences[i].item()
        results.append({
            'text': texts[i],
            'label': label,
            'confidence': confidence
        })
    return results, round(inference_time, 2)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request body'}), 400
    texts = data.get('texts')
    if not texts or not isinstance(texts, list):
        return jsonify({'error': 'No texts provided or invalid format'}), 400

    results, inference_time = predict_scam(texts)
    return jsonify({
        'results': results,
        'inference_time': inference_time
    })


if __name__ == '__main__':
    app.run(debug=True)