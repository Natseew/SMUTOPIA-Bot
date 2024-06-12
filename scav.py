import asyncio
import threading
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

#global Variables
hunt_started = False
hunt_stopped = False
BOT_USERNAME : Final = "@SMUTOPIABOT"

def startTimer(waitForSeconds):
    loop = asyncio.new_event_loop()
    threading.Thread(daemon=True, target=loop.run_forever).start()
    async def sleep_and_run():
        await asyncio.sleep(waitForSeconds)
        await stop_hunt()
    asyncio.run_coroutine_threadsafe(sleep_and_run(), loop)

async def stop_hunt():
  global hunt_started
  global hunt_stopped
  hunt_started = False
  hunt_stopped = True
  
  

#scav starting command
async def scav_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global hunt_started
    hunt_started = True
    await update.message.reply_text('What is your group number?')
    startTimer(20)
    
    

#Responses
def handle_response_scav(text: str) -> str:
    if '1' in text:
        return 'Your first clue is .....'
    if '2' in text:
        return 'Your first clue is .....'
    if text == 'SCIS':
        return 'Your second clue is'

    return 'I do not understand your message.'

async def handle_message(update:Update, context: ContextTypes.DEFAULT_TYPE):
    global hunt_stopped
    
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}),({update.message.chat.username}) in {message_type}: "{text}"')
    if hunt_started:
        if 'group' in message_type:
            if BOT_USERNAME in text:
                new_text: str = text.replace(BOT_USERNAME, '').strip()
                response: str = handle_response_scav(new_text)
            else:
                return  
        else:
            response: str = handle_response_scav(text)

        print('Bot:', response)
        
        await update.message.reply_text(response)
  
    if hunt_stopped:
      if 'group' in message_type:
        if BOT_USERNAME in text:
          hunt_stopped = False
          await update.message.reply_text('The Hunt has ended. Please run /Hunt again if needed.')
        else:
          return 
      else:
        hunt_stopped = False
        await update.message.reply_text('The Hunt has ended. Please run /Hunt again if needed.')
