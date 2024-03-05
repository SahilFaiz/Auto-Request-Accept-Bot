import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import mysql.connector
import time

# Get MySQL connection variables from environment variables
MYSQL_DATABASE = os.environ["MYSQL_DATABASE"]
MYSQL_HOST = os.environ["MYSQLHOST"]
MYSQL_PORT = os.environ["MYSQLPORT"]
MYSQL_USER = "root"
MYSQL_PASSWORD = os.environ["MYSQLPASSWORD"]

# Establish MySQL connection
mydb = mysql.connector.connect(
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    database=MYSQL_DATABASE,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD
)

pr0fess0r_99 = Client(
    "𝗕𝗼𝘁 𝗦𝘁𝗮𝗿𝘁𝗲𝗱",
    bot_token=os.environ["BOT_TOKEN"],
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"]
)

CHAT_ID = [int(chat_id) for chat_id in os.environ.get("CHAT_ID", "").split(",")]

# Function to send messages with rate limiting
async def send_message_with_rate_limit(client, user_id, text):
    try:
        await client.send_message(user_id, text)
        print(f"Broadcasted {user_id} Sucessfully!!!!!")
    except Exception as e:
        print(f"Failed to send message to user {user_id}: {e}")

# Function to broadcast messages to all users
async def broadcast_message(client, text):
    if text.strip():
        # Retrieve user IDs from the database
        cursor = mydb.cursor()
        cursor.execute("SELECT user_id FROM users")
        rows = cursor.fetchall()

        # Batch messages to avoid hitting limits
        batch_size = 30  # Max messages per batch
        for i in range(0, len(rows), batch_size):
            batch = rows[i:i + batch_size]
            for row in batch:
                user_id = (row[0])
                await send_message_with_rate_limit(client, user_id, text)
                time.sleep(1)  # Rate limit: 1 message per second

    else:
        print("Empty message. Skipping broadcast.")

# Command handler for broadcasting messages
@pr0fess0r_99.on_message(filters.private & filters.command(["broadcast"]))
async def broadcast_command(client, message):
    # Check if the user sending the command is the owner of the bot
    owner_id = os.environ.get("OWNER_ID", None)
    if owner_id and message.from_user.username == owner_id[1:]:
        # Get the message to broadcast from the command
        broadcast_text = " ".join(message.command[1:])

        # Send broadcast message to users who joined the channel
        await broadcast_message(client, broadcast_text)
    else:
        print("u r not owner")
        
@pr0fess0r_99.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    approvedbot = await client.get_me() 
    button=[
        [InlineKeyboardButton("𝚂𝚄𝙿𝙿𝙾𝚁𝚃", url="https://t.me/Prime_SaversBot")]
    ]
    await message.reply_text(text="**𝙷𝙴𝙻𝙻𝙾...⚡\n\n𝙸𝙰𝙼 𝙰 𝚂𝙸𝙼𝙿𝙻𝙴 𝚃𝙴𝙻𝙴𝙶𝚁𝙰𝙼 𝙰𝚄𝚃𝙾 𝚁𝙴𝚀𝚄𝙴𝚂𝚃 𝙰𝙲𝙲𝙴𝙿𝚃 𝙱𝙾𝚃.", reply_markup=InlineKeyboardMarkup(button), disable_web_page_preview=True)

@pr0fess0r_99.on_chat_join_request(filters.chat(CHAT_ID))
async def autoapprove(client, message):
    chat = message.chat  # Chat
    user = message.from_user  # User
    if chat.id in CHAT_ID:  # Check if the join request is from any of the specified chat IDs
        print(f"{user.first_name} 𝙹𝙾𝙸𝙽𝙴𝙳 ⚡")  # Logs
        await client.approve_chat_join_request(chat_id=chat.id, user_id=user.id)

        # Check if the user ID already exists in the database
        cursor = mydb.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user.id,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            print(f"User {user.id} already exists in the database.")
        else:
            # Insert the user ID into the database
            cursor.execute("INSERT INTO users (user_id) VALUES (%s)", (user.id,))
            mydb.commit()

print("𝗕𝗼𝘁 𝗦𝘁𝗮𝗿𝘁𝗲𝗱")
pr0fess0r_99.run()
