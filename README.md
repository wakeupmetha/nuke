# NUKE ME

## 📋 Навигация / Navigation

- [🇷🇺 Русская версия](#-русская-версия)
- [🇺🇸 English Version](#-english-version)

---

## 🇷🇺 Русская версия

Скрипт для удаления ваших собственных сообщений в чатах Telegram по команде.

### Установка

0.1 УСТАНОВИТЕ PYTHON!

https://www.python.org/downloads/release/python-3133/

И ВЫПОЛНЯЙТЕ ДЕЙСТВИЯ ЧЕРЕЗ VS CODE
- https://code.visualstudio.com/

1. Установите зависимости:
```bash
pip install -r anonim/requirements.txt
```

2. Создайте файл `.env` в корневой директории проекта со следующим содержимым:
```
API_ID=ваш_api_id
API_HASH=ваш_api_hash
PHONE=ваш_телефон_с_+
USER_ID=telegram_user_id
CHAT_IDS=chat_id (где вы хотите удалять сообщения)
```

Для получения `API_ID` и `API_HASH`:
1. Перейдите на https://my.telegram.org
2. Войдите в свой аккаунт
3. Перейдите в "API development tools"
4. Создайте новое приложение
5. Скопируйте `API_ID` и `API_HASH`

Для получения вашего `USER_ID`:
1. Отправьте сообщение боту @userinfobot в Telegram
2. Бот ответит с вашим user ID

### Использование

1. Запустите бота:
```bash
python anonim/nuke.py
```

2. В любом чате, где вы хотите удалить сообщения, отправьте команду:
- `nuke` - удалит все ваши сообщения в чате
- `nuke 100` - удалит последние 100 ваших сообщений в чате

### Важно

- Бот будет работать только с сообщениями пользователя, чей ID указан в переменной `USER_ID` в файле `.env`
- Убедитесь, что у вас есть разрешение на удаление сообщений в чатах
- Используйте с осторожностью, так как удаление сообщений необратимо

---

## 🇺🇸 English Version

A script for deleting your own messages in Telegram chats by command.

### Installation

0.1 INSTALL PYTHON!

https://www.python.org/downloads/release/python-3133/

AND EXECUTE THE ACTIONS VIA VS CODE
- https://code.visualstudio.com/

1. Install dependencies:
```bash
pip install -r anonim/requirements.txt
```

2. Create a `.env` file in the project root directory with the following content:
```
API_ID=your_api_id
API_HASH=your_api_hash
PHONE=your_phone_with_+
USER_ID=telegram_user_id
CHAT_IDS=chat_id (where you want to delete messages)
```

To get `API_ID` and `API_HASH`:
1. Go to https://my.telegram.org
2. Log in to your account
3. Go to "API development tools"
4. Create a new application
5. Copy `API_ID` and `API_HASH`

To get your `USER_ID`, you can:
1. Send a message to @userinfobot on Telegram
2. The bot will reply with your user ID

### Usage

1. Start the bot:
```bash
python anonim/nuke.py
```

2. In any chat where you want to delete messages, send the command:
- `nuke` - will delete all your messages in the chat
- `nuke 100` - will delete the last 100 of your messages in the chat

### Important

- The bot will only work with messages from the user whose ID is specified in the `USER_ID` variable in the `.env` file
- Make sure you have permission to delete messages in the chats
- Use with caution as message deletion is irreversible
```
        