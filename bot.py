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
        [InlineKeyboardButton("❤️ JOIN NOW ❤️", url="https://t.me/+xeuoL6uq_AA3MzQ1")],
        [InlineKeyboardButton("MAIN CHANNEL 🛍️", url="https://t.me/+xeuoL6uq_AA3MzQ1")]
    ]
    photo_url = "https://i.ibb.co/WBjZ4tn/photo1713602597.jpg"
    await message.reply_photo(photo=photo_url, caption='''
90% Discount Big Loots & Deals (From Amazon & Flipkart) Only Post in Our Main Channels 🔥👇. 

🛍हमारे Main  चैनल "Prime Savers" (250K Subscribers) को Join करलो 
यहाँ आपको बहुत सारी Loots के Link मिलेगा। 

👇👇👇👇JOIN NOW👇👇👇👇
https://t.me/+a59EuSFxiNMwZGY1
https://t.me/+a59EuSFxiNMwZGY1
https://t.me/+a59EuSFxiNMwZGY1
https://t.me/+a59EuSFxiNMwZGY1
👆👆👆👆JOIN NOW👆👆👆👆 

Note : We Don't Post Any Loots Here , If You Ignore This Msg & Don't Join Our Main Channel (You May Miss Many Loots Daily) 🙂❤️🙏''',reply_markup=InlineKeyboardMarkup(button))
print("𝗕𝗼𝘁 𝗦𝘁𝗮𝗿𝘁𝗲𝗱")
pr0fess0r_99.run()
