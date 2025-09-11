from flask import Flask, request, jsonify, render_template, redirect, session, url_for
import os
import torch
import time
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24) # It's important to set a secret key for session management


supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    raise RuntimeError(
        "SUPABASE_URL and SUPABASE_KEY environment variables are required.\n"
        "Set them before running the app, e.g.:\n"
        "  export SUPABASE_URL='https://<your-project-ref>.supabase.co'\n"
        "  export SUPABASE_KEY='<your-anon-public-key>'\n"
        "If you intentionally want to hardcode values for testing, set them in the environment or update this file deliberately."
    )

supabase: Client = create_client(supabase_url, supabase_key)

MODEL_NAME = "Priyanshuchaudhary2425/ScamGuard"

# Check if model is already cached locally
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
    user = session.get('user')
    return render_template('index.html', user=user)

@app.route('/login')
def login():
    try:
        # Use the correct redirect URL format for Supabase
        redirect_url = f"{request.url_root}callback"
        auth_url = supabase.auth.sign_in_with_oauth({
            'provider': 'google',
            'options': {
                'redirect_to': redirect_url
            }
        }).url
        return redirect(auth_url)
    except Exception as e:
        return jsonify({"error": f"Login failed: {str(e)}"}), 500

@app.route('/callback')
def callback():
    code = request.args.get('code')
    error = request.args.get('error')
    
    if error:
        return jsonify({"error": f"OAuth error: {error}"}), 400
    
    if code:
        try:
            # Exchange the authorization code for a session
            session_data = supabase.auth.exchange_code_for_session({'auth_code': code, 'flow_type': 'pkce'})
            if session_data and session_data.user:
                session['user'] = {
                    'id': session_data.user.id,
                    'email': session_data.user.email,
                    'name': getattr(session_data.user, 'user_metadata', {}).get('full_name', ''),
                    'avatar_url': getattr(session_data.user, 'user_metadata', {}).get('avatar_url', '')
                }
                return redirect(url_for('index'))
            else:
                return jsonify({"error": "Failed to get user data"}), 400
        except Exception as e:
            print(f"Callback error: {str(e)}")
            return jsonify({"error": f"Authentication failed: {str(e)}"}), 400
    
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/predict', methods=['POST'])
def predict():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
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