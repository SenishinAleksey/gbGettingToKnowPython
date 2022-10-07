import logging

from telegram import Bot, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters

import models.csv as csv
import models.workers_db as workers_db

workers_db.init()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

bot_token = ''
bot = Bot(bot_token)
updater = Updater(bot_token, use_context=True)
dispatcher = updater.dispatcher


def start(update, context, page=1):
    all_workers_list = workers_db.get_workers_list()
    context.chat_data['page'] = page
    workers_data = workers_db.get_workers_for_page(page, all_workers_list)
    context.chat_data['pages_count'] = workers_data['pages_count']
    workers_str_list = [f'{worker[0]}: {worker[1]} - {worker[2]}' for worker in workers_data['notes']]
    workers_str = '\n'.join(workers_str_list)
    keyboard = [
        [
            KeyboardButton('/next_page'),
        ],
        [
            KeyboardButton('/show_more'),
            KeyboardButton('/add_worker')
        ],
        [
            KeyboardButton('/find'),
            KeyboardButton('/export_csv')
        ]
    ]
    if page == workers_data['pages_count']:
        keyboard[0] = [KeyboardButton('/prev_page')]
    elif page > 1:
        keyboard[0].insert(0, KeyboardButton('/prev_page'))

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        one_time_keyboard=True,
        resize_keyboard=True,
        input_field_placeholder='Выберите пункт меню:'
    )
    context.bot.send_message(
        update.effective_chat.id,
        f'Список работников, страница {workers_data["page"]} из {workers_data["pages_count"]}\n{workers_str}',
        reply_markup=reply_markup
    )
    return ConversationHandler.END


def next_page(update, context):
    if context.chat_data['page'] < context.chat_data['pages_count']:
        start(update, context, page=context.chat_data['page'] + 1)
    else:
        context.bot.send_message(update.effective_chat.id, 'Такой страницы не существует')


def prev_page(update, context):
    if context.chat_data['page'] > 1:
        start(update, context, page=context.chat_data['page'] - 1)
    else:
        context.bot.send_message(update.effective_chat.id, 'Такой страницы не существует')


def get_start_reply_markup():
    keyboard = [[KeyboardButton('/start')]]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


def show_more_id_request(update, context):
    context.bot.send_message(update.effective_chat.id, 'Введите номер работника', reply_markup=get_start_reply_markup())
    return 1


def show_more(update, context):
    try:
        worker_id = int(update.message.text)
        worker_data = workers_db.get_worker_data(worker_id)
        context.chat_data['worker_id'] = worker_id
        context.chat_data['worker_data'] = worker_data
        worker_data_str_list = [
            f'ИД: {worker_data["id"]}',
            f'Имя: {worker_data["last_name"]} {worker_data["name"]}',
            f'Должность: {worker_data["position"]}',
            f'Рабочий телефон: {worker_data["work_phone"]}',
            f'Год рождения: {worker_data["year_of_birth"]}',
            f'Оклад: {worker_data["salary"]} руб.'
        ]
        worker_data_str = '\n'.join(worker_data_str_list)
        keyboard = [[KeyboardButton('/delete_worker'), KeyboardButton('/edit_worker')], [KeyboardButton('/start')]]
        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )
        context.bot.send_message(
            update.effective_chat.id,
            f'Данные о работнике:\n{worker_data_str}',
            reply_markup=reply_markup
        )
    except (ValueError, Warning):
        context.bot.send_message(update.effective_chat.id, 'Некорректный номер работника',
                                 reply_markup=get_start_reply_markup())
    return ConversationHandler.END


def delete_worker(update, context):
    worker_id = context.chat_data['worker_id']
    try:
        workers_db.delete(worker_id)
    except Warning as mes:
        context.bot.send_message(update.effective_chat.id, mes)
    start(update, context)
    return ConversationHandler.END


def edit_worker_last_name_request(update, context):
    context.chat_data['new_worker_data'] = {
        'id': context.chat_data['worker_id']
    }
    context.chat_data['mode'] = 'edit_worker'
    context.bot.send_message(update.effective_chat.id, 'Введите фамилию', reply_markup=get_start_reply_markup())
    return 1


def add_worker_last_name_request(update, context):
    context.chat_data['new_worker_data'] = {}
    context.chat_data['mode'] = 'add_worker'
    context.bot.send_message(update.effective_chat.id, 'Введите фамилию', reply_markup=get_start_reply_markup())
    return 1


def name_request(update, context):
    context.chat_data['new_worker_data']['last_name'] = update.message.text
    context.bot.send_message(update.effective_chat.id, 'Введите имя', reply_markup=get_start_reply_markup())
    return 2


def year_of_birth_request(update, context):
    context.chat_data['new_worker_data']['name'] = update.message.text
    context.bot.send_message(update.effective_chat.id, 'Введите год рождения', reply_markup=get_start_reply_markup())
    return 3


def position_request(update, context):
    context.chat_data['new_worker_data']['year_of_birth'] = update.message.text
    context.bot.send_message(update.effective_chat.id, 'Введите должность', reply_markup=get_start_reply_markup())
    return 4


def work_phone_request(update, context):
    context.chat_data['new_worker_data']['position'] = update.message.text
    context.bot.send_message(update.effective_chat.id, 'Введите рабочий телефон', reply_markup=get_start_reply_markup())
    return 5


def salary_request(update, context):
    context.chat_data['new_worker_data']['work_phone'] = update.message.text
    context.bot.send_message(update.effective_chat.id, 'Введите оклад', reply_markup=get_start_reply_markup())
    return 6


def add_or_edit_worker(update, context):
    try:
        if context.chat_data['mode'] == 'edit_worker':
            context.chat_data['new_worker_data']['salary'] = update.message.text
            workers_db.edit(context.chat_data['new_worker_data'])
            context.bot.send_message(update.effective_chat.id, 'Работник изменен')
            show_more(update, context)
        elif context.chat_data['mode'] == 'add_worker':
            last_name = context.chat_data['new_worker_data']['last_name']
            name = context.chat_data['new_worker_data']['name']
            year_of_birth = context.chat_data['new_worker_data']['year_of_birth']
            position = context.chat_data['new_worker_data']['position']
            work_phone = context.chat_data['new_worker_data']['work_phone']
            salary = update.message.text
            workers_db.add(last_name, name, year_of_birth, position, work_phone, salary)
            context.bot.send_message(update.effective_chat.id, 'Работник добавлен')
            start(update, context)
    except Warning as mes:
        context.bot.send_message(update.effective_chat.id, mes)
        start(update, context)
    return ConversationHandler.END


def export_csv(update, context):
    file_name = 'tg_bot_workers.csv'
    workers_db.export_workers(file_name, csv.write)
    context.bot.send_document(update.effective_chat.id, document=open(file_name, 'rb'))


def find(update, context):
    try:
        workers_data = workers_db.search(context.chat_data['find_mode'], update.message.text)
        workers_str_list = [f'{worker[0]}: {worker[1]} - {worker[2]}' for worker in workers_data]
        workers_str = '\n'.join(workers_str_list)
        context.bot.send_message(
            update.effective_chat.id,
            f'Результаты поиска:\n{workers_str}',
            reply_markup=get_start_reply_markup()
        )
    except Warning as mes:
        context.bot.send_message(update.effective_chat.id, mes, reply_markup=get_start_reply_markup())
    return ConversationHandler.END


def find_query_request(update, context):
    context.chat_data['find_mode'] = update.message.text[1:]
    context.bot.send_message(update.effective_chat.id, 'Введите текст для поиска', reply_markup=get_start_reply_markup())
    return 2


def find_mode_request(update, context):
    keyboard = [
        [
            KeyboardButton('/last_name'),
            KeyboardButton('/name'),
        ],
        [
            KeyboardButton('/year_of_birth'),
            KeyboardButton('/position')
        ],
        [
            KeyboardButton('/work_phone'),
            KeyboardButton('/start')
        ]
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )
    context.bot.send_message(update.effective_chat.id, 'Выберите параметр для поиска', reply_markup=reply_markup)
    return 1


start_handler = CommandHandler('start', start)
next_page_handler = CommandHandler('next_page', next_page)
prev_page_handler = CommandHandler('prev_page', prev_page)
delete_worker_handler = CommandHandler('delete_worker', delete_worker)
edit_worker_handler = CommandHandler('edit_worker', edit_worker_last_name_request)
export_csv_handler = CommandHandler('export_csv', export_csv)
show_more_handler = ConversationHandler(
    entry_points=[CommandHandler('show_more', show_more_id_request)],
    states={
        1: [MessageHandler(Filters.text & ~Filters.command, show_more)],
    },
    fallbacks=[start_handler, delete_worker_handler, edit_worker_handler]
)
add_edit_worker_handler = ConversationHandler(
    entry_points=[
        CommandHandler('add_worker', add_worker_last_name_request),
        edit_worker_handler
    ],
    states={
        1: [MessageHandler(Filters.text & ~Filters.command, name_request)],
        2: [MessageHandler(Filters.text & ~Filters.command, year_of_birth_request)],
        3: [MessageHandler(Filters.text & ~Filters.command, position_request)],
        4: [MessageHandler(Filters.text & ~Filters.command, work_phone_request)],
        5: [MessageHandler(Filters.text & ~Filters.command, salary_request)],
        6: [MessageHandler(Filters.text & ~Filters.command, add_or_edit_worker)]
    },
    fallbacks=[start_handler]
)
find_handler = ConversationHandler(
    entry_points=[CommandHandler('find', find_mode_request)],
    states={
        1: [
            CommandHandler('last_name', find_query_request),
            CommandHandler('name', find_query_request),
            CommandHandler('year_of_birth', find_query_request),
            CommandHandler('position', find_query_request),
            CommandHandler('work_phone', find_query_request),
        ],
        2: [MessageHandler(Filters.text & ~Filters.command, find)]
    },
    fallbacks=[start_handler]
)

dispatcher.add_handler(show_more_handler)
dispatcher.add_handler(add_edit_worker_handler)
dispatcher.add_handler(find_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(next_page_handler)
dispatcher.add_handler(prev_page_handler)
dispatcher.add_handler(edit_worker_handler)
dispatcher.add_handler(delete_worker_handler)
dispatcher.add_handler(export_csv_handler)

updater.start_polling()
updater.idle()
