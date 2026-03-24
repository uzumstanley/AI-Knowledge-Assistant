# Deployment Guide - AI Knowledge Assistant (100% Free)

This guide walks you through deploying your app using completely free services.

## Architecture Overview

```
┌─────────────────────────┐
│   Streamlit Cloud       │  Frontend (Free)
│   (Streamlit App)       │
└────────────┬────────────┘
             │ HTTP requests
             ▼
┌─────────────────────────┐
│   Render.com            │  Backend (Free)
│   (FastAPI + Uvicorn)   │
└────────────┬────────────┘
             │ API calls
             ▼
┌─────────────────────────┐
│   Hugging Face API      │  LLM (Free tier)
│   (OpenAI-compatible)   │
└─────────────────────────┘
```

---

## Prerequisites

- GitHub account (free)
- Streamlit Cloud account (free) 
- Render.com account (free)
- Hugging Face account with API key (free)

---

## Part 1: Prepare Your Code (Already Done ✓)

These files have been created/updated:
- ✓ `.streamlit/config.toml` - Streamlit configuration
- ✓ `Procfile` - Render deployment configuration
- ✓ `.gitignore` - Prevent uploading sensitive files

---

## Part 2: Set Up GitHub Repository

1. **Initialize Git** (if not already done):
   ```bash
   cd /Users/mac/Desktop/AI\ Knowledge\ Assistant
   git init
   git add .
   git commit -m "Initial commit: AI Knowledge Assistant"
   ```

2. **Create a GitHub Repository**:
   - Go to [github.com](https://github.com) and sign in
   - Click **New Repository**
   - Name it: `AI-Knowledge-Assistant`
   - Add description: "RAG-based PDF Q&A with Streamlit + FastAPI"
   - Click **Create repository**

3. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/AI-Knowledge-Assistant.git
   git branch -M main
   git push -u origin main
   ```
   (Replace `YOUR_USERNAME` with your GitHub username)

---

## Part 3: Deploy Backend on Render.com

### Step 1: Create Render Account
- Go to [render.com](https://render.com)
- Sign up with GitHub (easiest)
- Connect your GitHub account when prompted

### Step 2: Deploy FastAPI Backend
1. Click **+ New** → **Web Service**
2. Select your `AI-Knowledge-Assistant` repository
3. Fill in the form:
   - **Name**: `ai-assistant-backend`
   - **Environment**: `Python 3.14`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Click **Advanced** and add **Environment Variables**:
   ```
   HUGGINGFACE_API_KEY = your_hf_api_key_here
   HUGGINGFACE_API_URL = https://router.huggingface.co/v1/chat/completions
   HUGGINGFACE_API_MODEL = openai/gpt-oss-120b:fastest
   ```
5. Click **Create Web Service**
6. Wait ~5-10 minutes for deployment
7. **Copy the service URL** (e.g., `https://ai-assistant-backend.onrender.com`)

---

## Part 4: Deploy Frontend on Streamlit Cloud

### Step 1: Create Streamlit Cloud Account
- Go to [share.streamlit.io](https://share.streamlit.io)
- Click **Sign up** → **Sign up with GitHub**
- Authorize Streamlit to access your GitHub

### Step 2: Deploy Streamlit App
1. Click **New app**
2. Select:
   - Repository: `YOUR_USERNAME/AI-Knowledge-Assistant`
   - Branch: `main`
   - Main file path: `app.py`
3. Click **Deploy**

### Step 3: Add Backend URL
1. Once deployed, go to your Streamlit app URL
2. Click the **☰** menu (top right) → **Settings** → **Secrets**
3. Add this secret:
   ```
   API_BASE_URL="https://ai-assistant-backend.onrender.com"
   ```
   (Replace with your Render backend URL from Part 3)
4. Save and refresh the app

---

## Part 5: Get Hugging Face API Key (Free)

1. Go to [huggingface.co](https://huggingface.co)
2. Sign up if needed
3. Click your **profile** → **Settings** → **Access Tokens**
4. Click **New token** → **Generate a token**
   - Name: `ai-assistant-token`
   - Type: `read`
5. Copy the token
6. Add it to **both Render and Streamlit Cloud** environment variables

---

## Part 6: Test Your Deployment

1. Open your Streamlit app URL (from Streamlit Cloud dashboard)
2. **Upload a PDF** - You should see "Uploaded successfully!"
3. **Ask a question** - The backend should respond with an answer
4. If you get an error, check:
   - Backend URL is correct in Streamlit Secrets
   - Hugging Face API key is valid
   - Render backend is running (check logs)

---

## Important Notes

### Free Tier Limitations:
- **Render**: Auto-spins down after 15 mins of inactivity (cold start ~30 sec)
- **Streamlit Cloud**: Deploys automatically on GitHub push, unlimited apps
- **Hugging Face**: Limited API calls per day on free tier

### To Keep Backend Alive (Optional - Still Free):
If you want to prevent cold starts, you can:
1. Use Render's free tier with a monitoring service (e.g., uptimerobot.com)
2. Or use PythonAnywhere instead of Render (slightly better free tier)

### Environment Variables Location:
- **Render**: Dashboard → Service → Settings → Environment
- **Streamlit Cloud**: App Settings → Secrets

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Connection refused" | Backend cold-start. Wait 30 sec and retry. |
| "Invalid API key" | Check HUGGINGFACE_API_KEY in both platforms |
| Upload fails | Ensure backend URL in Streamlit Secrets is correct |
| App crashes | Check Render backend logs for Python errors |

---

## Making Updates

After deployment, whenever you update your code:

```bash
git add .
git commit -m "Update description"
git push origin main
```

Both Render and Streamlit Cloud will automatically redeploy from GitHub!

---

## Next Steps

- Monitor logs: Render dashboard → Logs tab
- Scale up if needed (paid plans available)
- Add authentication for production
- Optimize PDF processing for better performance

