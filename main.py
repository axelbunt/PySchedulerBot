import telebot
import datetime
from telebot.types import *

BOT_TOKEN = ""
NEW_TASK = '1'
GET_TASK = '2'
DELETE_TASK = '3'
GREETING_TEXT = "Этот бот-планировщик поможет вам запоминать ваши задачи на определенные дни.\n" \
                "Для подробной информации введите '/help'.\n" \
                "Автор: Алексей Б."
HELP_TEXT = f"Чтобы внести новую задачу, введите '/{NEW_TASK}', затем введите дату в формате " \
            "ДД.ММ.ГГГГ, затем введите формулировку задачи через пробел.\n" \
            f"Чтобы получить задачи на определнный день, сначала введите '/{GET_TASK}', затем " \
            "введите дату в формате ДД.ММ.ГГГГ через пробел.\n" \
            f"Чтобы удалить конкретную задачу на определенный день, введите '/{DELETE_TASK}', " \
            "затем дату в формате ДД.ММ.ГГГГ, затем изначальную формулировку задачи через пробел."
DATE_FORMAT = "%d.%m.%Y"


state = ''
date = ''
tasks = {}

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start_bot(message: Message) -> None:
    bot.send_message(message.from_user.id, GREETING_TEXT)
    bot.send_message(message.from_user.id, HELP_TEXT)


@bot.message_handler(commands=['help'])
def help_bot(message: Message) -> None:
    bot.send_message(message.from_user.id, HELP_TEXT)


@bot.message_handler(commands=[NEW_TASK])
def create_new_task(message: Message) -> None:
    command = message.text
    try:
        task_date = command.split()[1]
        task_begin_index = command.index(command.split()[2])
        task = command[task_begin_index:]
        if not date_is_right(task_date):
            bot.send_message(message.from_user.id, 'Введите дату в формате ДД.ММ.ГГГГ')
            return

        if task_date not in tasks:
            tasks[task_date] = []
        tasks[task_date].append(task)
        bot.send_message(message.from_user.id, 'Задача записана')
    except IndexError:
        bot.send_message(message.from_user.id, 'Введите дату и задачу')


@bot.message_handler(commands=[GET_TASK])
def get_task(message: Message) -> None:
    command = message.text.split()
    try:
        task_date = command[1]
        if not date_is_right(task_date):
            bot.send_message(message.from_user.id, 'Введите дату в формате ДД.ММ.ГГГГ')
            return

        if task_date in tasks and len(tasks[task_date]) != 0:
            tasks_text = task_date + '\n'
            for task in tasks[task_date]:
                tasks_text += '- ' + task + '\n'
            bot.send_message(message.from_user.id, tasks_text)
        else:
            bot.send_message(message.from_user.id, 'Задач на этот день нет')
    except IndexError:
        bot.send_message(message.from_user.id, 'Введите дату')


@bot.message_handler(commands=[DELETE_TASK])
def delete_task(message: Message) -> None:
    command = message.text
    try:
        task_date = command.split()[1]
        task_begin_index = command.index(command.split()[2])
        task = command[task_begin_index:]
        if not date_is_right(task_date):
            bot.send_message(message.from_user.id, 'Введите дату в формате ДД.ММ.ГГГГ')
            return

        if task in tasks[task_date]:
            tasks[task_date].remove(task)
            bot.send_message(message.from_user.id, 'Задача удалена')
        else:
            bot.send_message(message.from_user.id, 'Задача отсутствует')
    except IndexError:
        bot.send_message(message.from_user.id, 'Введите дату и задачу')


@bot.message_handler(content_types=['text'])
def prompt_for_correct_command(message: Message) -> None:
    bot.send_message(message.from_user.id, "Некорректный запрос. Для подробной информации "
                                           "введите /help.")


def date_is_right(message: str) -> bool:
    try:
        datetime.datetime.strptime(message, DATE_FORMAT)
        return True
    except ValueError:
        return False


bot.polling(none_stop=True, interval=0)
