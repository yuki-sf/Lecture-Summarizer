# 🧠 AI Lecture Summarizer

![Streamlit](https://img.shields.io/badge/Streamlit-App-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-yellowgreen)
![GitHub last commit](https://img.shields.io/github/last-commit/yuki-sf/Lecture-Summarizer)

Welcome to **AI Lecture Summarizer** — your handy study buddy that magically condenses YouTube lectures and online articles into crisp, clear summaries! 🚀

Powered by [Streamlit](https://streamlit.io/) and Hugging Face’s cutting-edge AI, this app helps you absorb knowledge faster and smarter. Whether you want to catch up on a long video or skim through a dense article, this tool has your back!

---

## 🎥 Demo

![Demo GIF](https://media.giphy.com/media/3o7aD4j2HVhij0M6pW/giphy.gif)  

---

## 🎉 Features that make learning fun & easy

- 🎥 **YouTube Video Summarization**  
  Paste a YouTube URL and get a neat summary of the lecture (transcripts permitting).

- 📄 **Article Summarization**  
  Drop in any online article link and get a concise breakdown.

- 💬 **Chat-style Interface**  
  Interact with your summaries in a conversation-like flow, with message history saved for seamless review.

- ☁️ **Cloud-Ready & Deployable**  
  Easily run it locally or deploy on AWS, Streamlit Cloud, or your favorite platform.

---

## 🚀 Quick Start Guide

### 1. Clone this repo

```bash
git clone https://github.com/yuki-sf/Lecture-Summarizer.git
cd Lecture-Summarizer
```
### 2. Set up your Python environment
```bash
python -m venv venv
source venv/bin/activate   # Windows users: venv\Scripts\activate
pip install -r requirements.txt
```
### 3. Get your Hugging Face API token
Head over to Hugging Face tokens, create a new token, and add it to a .env file:
```ini
HUGGINGFACEHUB_API_TOKEN=your_hf_api_token_here
```
### 4. Run the app
```bash
streamlit run main.py
```
Open `http://localhost:8501` in your browser and start summarizing!

---


## ⚠️ Heads up about YouTube transcripts
YouTube sometimes blocks transcript requests — especially from cloud servers like AWS or GCP — resulting in errors like:

Could not retrieve a transcript for the video...

### What you can do:
Run the app locally from your own machine’s IP (usually works better)

Use a proxy to mask your IP (check youtube-transcript-api docs)

Summarize articles instead (no transcript issues there!)


## 🤝 Contributing
Got ideas or improvements? Feel free to open issues or submit PRs! Let’s make learning smarter together.


## 📜 License
This project is licensed under the MIT License. Share, learn, and improve freely!

Thanks for stopping by! If this app makes your study sessions easier, a ⭐ on the repo would be amazing! ✨

---
