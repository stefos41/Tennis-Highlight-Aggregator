https://github.com/user-attachments/assets/7d904a1c-11bc-4b1d-a74f-d7f9fa6a9907


# 🎾 Tennis Highlights Aggregator

*A full-stack application for discovering, saving, and managing tennis highlight videos from YouTube.*

---

## 📌 Table of Contents
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Project Structure](#-project-structure)
- [API Endpoints](#-api-endpoints)
- [Future Improvements](#-future-improvements)

---

## ✨ Features
✅ **Chrome Extension** – One-click saving of YouTube tennis highlights.  
📊 **Streamlit Dashboard** – Browse, add, or delete highlights with a clean UI.  
🎥 **Highlight of the Day** – Randomly picks a featured video daily.  
🔒 **Secure API** – FastAPI backend with API key authentication.  
📦 **Database Integration** – HarperDB stores video metadata.

---

## 🛠 Tech Stack
| Component           | Technology                        |
|---------------------|-----------------------------------|
| **Frontend**        | Streamlit, HTML/CSS (Chrome Ext.) |
| **Backend**         | FastAPI (Python)                  |
| **Database**        | HarperDB (NoSQL)                  |
| **YouTube Integration** | `yt-dlp`                     |
| **Deployment**      | Local (Docker support planned)    |

---

## ⚙️ Installation

### 1. Backend (FastAPI)
```bash
# Clone the repo
git clone https://github.com/your-username/tennis-highlights.git
cd tennis-highlights

# Install dependencies
pip install -r requirements.txt  # Create one if missing!

# Run the FastAPI server
uvicorn api:app --reload
```
**Access API docs**: http://localhost:8000/docs

### 2. Streamlit Dashboard
```bash
streamlit run app.py
```
**Dashboard URL**: http://localhost:8501

### 3. Chrome Extension
1. Go to `chrome://extensions`.
2. Enable **Developer Mode**.
3. Click **Load Unpacked** and select the extension folder.

---

## 📂 Project Structure
```bash
.
├── backend/                # FastAPI server
│   ├── api.py              # REST endpoints
│   ├── database_service.py # DB operations
│   └── yt_extractor.py     # YouTube metadata fetcher
├── frontend/               # Streamlit app
│   └── app.py              # Dashboard UI
├── chrome-extension/       # Browser add-on
│   ├── manifest.json       # Extension config
│   ├── popup.js            # Extension logic
│   └── popup.html          # UI
└── config.py               # Environment variables
```

---

## 🔌 API Endpoints
| Endpoint         | Method | Description                                   |
|------------------|--------|-----------------------------------------------|
| `/video-info`    | GET    | Fetches YouTube video metadata (title, etc.)  |
| `/add-highlight` | POST   | Saves a highlight to the database             |

---

## 🚦 To Run
1. make sure you add your cloud harperedb url, username, and password into the correct areas
2. Select the developer mode in manage extensions and add the chrome extension folder from the repositorie into "load unpacked" 
3. Run the api.py folder
4. Lastly run the app.py folder and the streamlit webpage will pop up
5. Now the chrome extension is sinked with the webpage and highlights can be added

---

## 🚀 Future Improvements
- **User Authentication** – Replace API keys with OAuth/JWT.
- **Advanced Search** – Filter highlights by player/tournament.
- **Deployment** – Dockerize + deploy on AWS/GCP.
- **Mobile App** – React Native companion app.

---

**Let’s connect!**  
[LinkedIn Profile](https://www.linkedin.com/in/stefan-spatariu-b03bb7369/?trk=opento_sprofile_topcard)
stef.spat4@outlook.com


---

🎉 Enjoy curating your tennis highlights!  
*Star ⭐ the repo if you find it useful!*

---
