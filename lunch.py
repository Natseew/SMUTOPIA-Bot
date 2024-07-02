from typing import Final
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


import json

BOT_USERNAME : Final = "@SMUTOPIABOT"

#initialize clue_info
with open("lunch_info.json", "r") as menu:
	menu_contents = json.load(menu)

#lunch starting command
async def lunch_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  keyboard = [
    [
        InlineKeyboardButton("Day 1", callback_data="D1"),
        InlineKeyboardButton("Day 2", callback_data="D2"),
    ],
    [
      InlineKeyboardButton("Day 3", callback_data="D3")
    ],
  ]

  reply_markup = InlineKeyboardMarkup(keyboard)

  await update.message.reply_text("Please choose:", reply_markup=reply_markup)

#Responses
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  """Parses the CallbackQuery and updates the message text."""
  query = update.callback_query

  # CallbackQueries need to be answered, even if no notification to the user is needed
  # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
  await query.answer()

  await query.edit_message_text(text=f"Selected option: " + menu_contents[{query.data}])