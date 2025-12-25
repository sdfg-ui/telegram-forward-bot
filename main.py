import asyncio
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler

BOT_TOKEN = "8522330466:AAGtiV2kFCDQ2wHXJ9UDFt8jKpEGsZni_fQ"

SOURCE_CHAT_ID = -1002774891855
TARGET_CHAT_ID = -5051187981

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    msg = f"群名: {chat.title}\nChat ID: {chat.id}\n发送者: {user.first_name} (ID: {user.id})"
    await update.message.reply_text(msg)
    logger.info(f"Chat ID: {chat.id}, Title: {chat.title}")

async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.channel_post:
        chat = update.channel_post.chat
        print(f"\n=== 检测到频道消息 ===")
        print(f"频道名: {chat.title}")
        print(f"频道ID: {chat.id}")
        print(f"========================\n")
        logger.info(f"Channel ID: {chat.id}, Title: {chat.title}")
        
        if chat.id == SOURCE_CHAT_ID:
            message = update.channel_post
            try:
                if message.text:
                    await context.bot.send_message(
                        chat_id=TARGET_CHAT_ID,
                        text=message.text
                    )
                elif message.photo:
                    await context.bot.send_photo(
                        chat_id=TARGET_CHAT_ID,
                        photo=message.photo[-1].file_id,
                        caption=message.caption
                    )
                elif message.document:
                    await context.bot.send_document(
                        chat_id=TARGET_CHAT_ID,
                        document=message.document.file_id,
                        caption=message.caption
                    )
                elif message.video:
                    await context.bot.send_video(
                        chat_id=TARGET_CHAT_ID,
                        video=message.video.file_id,
                        caption=message.caption
                    )
                elif message.voice:
                    await context.bot.send_voice(
                        chat_id=TARGET_CHAT_ID,
                        voice=message.voice.file_id
                    )
                elif message.sticker:
                    await context.bot.send_sticker(
                        chat_id=TARGET_CHAT_ID,
                        sticker=message.sticker.file_id
                    )
                print(f"已转发消息到目标群")
                logger.info(f"Forwarded channel message from {SOURCE_CHAT_ID} to {TARGET_CHAT_ID}")
            except Exception as e:
                print(f"转发失败: {e}")
                logger.error(f"Forward failed: {e}")

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if SOURCE_CHAT_ID is None or TARGET_CHAT_ID is None:
        return
    
    if update.effective_chat.id != SOURCE_CHAT_ID:
        return
    
    message = update.message
    if message is None:
        return
    
    try:
        if message.text:
            await context.bot.send_message(
                chat_id=TARGET_CHAT_ID,
                text=message.text
            )
        elif message.photo:
            await context.bot.send_photo(
                chat_id=TARGET_CHAT_ID,
                photo=message.photo[-1].file_id,
                caption=message.caption
            )
        elif message.document:
            await context.bot.send_document(
                chat_id=TARGET_CHAT_ID,
                document=message.document.file_id,
                caption=message.caption
            )
        elif message.video:
            await context.bot.send_video(
                chat_id=TARGET_CHAT_ID,
                video=message.video.file_id,
                caption=message.caption
            )
        elif message.voice:
            await context.bot.send_voice(
                chat_id=TARGET_CHAT_ID,
                voice=message.voice.file_id
            )
        elif message.sticker:
            await context.bot.send_sticker(
                chat_id=TARGET_CHAT_ID,
                sticker=message.sticker.file_id
            )
        logger.info(f"Forwarded message from {SOURCE_CHAT_ID} to {TARGET_CHAT_ID}")
    except Exception as e:
        logger.error(f"Forward failed: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("chatid", get_chat_id))
    app.add_handler(MessageHandler(filters.ChatType.CHANNEL, handle_channel_post))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, forward_message))
    
    print("Bot启动中...")
    print("按 Ctrl+C 停止")
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
