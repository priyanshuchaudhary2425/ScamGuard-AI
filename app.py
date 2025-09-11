from flask import Flask, request, jsonify, render_template
import os
import time
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_NAME = "Priyanshuchaudhary2425/ScamGuard"
label_map = {0: "Not Scam", 1: "Scam"}

# Simple cache path attempt (optional) - keeps behavior similar to your original
model_cache_path = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "hub", MODEL_NAME.replace("/", "_"))

print("Loading tokenizer and model (this may take a while if not cached)...")
try:
    if os.path.exists(model_cache_path):
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, local_files_only=True)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, local_files_only=True)
    else:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
    model.eval()
    print("✅ Model loaded.")
except Exception as e:
    print("❌ Failed loading model:", e)
    raise

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

app = Flask(__name__)

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
    return jsonify({'results': results, 'inference_time': inference_time})

if __name__ == '__main__':
    app.run(debug=True)
