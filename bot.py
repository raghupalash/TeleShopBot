from telegram import Update, Message, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater, 
    CommandHandler, 
    ConversationHandler,
    CallbackQueryHandler, 
    CallbackContext,
)
import pandas
from sheet import get_sheet
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update: Update, context: CallbackContext):
    """Sends a message with three inline buttons attached."""
    first_set(update, type="initial")

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data.split("_")

    keyboard = [[InlineKeyboardButton(u"\U0001F61E back", callback_data="first_back")]]
    if data[0] == "first":
        second_set(query, data[1])
    elif data[0] == "second":
        third_set(query, data[1])
    elif data[0] == "third":
        fourth_set(query, data[1])

def first_set(message_object, type):
    # This function will be approached in two ways - one initially and one from backwards direction
    keyboard = [
        [InlineKeyboardButton(u"\U0001F3EA" + "shop", callback_data='first_shop')],
        [InlineKeyboardButton(u"\U00002754" + "FAQ", callback_data='first_faq')],
        [InlineKeyboardButton(u"\U0001F61E" + "exit", callback_data='first_back')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if type == "initial":
        message_object.message.reply_text("Welcome to my online shop!!\nWhat do you want to do?", reply_markup=reply_markup)
    else:
        message_object.edit_message_text("What do you want to do?", reply_markup=reply_markup)

def second_set(query, data):
    keyboard = [[InlineKeyboardButton(u"\U000023EA back", callback_data="second_back")]]
    if data == "shop":
        product_sheet = get_sheet('Telegram Shop', 0)
        df = pandas.DataFrame.from_dict(product_sheet.get_all_records())
    
        # Product Buttons
        for i, item in df["Product Name"].iteritems():
            keyboard.insert(i, [InlineKeyboardButton(item, callback_data=f"second_{item}")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("What do you want to buy?", reply_markup=reply_markup)

    elif data == "faq":
        questions = [
            "How does this shop work?\n",
            "How payment is done?\n",
            "Is this safe?\n",
        ]
        answers = [
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit\. Sed ante mi, feugiat sed vestibulum at, efficitur et est\. Lorem ipsum dolor sit amet, consectetur adipiscing elit\. Ut et placerat lacus\. Sed hendrerit, arcu lacinia dictum eleifend, nibh sem ullamcorper libero, ut molestie ipsum mauris nec lectus\. Proin blandit pulvinar augue eu accumsan. Proin lacinia pretium nisi ornare tincidunt. Donec venenatis nisl non porta tempor. Donec malesuada enim a enim auctor, et vulputate tortor mollis.\n",
            "Nam at hendrerit augue\. Sed congue viverra molestie\. Morbi consectetur mauris dui, sed feugiat magna finibus et\. Nunc tristique hendrerit nisi ac faucibus. Sed nec fringilla metus. Integer at nisi varius, lacinia est eget, efficitur arcu. In eget urna eu risus venenatis dictum ut sit amet tortor. Quisque eleifend hendrerit leo, quis varius leo imperdiet in. Nunc consequat ac lectus a interdum.\n",
            "Suspendisse ut turpis lorem. Aliquam volutpat hendrerit felis, ut congue turpis lacinia et. Maecenas sollicitudin id libero nec condimentum. Aenean porta felis eget mauris rutrum varius. Fusce sit amet dolor mi. Quisque posuere, lorem at malesuada commodo, leo diam pulvinar ante, dictum semper ex tortor vitae nunc. Pellentesque non mollis nunc, convallis auctor nibh. Sed orci libero, facilisis quis massa ac, egestas aliquet odio.\n",
        ]
        faq = zip(questions, answers)
        message = "*FAQ*\n\n"
        for question, answer in faq:
            message += f"*{question}* {answer} \n"

        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(message, parse_mode="markdown", reply_markup=reply_markup)
    elif data == "back":
        query.edit_message_text("Byee, thanks for visiting!")

def third_set(query, data):
    if data == "back":
        first_set(query, type="back")
    else:
        product_sheet = wb["Product"]
        
        message = f"*{data}*\nPrice - $20\n*description* - Suspendisse ut turpis lorem. Aliquam volutpat hendrerit felis, ut congue turpis lacinia et.\n"
        keyboard = [
            [InlineKeyboardButton(u"\U0001F4B2 buy", callback_data="third_buy")],
            [InlineKeyboardButton(u"\U000023EA back", callback_data="third_back")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(message, parse_mode="markdown", reply_markup=reply_markup)
def fourth_set(query, data):
    if data == "back":
        second_set(query, data="shop")

def main():
    updater = Updater(token="1982910780:AAGdFTAqcud7pC1p7zZdcVtxh-UgO177-xM")

    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    button_handler = CallbackQueryHandler(button)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(button_handler)

    updater.start_polling()

    updater.idle()

if __name__ == "__main__":
    main()