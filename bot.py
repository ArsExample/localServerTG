import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

token = '5846510402:AAF2knMSpHRm_vCccht8mYERWkb40WE1M5Q'
password = "scam777"
authed_users = []

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def get_response(messageText, user):
    response = ''
    if not authed_users.__contains__(user):
        if messageText == password:
            authed_users.append(user)
            return 'Authorization successful'
        else:
            return 'You can\'t send commands, because you are unauthorized\nEnter a password to start sending commands'
    else:
        response = 'Not implemented yet'
    return response


def handle_messages(update: Update, context: CallbackContext) -> None:
    bot = context.bot
    message = update.message
    messageText = message.text
    user = message.from_user
    username = user.username

    print(f'Received a message from @{username} with text: {messageText}')
    response = get_response(messageText, user)
    bot.send_message(message.chat_id, response)


def main() -> None:
    """Start the bot."""
    print('Bot started')
    # Create the Updater and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_messages))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
