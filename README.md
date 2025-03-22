# NukeTG - Telegram Message Deletion Bot

A bot for deleting your own messages in Telegram chats by command.

## Installation

1. Install dependencies:
```bash
pip install -r anonim/requirements.txt
```

2. Create a `.env` file in the project root directory with the following content:
```
API_ID=your_api_id
API_HASH=your_api_hash
PHONE=your_phone_number
CHAT_IDS=chat_id1,chat_id2,chat_id3
```

To get `API_ID` and `API_HASH`:
1. Go to https://my.telegram.org
2. Log in to your account
3. Go to "API development tools"
4. Create a new application
5. Copy `API_ID` and `API_HASH`

## Usage

1. Start the bot:
```bash
python anonim/nuke.py
```

2. In any chat where you want to delete messages, send the command:
- `nuke` - will delete all your messages in the chat
- `nuke 100` - will delete the last 100 of your messages in the chat

## Important

- The bot will only work with messages from the user whose ID is specified in the `MY_USER_ID` variable in the `nuke.py` file
- Make sure you have permission to delete messages in the chats
- Use with caution as message deletion is irreversible 