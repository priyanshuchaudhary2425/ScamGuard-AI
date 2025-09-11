# ScamGuard API with Supabase Authentication

A Flask-based API that provides scam detection using machine learning, integrated with Supabase for Google OAuth authentication.

## Features

- 🔍 **Scam Detection**: Uses a fine-tuned transformer model to detect scam messages
- 🔐 **Google OAuth**: Secure authentication via Supabase and Google
- ⚡ **Fast Inference**: Optimized model loading and prediction
- 🛡️ **Session Management**: Secure user sessions with Flask

## Prerequisites

- Python 3.8+
- Google Cloud Console account
- Supabase account

## Setup Instructions

### 1. Clone and Install Dependencies

```bash
git clone <your-repo-url>
cd API
pip install -r requirements.txt
```

### 2. Google Cloud Console Setup

1. **Go to [Google Cloud Console](https://console.cloud.google.com/)**
2. **Create a new project** or select an existing one
3. **Enable APIs**:
   - Go to "APIs & Services" → "Library"
   - Search for "Google Identity" or "Google+ API"
   - Enable the API
4. **Configure OAuth Consent Screen**:
   - Go to "APIs & Services" → "OAuth consent screen"
   - Choose "External" user type
   - Fill in required fields:
     - App name: "ScamGuard API"
     - User support email: Your email
     - Developer contact: Your email
   - Add your domain to "Authorized domains"
   - Add your email to "Test users"
5. **Create OAuth 2.0 Credentials**:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth 2.0 Client IDs"
   - Application type: "Web application"
   - Name: "ScamGuard Web Client"
   - Authorized redirect URIs: `https://your-project-ref.supabase.co/auth/v1/callback`
   - **Save the Client ID and Client Secret**

### 3. Supabase Setup

1. **Go to [Supabase Dashboard](https://supabase.com/dashboard)**
2. **Create a new project** or use existing one
3. **Get your project credentials**:
   - Go to "Settings" → "API"
   - Copy your "Project URL" and "anon public" key
4. **Configure Google Authentication**:
   - Go to "Authentication" → "Providers"
   - Find "Google" and click "Enable"
   - Enter your Google OAuth credentials:
     - Client ID: (from Google Cloud Console)
     - Client Secret: (from Google Cloud Console)
5. **Configure URL Settings**:
   - Go to "Authentication" → "URL Configuration"
   - Set Site URL: `http://localhost:5000` (for development)
   - Add Redirect URLs: `http://localhost:5000/callback`

### 4. Environment Variables

Create a `.env` file in your project root:

```bash
# Supabase Configuration
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_KEY=your-anon-key-here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

Or export them directly:

```bash
export SUPABASE_URL='https://your-project-ref.supabase.co'
export SUPABASE_KEY='your-anon-key-here'
```

### 5. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## API Endpoints

### Authentication

- `GET /login` - Redirects to Google OAuth login
- `GET /callback` - Handles OAuth callback
- `GET /logout` - Logs out the current user

### Scam Detection

- `POST /predict` - Analyzes text for scam content
  - **Headers**: `Content-Type: application/json`
  - **Body**: `{"texts": ["text1", "text2", ...]}`
  - **Response**: 
    ```json
    {
      "results": [
        {
          "text": "sample text",
          "label": "Scam" or "Not Scam",
          "confidence": 0.95
        }
      ],
      "inference_time": 45.2
    }
    ```

## Usage Examples

### 1. Login Flow

```bash
# Visit the login page
curl -L http://localhost:5000/login

# Or visit directly in browser
open http://localhost:5000/login
```

### 2. Predict Scam Content

```bash
# After authentication, make predictions
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -H "Cookie: session=your-session-cookie" \
  -d '{"texts": ["This is a legitimate message", "You have won $1000! Click here!"]}'
```

### 3. Logout

```bash
curl -L http://localhost:5000/logout
```

## Project Structure

```
API/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Frontend template
└── .env                  # Environment variables (create this)
```

## Troubleshooting

### Common Issues

1. **"SUPABASE_URL and SUPABASE_KEY environment variables are required"**
   - Make sure you've set the environment variables correctly
   - Check that your Supabase project URL and key are correct

2. **"Login failed" error**
   - Verify Google OAuth credentials in Supabase dashboard
   - Check that redirect URIs match exactly
   - Ensure Google Cloud Console project has APIs enabled

3. **"Unauthorized" error on /predict**
   - Make sure you're logged in (visit `/login` first)
   - Check that session cookies are being sent

4. **Model loading issues**
   - The app will download the model on first run (~500MB)
   - Ensure you have internet connection for initial setup
   - Model will be cached locally for subsequent runs

### Development Tips

- Use `FLASK_ENV=development` for debug mode
- Check Supabase logs in the dashboard for authentication issues
- Use browser developer tools to inspect network requests
- Test with different text samples to verify scam detection

## Security Notes

- Never commit your `.env` file or hardcode credentials
- Use HTTPS in production
- Regularly rotate your Supabase keys
- Monitor authentication logs in Supabase dashboard

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.