css = """
/* ------------------- CHAT CONTAINER ------------------- */
.chat-container {
    display: flex;
    flex-direction: column;
    height: 65vh;
    overflow-y: auto;
    border: 1px solid #ccc;
    padding: 15px;
    border-radius: 10px;
    background-color: #313b4f;
    scroll-behavior: smooth;
    position: relative;
}

.chat-container::-webkit-scrollbar {
    width: 6px;
}
.chat-container::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 4px;
}
.chat-container::-webkit-scrollbar-track {
    background: #222;
}

/* ------------------- CHAT MESSAGE ------------------- */
.chat-message {
    display: flex;
    align-items: center;
    max-width: 80%;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 12px;
    word-wrap: break-word;
}

/* Message */
.chat-message.user {
    background-color: #2b313e;
    align-self: flex-end;
}
.chat-message.bot {
    background-color: #475063;
    align-self: flex-start;
}

/* Avatar */
.chat-message .avatar {
    flex-shrink: 0;
    align-self: self-start;
}
.chat-message .avatar img {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
}

/* Text */
.chat-message .message {
    padding: 0 15px;
    color: #fff;
    flex: 1;
    max-width: 100%;
    overflow-wrap: break-word;
}

/* ------------------- USER MESSAGE ------------------- */
.user_message {
    position: fixed;
    bottom: 10px;
    left: 50%;
    transform: translateX(-50%);
    width: 60%;
    background: #fff;
    padding: 12px;
    border-radius: 10px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
}
"""


# ------------------ TEMPLATE CHAT ------------------
bot_message_element = """
<div class="chat-message bot">
  <div class="avatar">
    <img
      src="https://i.ibb.co/svsZL9Y8/Bot.jpg"
      alt="Bot Avatar"
    />
  </div>
  <div class="message">{{MSG}}</div>
</div>
"""

user_message_element = """
<div class="chat-message user">
  <div class="avatar">
    <img 
      src="https://i.ibb.co/Vnd47sp/User.jpg"
      alt="User Avatar"
    />
  </div>
  <div class="message">{{MSG}}</div>
</div>
"""
