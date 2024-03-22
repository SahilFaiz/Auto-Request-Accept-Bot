from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup,Message
import mysql.connector
import asyncio ,os,random

def establish_db_connection():
    while True:
        try:
            mydb = mysql.connector.connect(
                host=MYSQL_HOST,
                port=MYSQL_PORT,
                database=MYSQL_DATABASE,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD
            )
            print("Connected to MySQL database successfully!")
            return mydb
        except mysql.connector.Error as e:
            print(f"Failed to connect to MySQL database: {e}")
            print("Retrying in 10 seconds...")
            asyncio.sleep(10)

MYSQL_DATABASE = os.environ["MYSQL_DATABASE"]
MYSQL_HOST = os.environ["MYSQLHOST"]
MYSQL_PORT = os.environ["MYSQLPORT"]
MYSQL_USER = "root"
MYSQL_PASSWORD = os.environ["MYSQLPASSWORD"]
mydb = establish_db_connection()

pr0fess0r_99 = Client(
    "𝗕𝗼𝘁 𝗦𝘁𝗮𝗿𝘁𝗲𝗱",
    bot_token=os.environ["BOT_TOKEN"],
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"])
CHAT_ID = [int(chat_id) for chat_id in os.environ.get("CHAT_ID", "").split(",")]

async def broadcast_message(client, text):
    if text.strip():
        cursor = mydb.cursor()
        cursor.execute("SELECT user_id FROM users")
        rows = cursor.fetchall()
        for row in rows:
          try:
            await client.send_message(
                chat_id=int(row[0]),
                     text=text,
                        disable_notification=True)
            print("sending is done!")
          except Exception as e:
            print(e)
          await asyncio.sleep(random.randint(4,10))
        
        return
    else:
        print("Empty message. Skipping broadcast.")
        return
    
@pr0fess0r_99.on_message(filters.private & filters.command(["broadcast"]))
async def broadcast_command(client:Client, message:Message):
    owner_id = os.environ.get("OWNER_ID", None)
    if owner_id and message.from_user.username == owner_id[1:]:
        broadcast_text = " ".join(message.command[1:])
        await asyncio.ensure_future(broadcast_message(client, broadcast_text))
        return
    else:
        print("You are not the owner")
        return
    
def get_user_count():
    cursor = mydb.cursor()
    cursor.execute("SELECT COUNT(user_id) FROM users")
    count = cursor.fetchone()[0]
    return count
        
@pr0fess0r_99.on_message(filters.private & filters.command(["start"]))
async def start(client:Client, message:Message):
    button=[[InlineKeyboardButton("𝚂𝚄𝙿𝙿𝙾𝚁𝚃", url="https://t.me/Prime_SaversBot")]]
    await message.reply_text(text="**𝙷𝙴𝙻𝙻𝙾...⚡️\n\n𝙸𝙰𝙼 𝙰 𝚂𝙸𝙼𝙿𝙻𝙴 𝚃𝙴𝙻𝙴𝙶𝚁𝙰𝙼 𝙰𝚄𝚃𝙾 𝚁𝙴𝚀𝚄𝙴𝚂𝚃 𝙰𝙲𝙲𝙴𝙿𝚃 𝙱𝙾𝚃.", reply_markup=InlineKeyboardMarkup(button), disable_web_page_preview=True)
    return


@pr0fess0r_99.on_chat_join_request(filters.chat(CHAT_ID))
async def autoapprove(client:Client, message:Message):
    chat = message.chat  
    user = message.from_user 
    if chat.id in CHAT_ID:  
        print(f"{user.first_name} 𝙹𝙾𝙸𝙽𝙴𝙳 ⚡️")  
        await client.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
        welcome_message = f"Welcome to {chat.title}, {user.first_name}! \nHappy Shopping!!!!"
        await client.send_message(user.id, welcome_message)
        cursor = mydb.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user.id,))
        existing_user = cursor.fetchone()
        mydb.commit()
        mydb.close()
        if existing_user:
            print(f"User {user.id} already exists in the database.")
            return
        else:
            cursor.execute("INSERT INTO users (user_id) VALUES (%s)", (user.id,))
            mydb.commit()
            mydb.close()
            return
        
@pr0fess0r_99.on_message(filters.private & filters.command(["count_users"]))
async def count_users_command(client:Client, message:Message):
    owner_id = os.environ.get("OWNER_ID", None)
    if owner_id and message.from_user.username == owner_id[1:]:
        count = get_user_count()
        await message.reply_text(f"Total users: {count}")
        return
    else:
        print("u r not owner")
        return
    
@pr0fess0r_99.on_message(filters.private & filters.command(["reset_database"]))
async def reset_database(client:Client, message:Message):
    owner_id = os.environ.get("OWNER_ID", None)
    if owner_id and message.from_user.username == owner_id[1:]:
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM users")
        mydb.commit()
        cursor.close()
        await message.reply_text("Database reset successful. All entries have been deleted.")
        return
    else:
        await message.reply_text("You are not authorized to perform this action.")
        return

print("𝗕𝗼𝘁 𝗦𝘁𝗮𝗿𝘁𝗲𝗱")
pr0fess0r_99.run()
