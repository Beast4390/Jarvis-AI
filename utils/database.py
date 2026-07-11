import sqlite3

DATABASE = "database/chatbot.db"


# ==========================
# Database Connection
# ==========================

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ==========================
# Initialize Database
# ==========================

def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""

    CREATE TABLE IF NOT EXISTS conversations (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        conversation_id TEXT NOT NULL,

        role TEXT NOT NULL,

        message TEXT NOT NULL,

        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

    );

    CREATE TABLE IF NOT EXISTS chat_sessions (

        conversation_id TEXT PRIMARY KEY,

        title TEXT NOT NULL,

        created_at DATETIME DEFAULT CURRENT_TIMESTAMP

    );

    """)

    conn.commit()
    conn.close()


# ==========================
# Create New Chat Session
# ==========================

def create_chat_session(conversation_id, title):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO chat_sessions
        (conversation_id, title)

        VALUES (?, ?)

    """, (conversation_id, title))

    conn.commit()
    conn.close()

def update_chat_title(conversation_id, title):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        UPDATE chat_sessions

        SET title = ?

        WHERE conversation_id = ?

    """, (title, conversation_id))

    conn.commit()

    conn.close()

def get_chat_title(conversation_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT title

        FROM chat_sessions

        WHERE conversation_id = ?

    """, (conversation_id,))

    row = cursor.fetchone()

    conn.close()

    return row




# ==========================
# Save Message
# ==========================

def save_message(conversation_id, role, message):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO conversations
        (conversation_id, role, message)

        VALUES (?, ?, ?)

    """, (conversation_id, role, message))

    conn.commit()
    conn.close()


# ==========================
# Load One Conversation
# ==========================

def load_conversation(conversation_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT role, message

        FROM conversations

        WHERE conversation_id=?

        ORDER BY id ASC

    """, (conversation_id,))

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==========================
# Load Messages (Alias)
# ==========================

def load_messages(conversation_id):

    return load_conversation(conversation_id)


# ==========================
# Chat History
# ==========================

def get_conversation_list():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT
            conversation_id,
            title,
            created_at

        FROM chat_sessions

        ORDER BY created_at DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==========================
# First User Message
# ==========================

def get_first_message(conversation_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT message

        FROM conversations

        WHERE conversation_id=?
        AND role='user'

        ORDER BY id ASC

        LIMIT 1

    """, (conversation_id,))

    row = cursor.fetchone()

    conn.close()

    return row


# ==========================
# All Conversations
# ==========================

def get_all_conversations():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM chat_sessions

        ORDER BY created_at DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==========================
# Rename Chat
# ==========================

def rename_chat(conversation_id, new_title):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        UPDATE chat_sessions

        SET title=?

        WHERE conversation_id=?

    """, (new_title, conversation_id))

    conn.commit()
    conn.close()


# ==========================
# Delete Chat
# ==========================

def delete_chat(conversation_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        DELETE FROM conversations

        WHERE conversation_id=?

    """, (conversation_id,))

    cursor.execute("""

        DELETE FROM chat_sessions

        WHERE conversation_id=?

    """, (conversation_id,))

    conn.commit()
    conn.close()