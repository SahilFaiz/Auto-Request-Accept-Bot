import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

pr0fess0r_99 = Client(
    "𝗕𝗼𝘁 𝗦𝘁𝗮𝗿𝘁𝗲𝗱",
    bot_token=os.environ["BOT_TOKEN"],
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"]
)
        
@pr0fess0r_99.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    approvedbot = await client.get_me() 
    await message.reply_text(text='''Join Our Main Prime Savers  Channel (Open Link & Join Fast) 

Prime Savers (250k+
Subscribers) Join Fast👇
https://t.me/+a59EuSFxiNMwZGY1 


🛍हमारे Main  चैनल "Prime Savers" को Join करलो 
यहाँ आपको बहुत सारी Loots के Link मिलेगा। 

👇👇👇👇JOIN NOW👇👇👇👇
https://t.me/+a59EuSFxiNMwZGY1
https://t.me/+a59EuSFxiNMwZGY1


Note : We Don't Post Any Loots Here, Join Our Main Channel for Loots & Deals''', reply_markup=InlineKeyboardMarkup(button), disable_web_page_preview=True)

print("𝗕𝗼𝘁 𝗦𝘁𝗮𝗿𝘁𝗲𝗱")
pr0fess0r_99.run()
