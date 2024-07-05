import asyncio
import threading
from typing import Final
from datetime import datetime
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

#initialize clue_info
with open("clues.json", "r") as clues:
	clue_contents = json.load(clues)

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
    await update.message.reply_text('Key in your group name to start. eg.Azu_1')
    startTimer(20000)

#functions
def initialise_clan(clan: str) -> str:
  doc = doc_ref.get()
  if doc.exists:
    dic = doc.to_dict()
    if dic[clan]["progress"] == ['start']:
      dic[clan]["progress"] = route_contents[dic[clan]["route"]]["route"]
      doc_ref.set(dic)
      return "Please Key in password to start the scavenger hunt and get your first clue.", ""
    else:
      if dic[clan]["progress"]:
        return clue_contents[dic[clan]["progress"][0]]["clue"] + '\n \n To continue hunt please key in the next password to get your next clue.', clue_contents[dic[clan]["progress"][0]]["image"]
      else:
        return "Congratulations on completing the Heroes Quest! Your Guardian Spirits thanks you for your bravery! Please DO NOT LEAVE your last station. Update your FACI that you have completed your quest and they will come and pick you up from your location shortly, Thank you!", ""
  else:
    return 'Unable to retrieve data.', ""

def password_check(code: str, sub_clan: str) -> str:
  doc = doc_ref.get()
  if doc.exists:
    dic = doc.to_dict()
    if dic[sub_clan]["progress"]:
      if clue_contents[dic[sub_clan]["progress"][0]]["code"] == code:
        curr = dic[sub_clan]["progress"].pop(0)
        print()
        print(f'{'\033[4m'}{'\033[1m'}subclan: {sub_clan}{'\033[0m'} ' + datetime.now().strftime("%H:%M:%S"))
        print(f'{'\033[32m'}curr: {curr}{'\033[0m'}')
        doc_ref.set(dic)
        if dic[sub_clan]["progress"]:
          print(f'{'\033[36m'}next station: {dic[sub_clan]["progress"][0]}{'\033[0m'}')
          print()
          return clue_contents[dic[sub_clan]["progress"][0]]["clue"] + '\n \n Find the next station and retrieve the password to get your next clue.', clue_contents[dic[sub_clan]["progress"][0]]["image"]
        else:
          print(f'{'\033[31m'}{sub_clan} completed at {datetime.now().strftime("%H:%M:%S")}{'\033[0m'}')
          # print(sub_clan + " completed at " + datetime.now().strftime("%H:%M:%S") )
          return "Congratulations on completing the Heroes Quest! Your Guardian Spirits thanks you for your bravery! Please DO NOT LEAVE your last station. Update your FACI that you have completed your quest and they will come and pick you up from your location shortly, Thank you!", ""
      else:
        return "Password Incorrect. Try Again.", ""
    else:
      print(f'{'\033[31m'}{sub_clan} completed at {datetime.now().strftime("%H:%M:%S")}{'\033[0m'}')
      # print(sub_clan + " completed at " + datetime.now().strftime("%H:%M:%S") )
      return "Congratulations on completing the Heroes Quest! Your Guardian Spirits thanks you for your bravery! Please DO NOT LEAVE your last station. Update your FACI that you have completed your quest and they will come and pick you up from your location shortly, Thank you!", ""
  else:
    return "Unable to retrieve data.", ""
  
#Responses
def handle_response_scav(text: str, context: ContextTypes.DEFAULT_TYPE) -> str:
  try:
    user_data = context.user_data
    if any(clan in text.upper() for clan in ["AZU_","XOLO_","ELIOS_","IVIES_"]):
      user_data["name"] = text.upper()
      return initialise_clan(text.upper())
    else:
      return password_check(text, user_data.get("name"))
  except Exception as error:
    print("An exception occurred:", error)
    return 'An Error Occured. I do not understand your message.', ""

async def handle_message(update:Update, context: ContextTypes.DEFAULT_TYPE):
    global hunt_stopped
  
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # print(f'User ({update.message.chat.id}),({update.message.from_user.username}) in {message_type}: "{text}"')
    if hunt_started:
      if 'group' in message_type:
          if BOT_USERNAME in text:
              new_text: str = text.replace(BOT_USERNAME, '').strip()
              response, image = handle_response_scav(new_text, context)
          else:
              return  
      else:
          response, image = handle_response_scav(text, context)

      print('Bot:', response)      
      await update.message.reply_text(response)
      if image:
        chat_id = update.message.chat_id
        photo_file = open(image, 'rb') 
        await context.bot.send_photo(chat_id=chat_id, photo=photo_file)
  
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
