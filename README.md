# Langchain Chatbot

A chatbot built with LangChain and Azure OpenAI. It runs in the console or as a Gradio web app, keeps a separate conversation per user, and saves each conversation to disk so the bot remembers it after a restart.

## Features

- Azure OpenAI chat through `langchain-openai`
- Console interface and Gradio web interface sharing the same chat logic
- Per-user sessions with a unique session ID
- Persistent memory: each user's conversation is stored as JSON in `memory/`
- Only the most recent messages are sent to the model (default 20); the full history stays on disk
- System prompt that sets the bot's behaviour and tells it the user's name
- Handled errors: missing config, missing values, authentication, rate limit, connection and API errors, Ctrl+C

## Project structure

```
Langchain_chatbot_v1/
├── chatbot/                  Core code and console app
│   ├── main.py               Console entry point
│   ├── sendingMessage.py     Console chat loop
│   ├── chatService.py        ask(): calls the model, converts API errors to ChatError
│   ├── userSession.py        UserSession: user name, session ID, message history
│   ├── Memory.py             Loads and saves history as JSON
│   ├── init.py               Creates the AzureChatOpenAI client
│   └── librariesAndClass.py  Imports, loads and validates config/.env
├── GradioFrontend/
│   └── app.py                Gradio web interface
├── config/
│   └── .env                  Azure settings and API key (not committed)
├── memory/                   Saved conversations, one JSON file per user (not committed)
├── Requirements.txt
└── .gitignore
```

## Requirements

- Python 3.12
- An Azure OpenAI deployment with its endpoint, API key and API version

## Setup

1. Create and activate a virtual environment:

   ```powershell
   python -m venv LangChatbot
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
   .\LangChatbot\Scripts\Activate.ps1
   ```

2. Install the dependencies:

   ```powershell
   pip install -r Requirements.txt
   ```

3. Create `config/.env` with your Azure settings:

   ```
   AZURE_API_KEY=your-api-key
   AZURE_ENDPOINT=https://your-endpoint
   AZURE_DEPLOYMENT_NAME=your-deployment-name
   AZURE_API_VERSION=2024-06-01
   ```

   All four values are required. The app stops with a clear message if the file or any value is missing.

## Usage

### Console

```powershell
cd chatbot
python main.py
```

Enter your name, then chat. Type `exit` or `quit` to leave, or press Ctrl+C.

### Web (Gradio)

```powershell
cd GradioFrontend
python app.py
```

Open http://127.0.0.1:7860. Use the "Your name" box to choose whose memory is used. Changing the name switches to that user's conversation.

## How memory works

- Each user name maps to one file: `memory/<name>.json`. Characters other than letters, digits, `_` and `-` are replaced with `_`.
- The file is updated after every AI reply, so a failed request never leaves an unanswered question saved.
- When a user returns, the saved history is loaded and the model sees the last 20 messages.
- Delete a user's JSON file to reset that user's memory.
- In the web app, earlier messages are not shown in the chat window, but the model still uses them.

## Configuration

| Setting | Where | Default |
|---|---|---|
| Reply length limit | `max_completion_tokens` in `chatbot/init.py` | 500 |
| Retries / timeout | `max_retries`, `timeout` in `chatbot/init.py` | 3 / 30 s |
| Temperature / top_p | `chatbot/init.py` | 0.7 / 0.9 |
| Messages sent to the model | `recent_history(limit=20)` in `chatbot/userSession.py` | 20 |
| Bot role and tone | `SYSTEM_PROMPT` in `chatbot/chatService.py` | General assistant |

## Troubleshooting

| Message | Cause and fix |
|---|---|
| `Configuration file not found` | `config/.env` is missing. Create it as shown in Setup. |
| `Missing values in ...: AZURE_API_KEY` | A value in `config/.env` is empty or missing. |
| `Authentication failed` | The API key is wrong or expired. |
| `Cannot reach the endpoint` | Check the network or VPN, and the `AZURE_ENDPOINT` value. |
| `API error 404` | Check `AZURE_DEPLOYMENT_NAME` and `AZURE_API_VERSION`. |
| `Rate limit reached` | Wait a moment and try again. |
| `Import "chatService" could not be resolved` in the editor | Editor-only warning for `GradioFrontend/app.py`. Add `"python.analysis.extraPaths": ["./chatbot"]` to `.vscode/settings.json`. |

## Security

- Never commit `config/.env`. It is listed in `.gitignore`, along with `memory/`.
- Rotate the API key if it has been shared or committed.
- Do not use `share=True` in `demo.launch()` unless you want the app on a public URL. Anyone who can reach the app can read any user's memory by typing that name.
