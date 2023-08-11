from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Список вопросов и ответов
questions = [
    {
        'question': 'Вопрос 1: Какой язык программирования самый популярный?',
        'options': ['Python', 'Java', 'JavaScript', 'C++'],
        'answer': 0  # Индекс правильного ответа в списке options
    },
    {
        'question': 'Вопрос 2: Что такое REST?',
        'options': ['Архитектурный стиль', 'Программный язык', 'Библиотека', 'Операционная система'],
        'answer': 0
    },
    {
        'question': 'Вопрос 3: Какая команда используется для добавления файлов в Git репозиторий?',
        'options': ['git fetch', 'git add', 'git push', 'git commit'],
        'answer': 1
    },
    {
        'question': 'Вопрос 4: Что такое CSS?',
        'options': ['Язык программирования', 'Библиотека', 'Протокол', 'Технология стилей'],
        'answer': 3
    },
    {
        'question': 'Вопрос 5: Каково значение числа PI?',
        'options': ['3.14', '3.1415', '3.14159', '3.14159265359'],
        'answer': 3
    }
]

# Счетчик правильных ответов
correct_answers = 0


def start(update, context):
    global correct_answers
    update.message.reply_text("Привет! Я буду задавать тебе вопросы. Для каждого вопроса выбери правильный вариант ответа. Готов начать? Вот первый вопрос:")

    # Отправляем первый вопрос
    ask_question(update, context)

    # Обнуляем счетчик правильных ответов
    correct_answers = 0


def ask_question(update, context):
    # Получаем текущий номер вопроса
    question_number = len(context.chat_data)

    # Проверяем, были ли заданы все вопросы
    if question_number >= len(questions):
        # Все вопросы были заданы. Завершаем опрос и выводим результат
        complete_quiz(update, context)
        return

    # Получаем вопрос
    question = questions[question_number]['question']
    options = questions[question_number]['options']

    # Подготовка и отправка вопроса
    message = f"{question}\n"
    for i, option in enumerate(options):
        message += f"{i+1}. {option}\n"

    # Сохраняем правильный ответ в chat_data для последующей проверки
    context.chat_data['correct_answer'] = questions[question_number]['answer']

    update.message.reply_text(message)


def check_answer(update, context):
    global correct_answers
    # Получаем индекс ответа пользователя
    user_answer = int(update.message.text) - 1

    # Сравниваем ответ пользователя с правильным ответом
    if user_answer == context.chat_data['correct_answer']:
        correct_answers += 1

    # Переходим к следующему вопросу
    ask_question(update, context)


def complete_quiz(update, context):
    # Выводим результаты опроса
    update.message.reply_text(f"Опрос завершен! Количество правильных ответов: {correct_answers}")


def main():
    updater = Updater("6227021804:AAGhG8ktyHFGuTNlnOXBkpD_Fs68zjZl1gs", use_context=True)
    dp = updater.dispatcher

    # Обработчик команды /start
    dp.add_handler(CommandHandler("start", start))

    # Обработчик текстовых сообщений
    dp.add_handler(MessageHandler(Filters.text, check_answer))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()