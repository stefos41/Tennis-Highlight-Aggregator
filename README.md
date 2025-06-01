# 🎾 Tennis Highlights Manager

*A full-stack application for discovering, saving, and managing tennis highlight videos from YouTube.*

---

## 📌 Table of Contents
- [Features](#-features)
- [Demo](#-demo)
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

## 🎥 Demo
**Chrome Extension**  
![Extension Demo](https://via.placeholder.com/400x200?text=Chrome+Extension+Demo)

**Streamlit Dashboard**  
![Dashboard Demo](https://via.placeholder.com/400x200?text=Streamlit+Dashboard)

*Replace with actual screenshots or GIFs in your repo!*

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

**Example Request**:
```bash
curl -X GET "http://localhost:8000/video-info?url=https://youtu.be/example" \
  -H "api-key: valid-key"
```

---

## 🚀 Future Improvements
- **User Authentication** – Replace API keys with OAuth/JWT.
- **Advanced Search** – Filter highlights by player/tournament.
- **Deployment** – Dockerize + deploy on AWS/GCP.
- **Mobile App** – React Native companion app.

---

## 📜 License
MIT © [Your Name]

**Let’s connect!**  
[LinkedIn] | [Portfolio] | [Email]

*Replace placeholders with your info!*

---

🎉 Enjoy curating your tennis highlights!  
*Star ⭐ the repo if you find it useful!*

---

### Credits
- Icons by [Flaticon](https://www.flaticon.com).
- Inspired by [SportsHub](https://example.com). *(Customize!)*

---

This `README.md` is **comprehensive yet concise**, highlighting:  
1. **Functionality** (Features/Demo)  
2. **Technical Depth** (Stack/Endpoints)  
3. **Setup Guide** (Installation/Structure)  
4. **Future Vision** (Roadmap)  

**Tip**: Add screenshots/GIFs to make it visually appealing! 🖼️
