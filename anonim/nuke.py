import os
import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.messages import DeleteMessagesRequest
from telethon.tl.types import InputPeerUser, InputPeerChannel, InputPeerChat
from dotenv import load_dotenv

load_dotenv()

# Authentication data
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE = os.getenv('PHONE')
CHAT_IDS = [chat_id.strip() for chat_id in os.getenv('CHAT_IDS', '').split(',') if chat_id.strip()]

# get and validate USER_ID
user_id = os.getenv('USER_ID')
if not user_id:
    print("Error: USER_ID is not set in .env file")
    print("Please add your Telegram user ID to .env file")
    print("You can get your ID by sending a message to @userinfobot in Telegram")
    exit(1)

try:
    MY_USER_ID = int(user_id)
except ValueError:
    print(f"Error: USER_ID must be a number, got: {user_id}")
    print("Please check your .env file and make sure USER_ID is correct")
    exit(1)
# number of posts deleted here!!!
BATCH_SIZE = 10

def format_chat_id(chat_id):
    """Formats chat ID into the correct format"""
    try:
        chat_id = int(chat_id)
        if chat_id < 0:
            if abs(chat_id) < 1000000000000:
                return -1000000000000 + abs(chat_id)
            return chat_id
        return chat_id
    except ValueError:
        print(f"Error: Chat ID must be a number, got: {chat_id}")
        return None

async def get_chat_info(client, chat_id):
    try:
        formatted_id = format_chat_id(chat_id)
        if not formatted_id:
            return None
            
        print(f"Trying to get chat information for {formatted_id}")
        
        entity = await client.get_entity(formatted_id)
        
        chat_type = type(entity).__name__
        print(f"Chat type: {chat_type}")
        
        if chat_type == 'Channel':
            return {
                'id': formatted_id,
                'title': entity.title,
                'username': getattr(entity, 'username', None),
                'type': 'Channel'
            }
        elif chat_type == 'Chat':
            return {
                'id': formatted_id,
                'title': entity.title,
                'username': None,
                'type': 'Chat'
            }
        elif chat_type == 'User':
            return {
                'id': formatted_id,
                'title': f"{entity.first_name} {getattr(entity, 'last_name', '')}".strip(),
                'username': getattr(entity, 'username', None),
                'type': 'User'
            }
        else:
            print(f"Unknown chat type: {chat_type}")
            return None
            
    except ValueError as e:
        print(f"Error processing ID {chat_id}: {str(e)}")
        return None
    except Exception as e:
        print(f"Unknown error for ID {chat_id}: {str(e)}")
        print("Error type:", type(e).__name__)
        return None

async def delete_message_batch(client, chat_info, messages):
    """Deletes a batch of messages"""
    try:
        message_ids = [msg.id for msg in messages]
        
        result = await client.delete_messages(
            chat_info['id'],
            message_ids,
            revoke=True
        )
        
        if result:
            print(f"Deleted {len(message_ids)} messages")
            return True
        else:
            print("Failed to delete messages")
            return False
    except Exception as e:
        print(f"Error deleting message batch: {str(e)}")
        print("Error type:", type(e).__name__)
        return False

async def delete_my_messages_in_chat(client, chat_info, message_limit=None):
    try:
        print(f"\n{'='*50}")
        print(f"Starting chat processing: {chat_info['title']}")
        print(f"Chat ID: {chat_info['id']}")
        print(f"Chat type: {chat_info['type']}")
        if chat_info['username']:
            print(f"Chat username: @{chat_info['username']}")
        print(f"{'='*50}")
        
        messages = await client.get_messages(chat_info['id'], from_user=MY_USER_ID, limit=message_limit)
        
        total_messages = len(messages)
        print(f"Found {total_messages} of your messages")
        
        if total_messages == 0:
            print("No messages to delete in this chat")
            return
            
        for i in range(0, total_messages, BATCH_SIZE):
            batch = messages[i:i + BATCH_SIZE]
            print(f"\nProcessing batch {i//BATCH_SIZE + 1}/{(total_messages + BATCH_SIZE - 1)//BATCH_SIZE}")
            
            success = await delete_message_batch(client, chat_info, batch)
            
            if not success:
                print("Trying to delete messages one by one...")
                for msg in batch:
                    try:
                        result = await client.delete_messages(
                            chat_info['id'],
                            [msg.id],
                            revoke=True
                        )
                        if result:
                            print(f"Deleted message {msg.id}")
                        else:
                            print(f"Failed to delete message {msg.id}")
                    except Exception as e:
                        print(f"Error deleting message {msg.id}: {str(e)}")
            
            if i + BATCH_SIZE < total_messages:
                print(f"Waiting 10 seconds before next batch...")
                await asyncio.sleep(10)
            
        print(f"\n{'='*50}")
        print(f"Deletion process completed in chat {chat_info['title']}")
        print(f"{'='*50}")
        
    except Exception as e:
        print(f"Error processing chat {chat_info['id']}: {str(e)}")
        print("Error type:", type(e).__name__)

async def handle_nuke_command(event):
    """Handler for the nuke command"""
    try:
        if event.sender_id != MY_USER_ID:
            return
            
        message_text = event.message.text.lower()
        
        if not message_text.startswith('nuke'):
            return
            
        # Parse message count
        parts = message_text.split()
        message_limit = None
        
        if len(parts) > 1:
            try:
                message_limit = int(parts[1])
            except ValueError:
                await event.reply("Invalid command format. Use: nuke [count]")
                return
        
        # Get chat information
        chat_info = await get_chat_info(event.client, event.chat_id)
        if not chat_info:
            await event.reply("Failed to get chat information")
            return
            
        await event.message.delete()
        
        await delete_my_messages_in_chat(event.client, chat_info, message_limit)
        
    except Exception as e:
        print(f"Error handling nuke command: {str(e)}")

async def main():
    print(r"""
        _   ___  ____  _  __ ______
       / | / / / / / / / / //_/ ____/
      /  |/ / / / / / / / ,< / __/   
     / /|  / /_/ / /_/ / /| / /___   
    /_/ |_/\____/\____/_/ |_/_____/   
                                     
        ______________________   ____________________    ___    __  ___
       /_  __/ ____/ /   / ____/ / ____/ __ \   /   |  /   |  /  |/  /
        / / / __/ / /   / __/   / / __/ /_/ /  / /| | / /| | / /|_/ / 
       / / / /___/ /___/ /___  / /_/ / _, _/  / ___ |/ ___ |/ /  / /  
      /_/ /_____/_____/_____/  \____/_/ |_|  /_/  |_/_/  |_/_/  /_/   
                                                                     
        ____  ____  ______
       / __ )/ __ \/_  __/
      / __  / / / / / /   
     / /_/ / /_/ / / /    
    /_____/\____/ /_/     
    """)
    
    # create client
    client = TelegramClient('anon', API_ID, API_HASH)
    
    try:
        # connect to Telegram
        await client.start(phone=PHONE)
        print("Successfully connected to Telegram")
        
        @client.on(events.NewMessage(pattern=r'^nuke\s*\d*$'))
        async def nuke_handler(event):
            await handle_nuke_command(event)
        
        print("\nBot is running and waiting for 'nuke' command in chats")
        print("Use command 'nuke [count]' to delete messages")
        print("Example: nuke 100 - will delete the last 100 messages")
        print("nuke without parameters will delete all messages")
        
        await client.run_until_disconnected()
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Error type:", type(e).__name__)
    finally:
        await client.disconnect()

if __name__ == "__main__":
    if not CHAT_IDS:
        print("Error: No chat IDs specified in .env file")
    else:
        asyncio.run(main())