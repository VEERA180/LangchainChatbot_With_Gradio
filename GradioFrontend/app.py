import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "chatbot"))

import gradio as gr
from userSession import UserSession
from chatService import ask, ChatError

sessions = {}


def respond(message, history, user_name):
    user_name = (user_name or "").strip() or "guest"
    if user_name not in sessions:
        sessions[user_name] = UserSession(user_name)
    try:
        return ask(sessions[user_name], message)
    except ChatError as exc:
        return str(exc)


demo = gr.ChatInterface(
    fn=respond,
    additional_inputs=[gr.Textbox(label="Your name", value="guest")],
    title="Chatbot",
)

if __name__ == "__main__":
    demo.launch()