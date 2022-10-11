import logging
from random import randint

from telegram import Bot, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters

bot_token = ''


def get_new_game_markup():
    keyboard = [[KeyboardButton('/new_game')]]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


def get_end_game_markup():
    keyboard = [[KeyboardButton('/end_game')]]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


def get_bot_turn(num):
    if num - 28 > 29 or num == 29:
        return randint(1, 28)
    else:
        return num - 29


def start(update, context):
    context.bot.send_message(
        update.effective_chat.id,
        '/new_game - начать новую игру\nМожно брать от 1 до 28 конфет за ход, '
        'побеждает тот, кто может забрать все оставшиеся конфеты',
        reply_markup=get_new_game_markup()
    )


def new_game(update, context):
    context.bot.send_message(
        update.effective_chat.id,
        'Введите количество конфет в кучке для игры',
        reply_markup=get_end_game_markup()
    )
    return 1


def end_game(update, context):
    context.bot.send_message(
        update.effective_chat.id,
        'Игра окончена досрочно /new_game - начать новую игру',
        reply_markup=get_new_game_markup()
    )
    return ConversationHandler.END


def start_game(update, context):
    try:
        context.chat_data['candies_count'] = int(update.message.text)
        context.chat_data['user'] = randint(1, 2)
        if context.chat_data['user'] == 1:
            context.bot.send_message(
                update.effective_chat.id,
                'Первый ход за Вами',
                reply_markup=get_end_game_markup()
            )
            return 2
        else:
            context.bot.send_message(
                update.effective_chat.id,
                'Бот ходит первым',
                reply_markup=get_end_game_markup()
            )
            return game(update, context)
    except ValueError:
        context.bot.send_message(
            update.effective_chat.id,
            'Пожалуйста, введите число',
            reply_markup=get_end_game_markup()
        )
        return 1


def check_end_game(update, context):
    if context.chat_data["candies_count"] <= 28:
        if context.chat_data['user'] == 1:
            message = 'Вы выиграли!'
        else:
            message = 'Вы проиграли'
        context.bot.send_message(
            update.effective_chat.id,
            message,
            reply_markup=get_new_game_markup()
        )
        return True
    return False


def game(update, context):
    if check_end_game(update, context):
        return ConversationHandler.END
    if context.chat_data['user'] == 1:
        try:
            user_turn = int(update.message.text)
            if 0 < int(user_turn) <= 28:
                context.chat_data['candies_count'] -= int(update.message.text)
                context.bot.send_message(
                    update.effective_chat.id,
                    f'В кучке осталось: {context.chat_data["candies_count"]}',
                    reply_markup=get_end_game_markup()
                )
                context.chat_data['user'] = 2
                return game(update, context)
            else:
                raise ValueError
        except ValueError:
            context.bot.send_message(
                update.effective_chat.id,
                'Пожалуйста, введите число от 1 до 28',
                reply_markup=get_end_game_markup()
            )
    else:
        bot_turn = get_bot_turn(context.chat_data['candies_count'])
        context.chat_data['candies_count'] -= bot_turn
        context.bot.send_message(
            update.effective_chat.id,
            f'Бот решил взять: {bot_turn}\nВ кучке осталось: {context.chat_data["candies_count"]}',
            reply_markup=get_end_game_markup()
        )
        context.chat_data['user'] = 1
        if check_end_game(update, context):
            return ConversationHandler.END
    return 2


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )

    logger = logging.getLogger(__name__)

    bot = Bot(bot_token)
    updater = Updater(bot_token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    new_game_handler = ConversationHandler(
        entry_points=[CommandHandler('new_game', new_game)],
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, start_game)],
            2: [MessageHandler(Filters.text & ~Filters.command, game)],
        },
        fallbacks=[CommandHandler('end_game', end_game)]
    )

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(new_game_handler)

    updater.start_polling()
    updater.idle()
