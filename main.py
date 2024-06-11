
import asyncio
import os
from dotenv import load_dotenv
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes



from scav import handle_message, scav_command
from lunch import lunch_command


load_dotenv()

TOKEN: Final = os.getenv("BOT_TOKEN")
BOT_USERNAME : Final = "@SMUTOPIABOT"

#Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text('Welcome to SMUTOPIA!!! What would you like to do?')

async def error(update:Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting Bot')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('hunt', scav_command))
    app.add_handler(CommandHandler("whats_cooking", lunch_command))

    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Errors
    app.add_error_handler(error)
    print('Polling...')
    app.run_polling(poll_interval=3)