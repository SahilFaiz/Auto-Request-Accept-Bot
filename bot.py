import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import mysql.connector
import time
import csv
import aiohttp

# Function to establish MySQL connection with auto-reconnect
def establish_db_connection():
    while True:
        try:
            mydb = mysql.connector.connect(
                host= ["MYSQL_HOST"],
                port=["MYSQL_PORT"]),
                database=["MYSQL_DATABASE"],
                user="root",
                password=["MYSQL_PASSWORD"]
            )
            print("Connected to MySQL database successfully!")
            return mydb
        except mysql.connector.Error as e:
            print(f"Failed to connect to MySQL database: {e}")
            print("Retrying in 10 seconds...")
            time.sleep(10)

# Get MySQL connection variables from environment variables
MYSQL_DATABASE = os.environ["MYSQL_DATABASE"]
MYSQL_HOST = os.environ["MYSQL_HOST"]
MYSQL_PORT = os.environ["MYSQL_PORT"]
MYSQL_USER = "root"
MYSQL_PASSWORD = os.environ["MYSQL_PASSWORD"]

# Establish MySQL connection
mydb = establish_db_connection()

# Function to retrieve user IDs from the database
def get_user_ids():
    cursor = mydb.cursor()
    cursor.execute("SELECT user_id FROM users")
    rows = cursor.fetchall()
    return [row[0] for row in rows]

# Function to write user IDs to a CSV file
def write_user_ids_to_csv(user_ids):
    with open('user_ids.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["User ID"])
        for user_id in user_ids:
            writer.writerow([user_id])
    print("User IDs have been written to user_ids.csv")

pr0fess0r_99 = Client(
    "𝗕𝗼𝘁 𝗦𝘁𝗮𝗿𝘁𝗲𝗱",
    bot_token=os.environ["BOT_TOKEN"],
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"]
)

CHAT_ID = [int(chat_id) for chat_id in os.environ.get("CHAT_ID", "").split(",")]

# Function to send message with rate limit
async def send_message_with_rate_limit(client, user_id, text, session):
    url = f"https://api.telegram.org/bot{client.token}/sendMessage"
    data = {
        "chat_id": user_id,
        "text": text
    }
    async with session.post(url, data=data) as response:
        if response.status != 200:
            print(f"Failed to send message to user {user_id}: {response.status}")
            return False
        print(f"Broadcasted {user_id} successfully!")
        return True

# Function to broadcast messages to all users
async def broadcast_message(client, text):
    if text.strip():
        # Retrieve user IDs from the database
        cursor = mydb.cursor()
        cursor.execute("SELECT user_id FROM users")
        rows = cursor.fetchall()
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for row in rows:
                user_id = row[0]
                task = send_message_with_rate_limit(client, user_id, text, session)
                tasks.append(task)
            await asyncio.gather(*tasks)
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
        print("You are not the owner")

print("𝗕𝗼𝘁 𝗦𝘁𝗮𝗿𝘁𝗲𝗱")
pr0fess0r_99.run()
