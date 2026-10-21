from openai import AuthenticationError, RateLimitError, APIConnectionError, APIStatusError
from langchain_core.messages import SystemMessage
from init import chat

SYSTEM_PROMPT = (
    "You are a helpful, concise assistant. "
    "Answer clearly and say so if you don't know something instead of guessing."
)


class ChatError(Exception):
    """A user-friendly error message for a failed model call."""


def ask(session, question):
    session.add_user_message(question)
    system_message = SystemMessage(content=f"{SYSTEM_PROMPT} The user's name is {session.user_name}.")
    try:
        response = chat.invoke([system_message] + session.recent_history())
    except AuthenticationError as exc:
        session.discard_last_message()
        raise ChatError("Authentication failed. Check AZURE_API_KEY in config/.env.") from exc
    except RateLimitError as exc:
        session.discard_last_message()
        raise ChatError("Rate limit reached. Wait a moment and try again.") from exc
    except APIConnectionError as exc:
        session.discard_last_message()
        raise ChatError("Cannot reach the endpoint. Check your network or VPN.") from exc
    except APIStatusError as exc:
        session.discard_last_message()
        raise ChatError(f"API error {exc.status_code}: {exc.message}") from exc
    session.add_ai_message(response.content)
    return response.content