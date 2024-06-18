import os
import textwrap
from dotenv import load_dotenv
from typing import Final
from telegram import Update
from telegram.ext import *



from scav import handle_message, scav_command
from lunch import lunch_command


load_dotenv()

TOKEN: Final = os.getenv("BOT_TOKEN")
BOT_USERNAME : Final = "@SMUTOPIABOT"

#Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to SMUtopia, a realm where nature and magic entwine around the majestic World Tree. But peril looms – the Tree fades, poisoned by darkness. You, esteemed adventurers, are our chosen champions, embarking on the legendary Heroes Quest. Guided by wise Mentors (Facis) and challenged by Gatekeepers (Game Masters), your journey will test your courage and forge friendships. Embrace the adventure, uphold our CIRCLE values, and save our beloved land. Are you ready for the challenge?")
    await update.message.reply_text("Click on /help to get instructions.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(textwrap.dedent("""
    Instructions:
    
    In this quest, you are tasked with a series of challenges located within different parts of the SMU Campus only. As you attempt to successfully complete these challenges, you will be rewarded with potions (points).
    
    Any failure to complete any challenges will just result in no potions being awarded. The fastest subclan to finish this quest will be awarded with additional 100 potions. 
    
    Here’s how your quest will unfold:
    -   You will be on your own, as a subclan during this quest (No Mentors).

    -   The same phone have to be used to communicate with the bot throughout the quest.

    -   Duration: You have a maximum of 1.5 hours (until 11.45am) to complete the quest, the faster the better.

    -   Guidance: Each SC will use the clue given at every station by the gatekeepers to reveal the clue to their next destination via this bot. Use the provided school map and photo references to verify each location.

    -   Safety Rules: STRICTLY NO JAYWALKING (especially between SOB and LKS Library, and Connex and LKS Library ) and NO running. GMs and Facis will be stationed to enforce these rules. 
    
    -   Attendance: Follow your OWN route and visit ALL locations. Attendance will be taken.
    
    -   Lib Quest: you only need to visit your assigned library, LKS or KGC, not both to complete a challenge as part of your quest.
    
    -   SSH/Cozy Haven: This is just a touch and go station.

    -   Please send your message with (@SMUTOPIABOT) when submitting answers.
    
    Please pm @SUSannzz if you have any questions.
    Have Fun!!!
    Click on /hunt to start!!
    """
    ))

async def error(update:Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting Bot')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('hunt', scav_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler("whats_cooking", lunch_command))

    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Errors
    app.add_error_handler(error)
    print('Polling...')
    app.run_polling(poll_interval=3, allowed_updates=Update.ALL_TYPES)