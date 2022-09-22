import logging
import os
import asyncio
from html import escape
from uuid import uuid4
from telegram import (
    Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, User, InlineQueryResultArticle, InputTextMessageContent, Message
)
from telegram.ext import (
    Application, Updater, ApplicationBuilder, CommandHandler, filters, ContextTypes, MessageHandler, CallbackContext, ConversationHandler, CallbackQueryHandler, InlineQueryHandler
)
from telegram.constants import ParseMode
from dotenv import load_dotenv
load_dotenv()

# import the other local files
from setup import setup
import db

API_KEY = os.environ.get('API_KEY')
CHAT_IDS = db.get_chat_ids()
PLAYERS_ALL = setup() # load angel and mortal pairing
PLAYER_COMBINED_INFO = db.PLAYER_COMBINED_INFO # load dictionary of all registered players

# in 20.0 version of telegram, bot, application.builder replaces and encompasses the Updater
application = Application.builder().token(API_KEY).build()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def update_chat_id(username, chat_id):
    CHAT_IDS[username] = chat_id
    db.update_chat_ids(username, chat_id)
    PLAYERS_ALL.get(username).set_chat_id(chat_id)

async def start(update: Update, context: CallbackContext):
    player = PLAYERS_ALL.get(update.effective_chat.username)
    username = update.message.from_user.username
    chat_id = update.effective_chat.id
    print(chat_id)
    if not player:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Sorry, not registered as participant in Angel&Mortal. " +
            "If you think it's a mistake, please contact @yeo_menghan."
        )
    elif chat_id > 0 and chat_id not in CHAT_IDS.keys():
        update_chat_id(username, chat_id)
    
    text = 'Welcome @' + username+ """ to Angel & Mortal Escholars bot! You have successfully started the bot. The event starts now and ends during recess bonding event!!"""
    # migrate all the texts to another file
    text += "\n\n/help for commands\n\n"
    text += relay_mortal_info(username)
    await context.bot.send_message(
        chat_id=chat_id,
        text=text) 
    # once player /start on telegram, their chat_id will become numerical and start to work within this program
    

def relay_mortal_info(player):
    '''Input player's username into the parameter'''
    #find player's mortal pairing
    mortal = PLAYERS_ALL.get(player).get_mortal().get_username()
    mortal_name = PLAYER_COMBINED_INFO[mortal]["name"]
    mortal_course = PLAYER_COMBINED_INFO[mortal]["course"]
    mortal_year = PLAYER_COMBINED_INFO[mortal]["year"]
    mortal_nusmods = PLAYER_COMBINED_INFO[mortal]["nusmods"]
    mortal_residence = PLAYER_COMBINED_INFO[mortal]["residence"]
    mortal_room = PLAYER_COMBINED_INFO[mortal]["room"]
    mortal_budget_lvl = PLAYER_COMBINED_INFO[mortal]["budget_lvl"]
    mortal_wishlist = PLAYER_COMBINED_INFO[mortal]["wishlist"]
    mortal_dislikes = PLAYER_COMBINED_INFO[mortal]["dislikes"]
    mortal_interests = PLAYER_COMBINED_INFO[mortal]["interests"]
    #find mortal in giant spreadsheet (using first column)
    # relay mortal's name, gender, course, year, nusmods, residence, room, budget_lvl, wishlist, dislikes, interests in a formatted way

    text = "Your mortal is: " + mortal_name + '\n'
    text += "Course: " + mortal_course + '\n'
    text += "Year: " + mortal_year + '\n'
    text += "Nusmods link (if any): " + mortal_nusmods + '\n'
    text += "Residence: " + mortal_residence + '\n'
    text += "Room: " + mortal_room + '\n'
    text += "Budget Level: " + mortal_budget_lvl + '\n\n'
    text += "Wishlist: " + '\n' + mortal_wishlist + '\n\n'
    text += "Dislikes: " + '\n' + mortal_dislikes + '\n\n'
    text += "Interests: " + '\n' + mortal_interests
    return text

def revelation(player):
    angel = PLAYERS_ALL.get(player).get_angel().get_username()
    angel_name = PLAYER_COMBINED_INFO[angel]["name"]
    text = "Your Angel is " + angel_name + " @" + angel + '\n\n'
    text += "Kinda anti-climatic :') BBBUT Hope that Angel & Mortal has been fun for everybody! " + '\n\n'
    text += "Please do give your angel something in return to thank them for the last 2 weeks of welfare!"  + '\n\n'
    text += "Thank you so much for signing up for this iteration and hope you have a nice day ahead :)" + '\n'
    return text

async def help(update: Update, context: CallbackContext):
    await update.message.reply_text("""Available Commands :
    /angel: talk with your angel
    /mortal: talk with your mortal
    /help: for help!
    /checkinfo: to reference mortal's info again
    /instruction: to reference angel & mortal's game instructions""")

async def checkinfo(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    await context.bot.send_message(text=relay_mortal_info(username), chat_id=update.effective_chat.id)

async def checkinfoangel(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    await context.bot.send_message(text=revelation(username), chat_id=update.effective_chat.id)

async def instruction(update: Update, context: CallbackContext):
    await update.message.reply_text("""
Hello Everyone!! Welcome to our Angel and Mortal Game 2022! 😇

Our angel mortal will run from 9th September to E-scholars bonding event during recess week (look forward to it!), so ideally give 1 gift each week (for 1-2 weeks); space out your budget so you dont go broke ya 💸💸💸

Here are the rules

1️⃣ You get assigned 1 angel and 1 mortal (THEY ARE DIFFERENT PPL YES). You are both an angel to a mortal and a mortal to an angel!

2️⃣ Your angel is the person who sayang/take care of you, give you gifts and makes sure the next few weeks arent complete pain :”)

3️⃣ Your mortal is the person YOU sayang/take care of, give them gifts and make sure they stay alive for the next few weeks

4️⃣ Pls dont accidentally reveal your identity to your mortal in a dumb way like PM-ing them :”) if they figure it out themselves thats cool but ya if you got anything to tell them can pm them through the telegram bot anonymously!

5️⃣ We hope to keep this angel & mortal event wholesome, so please do avoid pranking. Nevertheless, if you do want to prank, please check with your mortal if they're open to it via the telegram bot chat feature before proceeding!

6️⃣ For those not staying on campus / not RC4 or are gifting a mortal that's not on campus / not in the same residences, fret not! Please contact @yeo_menghan to assist in gifting! Meng Han will be free on Tuesday afternoons and Friday mornings to assist! 

Also!! V impt!!! GIVE LETTERS AND NOTES TGT WITH YOUR GIFTS 🎁🥺 rmb that angel mortal is for yall to get to know each other better and make new frens (from diff batches/diff residences!), and also to have an excuse to make/buy things 💌 Youre highly encouraged to leave notes for your angels also (like just leave it at your door to take the next time they come by) then you can make double the number of friends HAHAHA
    """)

async def check_message(update: Update, context: CallbackContext):
    player = PLAYERS_ALL.get(update.effective_chat.username)
    if not player:
        await context.bot.send_message(
            text="Sorry, not registered as participant in Angel&Mortal. " + 
                "If you think it's a mistake, please contact @yeo_menghan.", 
                chat_id=update.effective_chat.id
        )
        return
    elif not player.get_chat_id:
        await context.bot.send_message(
            text="Sorry, please /start me first!",
            chat_id=update.effective_chat.id
        )
        return
    elif player.get_chat_with() == '':
        await context.bot.send_message(
            text="Sorry, please select who to chat with first!",
            chat_id=update.effective_chat.id
        )
        return
    elif player.get_chat_with() == 'mortal':
        mortal_chat_id = player.get_mortal().get_chat_id()
        if not mortal_chat_id:
            await context.bot.send_message(
                text="Sorry, your mortal has not started the chat yet... If this problem persists, please contact the admin.",
                chat_id=update.effective_chat.id
            )
        return mortal_chat_id
        # context.bot.send_message(
        #     text='Your angel says: ' + update.message.text,
        #     chat_id=mortal_chat_id
        # )
    elif player.get_chat_with() == 'angel':
        angel_chat_id = player.get_angel().get_chat_id()
        if not angel_chat_id:
            await context.bot.send_message(
                text="Sorry, your angel has not started the chat yet... If this problem persists, please contact the admin.",
                chat_id=update.effective_chat.id
            )
        return angel_chat_id
        # context.bot.send_message(
        #     text='Your mortal says: ' + update.message.text,
        #     chat_id=angel_chat_id
        # )


async def sendNonTextMessage(message, bot, chat_id):
    print(message.photo)
    if message.photo:
        await bot.send_photo(
            photo=message.photo[-1],
            caption=message.caption,
            chat_id=chat_id
        )
    elif message.sticker:
        print(message.sticker)
        await bot.send_sticker(
            sticker=message.sticker,
            chat_id=chat_id
        )
    elif message.document:
        print(message.document)
        await bot.send_document(
            document=message.document,
            caption=message.caption,
            chat_id=chat_id
        )
    elif message.video:
        await bot.send_video(
            video=message.video,
            caption=message.caption,
            chat_id=chat_id
        )
    elif message.video_note:
        await bot.send_video_note(
            video_note=message.video_note,
            chat_id=chat_id
        )
    elif message.voice:
        await bot.send_voice(
            voice=message.voice,
            chat_id=chat_id
        )
    elif message.audio:
        await bot.send_audio(
            audio=message.audio,
            chat_id=chat_id
        )
    elif message.animation:
        await bot.send_animation(
            animation=message.animation,
            chat_id=chat_id
        )

async def message_forward(update: Update, context: CallbackContext):
    forward_chat_id = await check_message(update, context)
    if forward_chat_id:
        player = PLAYERS_ALL.get(update.effective_chat.username)
        forward_to = ('angel' if player.get_chat_with() == 'mortal' else
                      'mortal' if player.get_chat_with() == 'angel' else
                      None
                      )
        if update.message.text:
            await context.bot.send_message(
                text=f"Your {forward_to} says: {update.message.text}",
                chat_id=forward_chat_id
            )
        elif not update.message.text:
            print("running")
            await context.bot.send_message(
                text=f"Your {forward_to} says: ",
                chat_id=forward_chat_id
            )
            await sendNonTextMessage(update.message, context.bot,
                               forward_chat_id)
            

async def angel_command(update, context):
    player = PLAYERS_ALL.get(update.effective_chat.username)
    player.set_chat_with('angel')
    await context.bot.send_message(
        text="You are now chatting with your angel!",
        chat_id=update.effective_chat.id
    )


async def mortal_command(update, context):
    player = PLAYERS_ALL.get(update.effective_chat.username)
    player.set_chat_with('mortal')
    await context.bot.send_message(
        text="You are now chatting with your mortal!",
        chat_id=update.effective_chat.id
    )


async def who_command(update, context):
    player = PLAYERS_ALL.get(update.effective_chat.username)
    chat_with = player.get_chat_with()
    if chat_with:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"You are currently chatting with the {chat_with}."
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="You are currently not chatting with anyone."
        )

async def blast_announcement(update, context):
    if(update.effective_chat.username == "yeo_menghan"):
        for user_chat_id in CHAT_IDS.values():
            await application.bot.send_message(chat_id=user_chat_id, text="""
Hi everyone! It has been 2 weeks since Angel & Mortal started. However, with all good things, it has finally come to an end. 

We will be revealing your angels now! Please /checkinfoangel to find out who your angel is!
            """)

# asyncio.run(blast_announcement())

def main() -> None:
    application.add_handler(MessageHandler(~filters.COMMAND, message_forward))
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('angel', angel_command))
    application.add_handler(CommandHandler('mortal', mortal_command))
    application.add_handler(CommandHandler('who', who_command))
    application.add_handler(CommandHandler('checkinfo', checkinfo))
    application.add_handler(CommandHandler('checkinfoangel', checkinfoangel)) # for revelation on 22/9/2022
    application.add_handler(CommandHandler('instruction', instruction))
    application.add_handler(CommandHandler('blast', blast_announcement)) # for any announcement blasts, but will users be able to see it thou?
    application.run_polling()

if __name__ == '__main__':
    main()