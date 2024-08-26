import telebot
from telebot import types

API_TOKEN = '7413573877:AAHBwTwp43lUQLUmRCAxAjhnpjwxvP64zTE'
bot = telebot.TeleBot(API_TOKEN)

# Global variables to store user information
users = {}

# Dictionary of fox outfits by level
fox_outfits = {
    1: "🦊 Basic Outfit",
    2: "🦊 Warrior Outfit",
    3: "🦊 Mage Outfit",
    4: "🦊 Ninja Outfit",
    5: "🦊 King Outfit",
    6: "🦊 Pirate Outfit",
    7: "🦊 Knight Outfit",
    8: "🦊 Samurai Outfit",
    9: "🦊 Superhero Outfit",
    10: "🦊 Legendary Outfit",
    # Add more outfits for higher levels
}

# Command /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to Fox2Gamebot! Use /help to see available commands.")
    users[message.chat.id] = {'level': 1, 'quests': [], 'staked': 0}
    send_fox_outfit(message)

# Command /help
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "/start - Start the game\n"
        "/level - View your current level\n"
        "/quest - View and accept quests\n"
        "/stake - Stake your FOXCOIN\n"
        "/unstake - Withdraw your staked FOXCOIN\n"
        "/balance - View your FOXCOIN balance\n"
        "/levelup - Level up\n"
    )
    bot.reply_to(message, help_text)

# Command /level
@bot.message_handler(commands=['level'])
def send_level(message):
    level = users[message.chat.id]['level']
    bot.reply_to(message, f"Your current level is {level}.")
    send_fox_outfit(message)

# Command /levelup
@bot.message_handler(commands=['levelup'])
def level_up(message):
    users[message.chat.id]['level'] += 1
    level = users[message.chat.id]['level']
    bot.reply_to(message, f"Congratulations! You have reached level {level}.")
    send_fox_outfit(message)

# Function to send the fox outfit
def send_fox_outfit(message):
    level = users[message.chat.id]['level']
    outfit = fox_outfits.get(level, "🦊 Legendary Outfit")
    bot.send_message(message.chat.id, f"Your fox is now wearing: {outfit}")

# Command /quest
@bot.message_handler(commands=['quest'])
def send_quest(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    quest1 = types.KeyboardButton('Quest 1')
    quest2 = types.KeyboardButton('Quest 2')
    markup.add(quest1, quest2)
    bot.send_message(message.chat.id, "Choose a quest:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['Quest 1', 'Quest 2'])
def handle_quest(message):
    quest = message.text
    users[message.chat.id]['quests'].append(quest)
    bot.reply_to(message, f"You have accepted {quest}.")

# Command /stake
@bot.message_handler(commands=['stake'])
def stake_tokens(message):
    bot.reply_to(message, "How much FOXCOIN do you want to stake?")

@bot.message_handler(func=lambda message: message.text.isdigit())
def handle_stake(message):
    amount = int(message.text)
    users[message.chat.id]['staked'] += amount
    bot.reply_to(message, f"You have staked {amount} FOXCOIN.")

# Command /unstake
@bot.message_handler(commands=['unstake'])
def unstake_tokens(message):
    staked = users[message.chat.id]['staked']
    bot.reply_to(message, f"You have {staked} FOXCOIN staked. How much do you want to withdraw?")

@bot.message_handler(func=lambda message: message.text.isdigit())
def handle_unstake(message):
    amount = int(message.text)
    if amount <= users[message.chat.id]['staked']:
        users[message.chat.id]['staked'] -= amount
        bot.reply_to(message, f"You withdrew {amount} FOXCOIN.")
    else:
        bot.reply_to(message, "You don't have enough FOXCOIN staked.")

# Command /balance
@bot.message_handler(commands=['balance'])
def send_balance(message):
    staked = users[message.chat.id]['staked']
    bot.reply_to(message, f"Your FOXCOIN balance staked is {staked}.")

bot.polling()