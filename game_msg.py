# load dictionary of all registered players
import db
from setup import setup
PLAYER_COMBINED_INFO = db.PLAYER_COMBINED_INFO
PLAYERS_ALL = setup()  # load angel and mortal pairing

'''For /blast annoucement blasts to everyone participating in bot.py'''
ANNOUNCEMENT_BLAST = ("""
Hi everyone! It has been 2 weeks since Angel & Mortal started. However, with all good things, it has finally come to an end.

We will be revealing your angels now! Please / checkinfoangel to find out who your angel is !""")

'''Help commands attached to bot.py'''
HELP = ("""Available Commands :
    /angel: talk with your angel
    /mortal: talk with your mortal
    /help: for help!
    /checkinfo: to reference mortal's info again
    /instruction: to reference angel & mortal's game instructions""")

INSTRUCTION = ("""
Hello Everyone!! Welcome to our Angel and Mortal Game AY2223 S2! 😇

Our angel mortal will run from 31st January to 13th February, so ideally give 1 gift each week 

Here are the rules

1. You get assigned 1 angel and 1 mortal 

2. Your angel is the person who sayang/take care of you, give you gifts and makes sure the next few weeks aren’t complete pain :”) or be the one who PRANKS you

3. Your mortal is the person YOU sayang/take care of, give them gifts and make sure they stay alive for the next few weeks or the person you pull PRANKS on

4. Pls don’t accidentally reveal your identity to your mortal in a dumb way like PM-ing them :”) if they figure it out themselves that’s cool but ya if you got anything to tell them can pm @yeo_menghan and he’ll forward your message to them!

5. For those not on campus, fret not! You can contact @yeo_menghan to help deliver your gifts to your mortal and likewise from your angel

For this iteration, we're limiting PRANKING within RC4 ONLY as part of trialing the new initiative and to ensure the same level of enthusiasm is matched amongst those participating.

Also!! V impt!!! GIVE LETTERS AND NOTES TGT WITH YOUR GIFTS 🎁🥺 rmb that angel mortal is for yall to get to know each other better and make new frens (from diff batches/diff residences!), and also to have an excuse to make/buy things 💌 Youre highly encouraged to leave notes for your angels also (like just leave it at your door to take the next time they come by) then you can make double the number of friends HAHAHA

Please refer to this document for the general rules: https://docs.google.com/document/d/1wsRdHFySartKzg-tZOqn1Epp4_7QR41NSteivokOJqA/edit?usp=sharing     
    """)

#TODO: send the 2 commands for /checkinfo & /instruction

def welcome_text(username):
    text = "Welcome @" + username + \
         " to Angel & Mortal Escholars bot! You have successfully started the bot. The event starts from now till a day before Valentine's Day (13th Feb)!"
    text += "\n\nTo begin, /checkinfo to get your mortal's info\n\n"
    text += "\n\nPLEASE READ THE INSTRUCTIONS! Use /instruction to check instructions!\n\n"
    return text

'''relay info at start and when checkinfomortal in bot.py'''
def relay_start_info(player):
    '''Input player's username into the parameter'''
    # find player's mortal pairing
    mortal = PLAYERS_ALL.get(player).get_mortal().get_username()
    mortal_name = PLAYER_COMBINED_INFO[mortal]["name"]
    mortal_course = PLAYER_COMBINED_INFO[mortal]["course"]
    mortal_year = PLAYER_COMBINED_INFO[mortal]["year"]
    mortal_nusmods = PLAYER_COMBINED_INFO[mortal]["nusmods"]
    mortal_residence = PLAYER_COMBINED_INFO[mortal]["residence"]
    mortal_room = PLAYER_COMBINED_INFO[mortal]["room"]
    mortal_wishlist = PLAYER_COMBINED_INFO[mortal]["wishlist"]
    mortal_dislikes = PLAYER_COMBINED_INFO[mortal]["dislikes"]
    mortal_interests = PLAYER_COMBINED_INFO[mortal]["interests"]
    mortal_welfare_lvl = PLAYER_COMBINED_INFO[mortal]["welfare_lvl"]
    mortal_prank_lvl = PLAYER_COMBINED_INFO[mortal]["prank_lvl"]

    # find player's angel pairing
    angel = PLAYERS_ALL.get(player).get_angel().get_username()
    angel_welfare_lvl = PLAYER_COMBINED_INFO[angel]["welfare_lvl"]
    angel_prank_lvl = PLAYER_COMBINED_INFO[angel]["prank_lvl"]

    # find mortal in giant spreadsheet (using first column)
    # relay mortal's information and angel's welfare/prank level in a formatted way

    text = "Your mortal is: " + mortal_name + '\n'
    text += "Course: " + mortal_course + '\n'
    text += "Year: " + mortal_year + '\n'
    text += "Nusmods link (if any): " + mortal_nusmods + '\n'
    text += "Residence: " + mortal_residence + '\n'
    text += "Room: " + mortal_room + '\n'
    text += "Wishlist: " + '\n' + mortal_wishlist + '\n\n'
    text += "Dislikes: " + '\n' + mortal_dislikes + '\n\n'
    text += "Interests: " + '\n' + mortal_interests + '\n'
    text += "Welfare level: " +  str(mortal_welfare_lvl) + '\n'
    text += "Prank level: " + str(mortal_prank_lvl) + '\n\n'

    text += "To manange expectations, we're revealing your angel's welfare and prank level: " + '\n'
    text += "Angel's welfare level: " + str(angel_welfare_lvl) + '\n'
    text += "Angel's prank level: " + str(angel_prank_lvl)
    return text


def revelation(player):
    angel = PLAYERS_ALL.get(player).get_angel().get_username()
    angel_name = PLAYER_COMBINED_INFO[angel]["name"]
    text = "Your Angel is " + angel_name + " @" + angel + '\n\n'
    text += "Kinda anti-climatic :') BBBUT Hope that Angel & Mortal has been fun for everybody! " + '\n\n'
    text += "Please do give your angel something in return to thank them for the last 2 weeks of welfare!" + '\n\n'
    text += "Thank you so much for signing up for this iteration and hope you have a nice day ahead :)" + '\n'
    return text
