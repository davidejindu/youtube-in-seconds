# 🎬 YouTube In Seconds

AI-powered web app that summarizes YouTube videos into clean, readable bullet points and headings — instantly.

##Demo
https://youtu.be/pcgvxuKzWIc

## 🚀 Features

- 🔗 Paste a YouTube URL and get an instant summary
- 🧠 AI-generated using **Google Gemini API**
- 📄 Export summary as **PDF**
- ⚡ Clean and responsive **TailwindCSS** UI
- 🧼 Safe and styled Markdown rendering with `marked` + `DOMPurify`
- ✅ Handles private/restricted/missing transcripts with error fallback

---

## 🛠️ Tech Stack

- **Frontend:** React + Vite + TailwindCSS
- **Backend:** Flask + YouTube Transcript API + Google Gemini
- **PDF Export:** html2canvas + jsPDF
- **Security:** CORS, DOMPurify, dotenv for API key safety

