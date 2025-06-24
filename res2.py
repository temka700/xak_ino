import telebot
from telebot import types

TOKEN = "7931894873:AAHn2WYyn-Ix83qm2LPp0oaKEJIHYEIXueg"
bot = telebot.TeleBot(TOKEN)

# Вопросы и варианты с весами по типам (0 - технарь, 1 - гуманитарий, 2 - социальный)
questions = [
    {
        'text': 'Что вам ближе?',
        'options': [
            {'text': 'Решать технические задачи', 'weights': [2, 0, 0]},
            {'text': 'Изучать литературу и языки', 'weights': [0, 2, 0]},
            {'text': 'Общаться и помогать людям', 'weights': [0, 0, 2]},
        ]
    },
    {
        'text': 'Какую деятельность предпочитаете?',
        'options': [
            {'text': 'Работа с техникой и цифрами', 'weights': [2, 0, 0]},
            {'text': 'Творческое самовыражение', 'weights': [0, 2, 0]},
            {'text': 'Организация и управление людьми', 'weights': [0, 0, 2]},
        ]
    },
    {
        'text': 'Какой формат работы вам подходит?',
        'options': [
            {'text': 'Компания', 'weights': [2, 0, 0]},
            {'text': 'Фриланс', 'weights': [0, 2, 0]},
            {'text': 'Собственный бизнес', 'weights': [0, 0, 2]},
        ]
    },
    {
        'text': 'Какой предмет в школе вам нравится больше всего?',
        'options': [
            {'text': 'Математика и физика', 'weights': [2, 0, 0]},
            {'text': 'История и литература', 'weights': [0, 2, 0]},
            {'text': 'Обществознание и психология', 'weights': [0, 0, 2]},
        ]
    },
    {
        'text': 'Как вы предпочитаете решать проблемы?',
        'options': [
            {'text': 'Логически и системно', 'weights': [2, 0, 0]},
            {'text': 'Интуитивно и творчески', 'weights': [0, 2, 0]},
            {'text': 'Совместно с другими людьми', 'weights': [0, 0, 2]},
        ]
    },
    {
        'text': 'Какая атмосфера работы вам ближе?',
        'options': [
            {'text': 'Чёткие правила и структура', 'weights': [2, 0, 0]},
            {'text': 'Свобода выражения и креатив', 'weights': [0, 2, 0]},
            {'text': 'Командная работа и поддержка', 'weights': [0, 0, 2]},
        ]
    },
    {
        'text': 'Что вы цените больше всего в работе?',
        'options': [
            {'text': 'Технический прогресс и инновации', 'weights': [2, 0, 0]},
            {'text': 'Культурное развитие и знания', 'weights': [0, 2, 0]},
            {'text': 'Влияние на общество и помощь людям', 'weights': [0, 0, 2]},
        ]
    },
]

# Вузы и направления по профилям
universities = {
    0: [("МГТУ им. Баумана", "Факультет информатики и вычислительной техники"),
        ("СПбГПУ", "Факультет прикладной математики и механики"),
        ("НИУ ВШЭ", "Факультет компьютерных наук"),
        ("МФТИ", "Факультет физики и технологий")],
    1: [("МГУ", "Факультет филологии"),
        ("ВШЭ", "Факультет гуманитарных наук"),
        ("СПбГУ", "Факультет истории"),
        ("РГГУ", "Факультет культурологии")],
    2: [("РАНХиГС", "Факультет государственного управления"),
        ("МГПУ", "Педагогический факультет"),
        ("МГУП", "Факультет социальной работы"),
        ("МГЮА", "Юридический факультет")],
}

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=5)
    ages = ['менее 18', '18-22', '23-30', '31+']
    for age in ages:
        btn = telebot.types.InlineKeyboardButton(age, callback_data='start_test')
        markup.add(btn)
    bot.send_message(message.chat.id, "Привет! Выберите, сколько тебе лет:", reply_markup=markup)

    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_test = types.InlineKeyboardButton("Пройти тест", callback_data='start_test')
    btn_result = types.InlineKeyboardButton("Посмотреть результат", callback_data='view_result')
    markup.add(btn_test, btn_result)
    bot.send_message(message.chat.id, "Привет! Выбери действие:", reply_markup=markup)



@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id

    if call.data == 'start_test':
        user_data[user_id] = {'answers': [], 'current_q': 0}
        bot.answer_callback_query(call.id)
        send_question(call.message.chat.id, user_id)

    elif call.data == 'view_result':
        bot.answer_callback_query(call.id)
        if user_id in user_data and 'result' in user_data[user_id]:
            send_final_result(call.message.chat.id, user_data[user_id]['result'])
        else:
            bot.send_message(call.message.chat.id, "Вы ещё не проходили тест.")

    elif call.data.startswith('answer_'):
        answer_index = int(call.data.split('_')[1])
        if user_id in user_data:
            current_q = user_data[user_id]['current_q']
            user_data[user_id]['answers'].append(answer_index)
            user_data[user_id]['current_q'] += 1
            bot.answer_callback_query(call.id)

            if user_data[user_id]['current_q'] < len(questions):
                send_question(call.message.chat.id, user_id)
            else:
                # Анализ результатов
                result_profile = analyze_answers(user_data[user_id]['answers'])
                user_data[user_id]['result'] = result_profile
                send_final_result(call.message.chat.id, result_profile)
                # Можно сохранить или очистить данные, если нужно

def send_question(chat_id, user_id):
    q_index = user_data[user_id]['current_q']
    question = questions[q_index]
    markup = types.InlineKeyboardMarkup(row_width=1)
    for i, option in enumerate(question['options']):
        btn = types.InlineKeyboardButton(option['text'], callback_data=f'answer_{i}')
        markup.add(btn)
    bot.send_message(chat_id, question['text'], reply_markup=markup)

def analyze_answers(answers):
    # Суммируем веса по профилям
    scores = [0, 0, 0]
    for q_index, ans_index in enumerate(answers):
        weights = questions[q_index]['options'][ans_index]['weights']
        for i in range(len(scores)):
            scores[i] += weights[i]
    # Определяем профиль с максимальным баллом
    max_score = max(scores)
    profiles = ['Технический профиль', 'Гуманитарный профиль', 'Социальный профиль']
    profile_index = scores.index(max_score)
    return profile_index

def send_final_result(chat_id, profile_index):
    profiles_desc = {
        0: "Вы склонны к техническим специальностям.",
        1: "Вы склонны к гуманитарным специальностям.",
        2: "Вы склонны к социальным специальностям."
    }
    bot.send_message(chat_id, profiles_desc[profile_index])

    # Предлагаем вуз и направления
    markup = types.InlineKeyboardMarkup(row_width=1)
    for uni, faculty in universities[profile_index]:
        btn = types.InlineKeyboardButton(f"{uni} - {faculty}", callback_data='university_info')
        markup.add(btn)
    bot.send_message(chat_id, "Рекомендуемые вузы и направления:", reply_markup=markup)

if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)
