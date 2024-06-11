from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

#lunch starting command
async def lunch_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  message_type: str = update.message.chat.type
  text: str = update.message.text
  if 'group' in message_type:
    if BOT_USERNAME in text:
        new_text: str = text.replace(BOT_USERNAME, '').strip()
        response: str = handle_response_lunch(new_text)
    else:
        return  
  else:
      response: str = handle_response_lunch(text)

  print('Bot:', response)
  
  await update.message.reply_text(response)

#Responses
def handle_response_lunch(text: str) -> str:

    return 'My Boy Cooked'