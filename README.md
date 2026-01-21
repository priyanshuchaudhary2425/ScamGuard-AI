

**ScamGuard** is a web-based, AI-driven assistant that analyzes chat messages in real-time. It uses a state-of-the-art Natural Language Processing model to classify messages as either "Safe" or "Scam," providing immediate feedback with a confidence score. This directly helps users identify potential social engineering attacks before they become victims.

The core of our solution is the **`ScamGuard`** model, a fine-tuned version of `bert-base-cased` that achieves **98.13% accuracy** on our evaluation dataset.

---

### ► Tech Stack

* **Backend:** Python, Flask
* **Machine Learning:** PyTorch, Hugging Face Transformers
* **Frontend:** HTML, Tailwind CSS, JavaScript
* **Core Model:** [Priyanshuchaudhary2425/ScamGuard](https://huggingface.co/Priyanshuchaudhary2425/ScamGuard) on Hugging Face Hub

---

### ► How to Run Locally

Follow these steps to get the application running on your local machine.

**1. Clone the Repository**
```bash
git clone https://github.com/priyanshuchaudhary2425/ScamGuard-AI.git
cd ScamGuard-AI
```

**2. Create and Activate a Virtual Environment**
```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install Dependencies**
First, make sure you have created a `requirements.txt` file. You can generate it with the following command in your activated virtual environment:
```bash
pip freeze > requirements.txt
```
Then, install the required packages:
```bash
pip install -r requirements.txt
```
*(Note: The first run might take some time to download the Hugging Face model).*

**4. Run the Flask Application**
```bash
python app.py
```

**5. Open in Browser**
Navigate to `http://127.0.0.1:5000` in your web browser to start using ScamGuard AI.

---

### ► Project File Structure
```
.
├── app.py              # Main Flask application logic
├── templates/
│   └── index.html      # Frontend HTML and JavaScript
├── requirements.txt    # Python dependencies
└── README.md           # You are here!
```

---
### ► Model Performance

The `ScamGuard` model was evaluated with the following results:
* **Accuracy:** 0.9813
* **F1 Score:** 0.9803
* **Precision:** 0.9826
* **Recall:** 0.9782

---

### ► Future Improvements

* **Audio Support:** Extend the functionality to analyze live audio from calls by integrating a speech-to-text model.
* **Browser Extension:** Create a browser plugin to protect users on various websites and social media platforms.
* **Enhanced Explanations:** Provide more details on *why* a message was flagged (e.g., "Urgency detected," "Suspicious link pattern").

---
Built with ❤️ for the Hackathon 2025.
