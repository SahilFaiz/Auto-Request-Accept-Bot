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
    button=[
        [InlineKeyboardButton("JOIN", url="https://t.me/+a59EuSFxiNMwZGY1")]
    ]
    await message.reply_text(text='''Avail the Best Deals, Unbeatable Offers, and Exclusive Loots all in one place

❤Share And Support Us✌''',reply_markup=InlineKeyboardMarkup(button), disable_web_page_preview=False)

print("𝗕𝗼𝘁 𝗦𝘁𝗮𝗿𝘁𝗲𝗱")
pr0fess0r_99.run()
