from turtle import title

from flask import Flask, render_template, request, jsonify
import uuid

from utils.groq_service import get_ai_response

from utils.database import (
    initialize_database,
    save_message,
    load_conversation,
    load_messages,
    get_conversation_list,
    create_chat_session,
    rename_chat,
    delete_chat,
    update_chat_title,
    get_chat_title
)

app = Flask(__name__)

current_conversation_id = str(uuid.uuid4())


@app.route("/")
def home():
    return render_template("index.html")


# ==========================
# Load Conversation
# ==========================

@app.route("/conversation/<conversation_id>")
def conversation(conversation_id):

    messages = load_messages(conversation_id)

    result = []

    for row in messages:
        result.append({
            "role": row["role"],
            "message": row["message"]
        })

    return jsonify(result)


# ==========================
# Sidebar History
# ==========================

@app.route("/history")
def history():

    conversations = get_conversation_list()

    history = []

    for conv in conversations:

        history.append({

            "conversation_id": conv["conversation_id"],

            "title": conv["title"]

        })

    return jsonify(history)


# ==========================
# Chat
# ==========================

@app.route("/chat", methods=["POST"])
def chat():

    global current_conversation_id

    data = request.get_json()

    conversation_id = data.get("conversation_id")

    if conversation_id:
        current_conversation_id = conversation_id

    user_message = data.get("message")

    title = get_chat_title(current_conversation_id)

    if title and title["title"] == "New Chat":

        new_title = user_message.strip()

        if len(new_title) > 35:
            new_title = new_title[:35] + "..."

        update_chat_title(
            current_conversation_id,
            new_title
        )

    save_message(
        current_conversation_id,
        "user",
        user_message
    )

    history = load_conversation(current_conversation_id)

    messages = []

    for row in history:
        messages.append({
            "role": row["role"],
            "content": row["message"]
        })

    ai_reply = get_ai_response(messages)

    save_message(
        current_conversation_id,
        "assistant",
        ai_reply
    )

    return jsonify({
        "reply": ai_reply
    })


# ==========================
# New Chat
# ==========================

@app.route("/new-chat", methods=["POST"])
def new_chat():

    global current_conversation_id

    current_conversation_id = str(uuid.uuid4())

    create_chat_session(
        current_conversation_id,
        "New Chat"
    )

    return jsonify({
        "status": "success",
        "conversation_id": current_conversation_id
    })


# ==========================
# Rename Chat
# ==========================

@app.route("/rename-chat", methods=["POST"])
def rename_chat_route():

    data = request.get_json()

    rename_chat(
        data["conversation_id"],
        data["title"]
    )

    return jsonify({
        "status": "success"
    })


# ==========================
# Delete Chat
# ==========================

@app.route("/delete-chat", methods=["POST"])
def delete_chat_route():

    data = request.get_json()

    delete_chat(
        data["conversation_id"]
    )

    return jsonify({
        "status": "success"
    })


# ==========================
# Main
# ==========================

if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)