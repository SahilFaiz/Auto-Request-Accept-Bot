import os
import sqlite3
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Create or connect to the SQLite database
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create users table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY)''')
conn.commit()

pr0fess0r_99 = Client(
    "𝗕𝗼𝘁 𝗦𝘁𝗮𝗿𝘁𝗲𝗱",
    bot_token=os.environ["BOT_TOKEN"],
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"]
)

CHAT_ID = int(os.environ.get("CHAT_ID", None))

# Command handler for broadcasting messages
@pr0fess0r_99.on_message(filters.private & filters.command(["broadcast"]))
async def broadcast_command(client, message):
    # Check if the user sending the command is the owner of the bot
    owner_id = os.environ.get("OWNER_ID", None)
    if owner_id and message.from_user.username == owner_id[1:]:
        # Get the message to broadcast from the command
        broadcast_text = " ".join(message.command[1:])
        
        # Send broadcast message to users who joined the channel
        await send_broadcast_message(client, broadcast_text)

async def send_broadcast_message(client, text):
    # Retrieve user IDs from the database
    c.execute("SELECT id FROM users")
    rows = c.fetchall()
    for row in rows:
        user_id = row[0]
        await client.send_message(user_id, text)
        
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
    print(f"{user.first_name} 𝙹𝙾𝙸𝙽𝙴𝙳 ⚡")  # Logs
    await client.approve_chat_join_request(chat_id=chat.id, user_id=user.id)

    # Insert the user ID into the database
    c.execute("INSERT INTO users (id) VALUES (?)", (user.id,))
    conn.commit()

print("𝗕𝗼𝘁 𝗦𝘁𝗮𝗿𝘁𝗲𝗱")
pr0fess0r_99.run()
