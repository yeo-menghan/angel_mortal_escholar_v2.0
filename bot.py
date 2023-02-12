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
import db, game_msg

API_KEY = os.environ.get('API_KEY')
CHAT_IDS = db.get_chat_ids()
PLAYERS_ALL = setup() # load angel and mortal pairing
PLAYER_COMBINED_INFO = db.PLAYER_COMBINED_INFO # load dictionary of all registered players

# in 20.0 version of telegram, bot, application.builder replaces and encompasses the Updater
application = Application.builder().token(API_KEY).build()

# TODO: Enable logging
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
    # print(chat_id)
    if not player:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Sorry, not registered as participant in Angel&Mortal. If you think it's a mistake, please contact @yeo_menghan."
        )
    elif chat_id > 0 and chat_id not in CHAT_IDS.keys():
        update_chat_id(username, chat_id)
    await context.bot.send_message(
        chat_id=chat_id,
        text=game_msg.welcome_text(username)) 
    # once player /start on telegram, their chat_id will become numerical and start to work within this program
    
'''For General Announcements + Using '/blast' command'''
async def blast_announcement(update, context):
    if (update.effective_chat.username == "yeo_menghan"):
        for user_chat_id in CHAT_IDS.values():
            await application.bot.send_message(chat_id=user_chat_id, text=game_msg.ANNOUNCEMENT_BLAST) # edit text in game_msg.py

async def help(update: Update, context: CallbackContext):
    await update.message.reply_text(game_msg.HELP)

async def check_start_info(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    await context.bot.send_message(text=game_msg.relay_start_info(username), chat_id=update.effective_chat.id)

'''Only made available during revelation'''
async def reveal(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    await context.bot.send_message(text=game_msg.revelation(username), chat_id=update.effective_chat.id)

async def instruction(update: Update, context: CallbackContext):
    await update.message.reply_text(game_msg.INSTRUCTION)

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
    elif player.get_chat_with() == 'angel':
        angel_chat_id = player.get_angel().get_chat_id()
        if not angel_chat_id:
            await context.bot.send_message(
                text="Sorry, your angel has not started the chat yet... If this problem persists, please contact the admin.",
                chat_id=update.effective_chat.id
            )
        return angel_chat_id


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

# send/receive messages to/from angel / mortal
async def message_forward(update: Update, context: CallbackContext):
    username = update.effective_chat.username
    # chat_id = update.effective_chat.id
    forward_chat_id = await check_message(update, context)
    if forward_chat_id:
        player = PLAYERS_ALL.get(update.effective_chat.username)
        forward_to = ('angel' if player.get_chat_with() == 'mortal' else
                      'mortal' if player.get_chat_with() == 'angel' else
                      None
                      )
        #NEW Feature: Update timing on google sheet
        if player.get_chat_with() == 'mortal':
            db.update_timing_mortal(username)
        elif player.get_chat_with() == 'angel':
            db.update_timing_angel(username)
        
        if update.message.text:
            await context.bot.send_message(
                text=f"Your {forward_to} says: {update.message.text}",
                chat_id=forward_chat_id
            )
        elif not update.message.text and not update.message.pinned_message: # At every instance of pinning a message
            await context.bot.send_message(
                text=f"Your {forward_to} says: ",
                chat_id=forward_chat_id    
            )
            await sendNonTextMessage(update.message, context.bot, forward_chat_id)


async def angel_command(update, context):
    player=PLAYERS_ALL.get(update.effective_chat.username)
    player.set_chat_with('angel')
    message=await context.bot.send_message(
        text="Chatting with Angel!",
        chat_id=update.effective_chat.id
    )
    await context.bot.pin_chat_message(
        chat_id=update.effective_chat.id,
        message_id=message.message_id
    )


async def mortal_command(update, context):
    player = PLAYERS_ALL.get(update.effective_chat.username)
    player.set_chat_with('mortal')
    message = await context.bot.send_message(
        text="Chatting with Mortal!",
        chat_id=update.effective_chat.id
    )
    await context.bot.pin_chat_message(
        chat_id=update.effective_chat.id,
        message_id = message.message_id
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

def main() -> None:
    application.add_handler(MessageHandler(~filters.COMMAND, message_forward))
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('angel', angel_command))
    application.add_handler(CommandHandler('mortal', mortal_command))
    application.add_handler(CommandHandler('who', who_command))
    application.add_handler(CommandHandler('checkinfo', check_start_info))
    application.add_handler(CommandHandler('reveal', reveal)) # for revelation
    application.add_handler(CommandHandler('instruction', instruction))
    application.add_handler(CommandHandler('blast', blast_announcement)) # for any announcement blasts, but will users be able to see it thou?
    application.run_polling()

if __name__ == '__main__':
    main()