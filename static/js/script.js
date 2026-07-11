const sendBtn = document.getElementById("send-btn");
const newChatBtn = document.getElementById("new-chat-btn");
const inputBox = document.getElementById("message-input");
const chatBox = document.getElementById("chat-box");

let activeConversationId = null;


// =======================
// Event Listeners
// =======================

sendBtn.addEventListener("click", sendMessage);

newChatBtn.addEventListener("click", createNewChat);

inputBox.addEventListener("keypress", function (event) {

    if (event.key === "Enter") {

        sendMessage();

    }

});


// =======================
// Add Message
// =======================

function addMessage(sender, message) {

    const div = document.createElement("div");

    div.className = sender;

    div.innerHTML = `
        <strong>${sender}:</strong>
        <div class="markdown-body">
            ${marked.parse(message)}
        </div>
    `;

    chatBox.appendChild(div);

    chatBox.scrollTop = chatBox.scrollHeight;

}


// =======================
// Send Message
// =======================

async function sendMessage() {

    const message = inputBox.value.trim();

    if (message === "") return;

    const welcome = document.querySelector(".welcome-message");

    if (welcome) {

        welcome.remove();

    }

    addMessage("You", message);

    inputBox.value = "";

    const response = await fetch("/chat", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify({

            message: message,

            conversation_id: activeConversationId

        })

    });

    const data = await response.json();

    addMessage("Jarvis AI", data.reply);

    loadHistory();

}


// =======================
// Load Sidebar
// =======================

async function loadHistory() {

    const response = await fetch("/history");

    const history = await response.json();

    const list = document.getElementById("chat-list");

    list.innerHTML = "";

    history.forEach(chat => {

        const li = document.createElement("li");

        li.className = "chat-item";

        // ---------- title ----------
        const title = document.createElement("span");

        title.innerText = chat.title;

        title.style.cursor = "pointer";

        title.onclick = () => {

            loadConversation(chat.conversation_id);

        };

        // ---------- rename button ----------
        const renameBtn = document.createElement("button");

        renameBtn.innerText = "✏️";

        renameBtn.onclick = async (e) => {

            e.stopPropagation();

            const newTitle = prompt("Rename chat:", chat.title);

            if (!newTitle) return;

            await fetch("/rename-chat", {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify({

                    conversation_id: chat.conversation_id,

                    title: newTitle

                })

            });

            loadHistory();

        };

        // ---------- delete button ----------
        const deleteBtn = document.createElement("button");

        deleteBtn.innerText = "🗑";

        deleteBtn.onclick = async (e) => {

            e.stopPropagation();

            if (!confirm("Delete this chat?")) return;

            await fetch("/delete-chat", {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify({

                    conversation_id: chat.conversation_id

                })

            });

            chatBox.innerHTML = "";

            activeConversationId = null;

            loadHistory();

        };

        li.appendChild(title);

        li.appendChild(renameBtn);

        li.appendChild(deleteBtn);

        list.appendChild(li);

    });

}


// =======================
// Load Conversation
// =======================

async function loadConversation(conversationId) {

    activeConversationId = conversationId;

    const response = await fetch(`/conversation/${conversationId}`);

    const messages = await response.json();

    chatBox.innerHTML = "";

    messages.forEach(msg => {

        if (msg.role === "user") {

            addMessage("You", msg.message);

        }

        else {

            addMessage("Jarvis AI", msg.message);

        }

    });

}


// =======================
// New Chat
// =======================

async function createNewChat() {

    const response = await fetch("/new-chat", {

        method: "POST"

    });

    const data = await response.json();

    activeConversationId = data.conversation_id;

    chatBox.innerHTML = `

        <div class="welcome-message">

            <h2>👋 Hello!</h2>

            <p>I'm <strong>Jarvis</strong>.</p>

            <p>Ask me anything.</p>

        </div>

    `;

    document.getElementById("chat-title").innerText = "New Conversation";

    inputBox.value = "";

    loadHistory();

}


// =======================
// Initial Load
// =======================

loadHistory();

