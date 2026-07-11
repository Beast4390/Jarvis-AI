# 🤖 Jarvis AI Chatbot

A modern AI-powered chatbot built using **Flask**, **Groq API**, **SQLite**, **HTML**, **CSS**, and **JavaScript**. Jarvis provides an interactive conversational experience with persistent chat history, Markdown rendering, and chat management features.

---

## 🚀 Features

- 💬 AI-powered conversations using Groq LLM
- 📝 Markdown support (Headings, Lists, Tables, Code Blocks)
- 📂 Multiple chat sessions
- 🕒 Persistent chat history using SQLite
- ✏️ Rename chat sessions
- 🗑️ Delete chat sessions
- ➕ Create new conversations
- 📱 Responsive modern UI
- ⚡ Fast Flask backend
- 💾 Local database storage
- 🎨 Clean and professional interface

---

## 🛠️ Tech Stack

### Backend
- Python
- Flask
- Groq API
- SQLite

### Frontend
- HTML5
- CSS3
- JavaScript

### Database
- SQLite

### Libraries
- Marked.js (Markdown Rendering)

---

## 📁 Project Structure

```
Jarvis-AI/
│
├── app.py
├── requirements.txt
├── README.md
│
├── database/
│   └── chatbot.db
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   └── script.js
│   │
│   └── images/
│
├── templates/
│   └── index.html
│
└── utils/
    ├── database.py
    └── groq_service.py
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/Jarvis-AI.git
```

```bash
cd Jarvis-AI
```

---

### Create Virtual Environment

Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Create Environment File

Create a file named

```
.env
```

Add your Groq API Key

```env
GROQ_API_KEY=YOUR_API_KEY_HERE
```

---

### Run Application

```bash
python app.py
```

Open

```
http://127.0.0.1:5000
```

## ✨ Supported Markdown

Jarvis can render

- Headings
- Bold Text
- Italic Text
- Lists
- Tables
- Blockquotes
- Code Blocks
- Links

