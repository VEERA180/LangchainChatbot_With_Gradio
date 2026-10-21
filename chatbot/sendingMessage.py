# 4. Ask questions in a loop until the user types 'exit'
from userSession import UserSession
from chatService import ask, ChatError

user_name = input("Enter your name: ").strip() or "guest"
session = UserSession(user_name)
print(f"Hello {session.user_name}! Session {session.session_id}")
print("Chatbot is ready. Type 'exit' to quit")
while True:
    question = input("You :").strip()
    if question.lower() in ("exit","quit"):
        print("Good bye....\n")
        break
    if not question:
        print("Please type a question.\n")
        continue
    try:
        reply = ask(session, question)
    except ChatError as exc:
        print(f"{exc}\n")
        continue
    print(f"AI Response :{reply}\n")