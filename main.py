from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = "7450986915:AAHmiCs_V5MLvqDKJl6dAcQFGPF3QxyQcfE"
BOT_USERNAME : Final = "@SMUTOPIABOT"

#Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text('Welcome to SMUTOPIA!!! Let us know your group number.')

#Responses

def handle_response(text: str) -> str:
    if '1' in text:
        return 'Your first clue is .....'
    
    return 'I do not understand your message.'

async def handle_message(update:Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str =update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:', response)

    await update.message.reply_text(response)

async def error(update:Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting Bot')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))

    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Errors
    app.add_error_handler(error)
    print('Polling...')
    app.run_polling(poll_interval=3)