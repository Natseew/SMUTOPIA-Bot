import asyncio
import threading
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

import firebase_admin
from firebase_admin import credentials, db, firestore
import json

#initialize firebase
cred = credentials.Certificate("smu-fo2024-smutopiabot-firebase-adminsdk-tt5im-6f3313e2ae.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
doc_ref = db.collection("hunt").document("clan_info")

#initialize route_info
with open("route_info.json", "r") as route:
	route_contents = json.load(route)

#global Variables
hunt_started = False
hunt_stopped = False
sub_clan = ""
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
    await update.message.reply_text('What is your group name?')
    startTimer(20)

#functions
def initialise_clan(clan: str) -> str:
  doc = doc_ref.get()
  if doc.exists:
    dic = doc.to_dict()
    if dic[clan]["progress"] == ['start']:
      dic[clan]["progress"] = route_contents[dic[clan]["route"]]["route"]
      doc_ref.set(dic)
      return "Please Key to start the scavenger hunt and get your first clue."
    else:
      return 'To continue hunt please key in the next password for the next clue.'
  else:
    return 'Unable to retrieve data.'

#Responses
def handle_response_scav(text: str) -> str:
  try:
    if text.upper() in ["AZU_1","XOLO_1"]:
      return initialise_clan(text.upper())
    else:
      return 'Pass'
  except:
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
