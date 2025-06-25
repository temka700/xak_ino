import telebot
from telebot import types
import time

TOKEN = "7931894873:AAHn2WYyn-Ix83qm2LPp0oaKEJIHYEIXueg"
bot = telebot.TeleBot(TOKEN)

questions = [
    {
        'text': '🧐 Что вам ближе?',
        'options': [
            {'text': '🛠 Решать технические задачи', 'weights': [2, 0, 0]},
            {'text': '📚 Изучать литературу и языки', 'weights': [0, 2, 0]},
            {'text': '🤝 Общаться и помогать людям', 'weights': [0, 0, 2]},
        ]
    },
    {
        'text': '🎯 Какую деятельность предпочитаете?',
        'options': [
            {'text': '💻 Работа с техникой и цифрами', 'weights': [2, 0, 0]},
            {'text': '🎨 Творческое самовыражение', 'weights': [0, 2, 0]},
            {'text': '📋 Организация и управление людьми', 'weights': [0, 0, 2]},
        ]
    },
    {
        'text': '🏢 Какой формат работы вам подходит?',
        'options': [
            {'text': '🏭 Компания', 'weights': [2, 0, 0]},
            {'text': '🏠 Фриланс', 'weights': [0, 2, 0]},
            {'text': '🚀 Собственный бизнес', 'weights': [0, 0, 2]},
        ]
    },
    {
        'text': '📖 Какой предмет в школе вам нравится больше всего?',
        'options': [
            {'text': '📐 Математика и физика', 'weights': [2, 0, 0]},
            {'text': '📜 История и литература', 'weights': [0, 2, 0]},
            {'text': '🧠 Обществознание и психология', 'weights': [0, 0, 2]},
        ]
    },
    {
        'text': '🧩 Как вы предпочитаете решать проблемы?',
        'options': [
            {'text': '🧮 Логически и системно', 'weights': [2, 0, 0]},
            {'text': '🎭 Интуитивно и творчески', 'weights': [0, 2, 0]},
            {'text': '🤗 Совместно с другими людьми', 'weights': [0, 0, 2]},
        ]
    },
    {
        'text': '🌟 Какая атмосфера работы вам ближе?',
        'options': [
            {'text': '📏 Чёткие правила и структура', 'weights': [2, 0, 0]},
            {'text': '🎉 Свобода выражения и креатив', 'weights': [0, 2, 0]},
            {'text': '👥 Командная работа и поддержка', 'weights': [0, 0, 2]},
        ]
    },
    {
        'text': '🏆 Что вы цените больше всего в работе?',
        'options': [
            {'text': '⚙️ Технический прогресс и инновации', 'weights': [2, 0, 0]},
            {'text': '📖 Культурное развитие и знания', 'weights': [0, 2, 0]},
            {'text': '🌍 Влияние на общество и помощь людям', 'weights': [0, 0, 2]},
        ]
    },
]

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

university_info = {
    "МГТУ им. Баумана": "МГТУ им. Баумана — ведущий технический университет России.",
    "СПбГПУ": "СПбГПУ — сильный технический вуз с широким спектром инженерных направлений.",
    "НИУ ВШЭ": "НИУ ВШЭ — один из лучших вузов России с сильным IT-направлением.",
    "МФТИ": "МФТИ — известен подготовкой специалистов в области физики и математики.",
    "МГУ": "МГУ — крупнейший университет России с сильным гуманитарным факультетом.",
    "ВШЭ": "ВШЭ — ведущий вуз в области экономики, социальных и гуманитарных наук.",
    "СПбГУ": "СПбГУ — старейший университет России с богатыми традициями.",
    "РГГУ": "РГГУ — специализируется на гуманитарных и культурологических направлениях.",
    "РАНХиГС": "РАНХиГС — лидер в подготовке управленческих кадров для госслужбы.",
    "МГПУ": "МГПУ — педагогический университет с сильными социальными программами.",
    "МГУП": "МГУП — социально ориентированный вуз с программами по социальной работе.",
    "МГЮА": "МГЮА — ведущий юридический вуз России.",
}

user_data = {}

@bot.message_handler(commands=['start', 'help'])
def start(message):
    text = (
        "👋 Привет! Я помогу тебе определиться с профориентацией и выбором вуза.\n\n"
        "🔹 Нажми «Пройти тест», чтобы начать.\n"
        "🔹 Нажми «Посмотреть результат», чтобы увидеть последний результат.\n"
        "🔹 Если хочешь пройти тест снова — просто нажми «Пройти тест».\n\n"
        "ℹ️ТУТ МОЖНО ПОСМОТРЕТЬ 👁➡ <a href=\"https://studywithshaiba.tilda.ws/\">наш сайт</a>."
    )
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_test = types.InlineKeyboardButton("🚀 Пройти тест", callback_data='start_test')
    btn_result = types.InlineKeyboardButton("📊 Посмотреть результат", callback_data='view_result')
    markup.add(btn_test, btn_result)
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id

    if call.data == 'start_test':
        markup = types.InlineKeyboardMarkup(row_width=2)
        ages = ['менее 18', '18-22', '23-30', '31+']
        for age in ages:
            btn = types.InlineKeyboardButton(age, callback_data=f'age_{age}')
            markup.add(btn)
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "👶 Выберите, сколько вам лет:", reply_markup=markup)

    elif call.data.startswith('age_'):
        age = call.data[4:]
        user_data[user_id] = {'age': age, 'answers': [], 'current_q': 0}
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, f"👍 Вы выбрали возраст: {age}. Начинаем тест!")
        time.sleep(1)
        send_question(call.message.chat.id, user_id)

    elif call.data == 'view_result':
        bot.answer_callback_query(call.id)
        if user_id in user_data and 'result' in user_data[user_id]:
            send_final_result(call.message.chat.id, user_data[user_id]['result'])
        else:
            bot.send_message(call.message.chat.id, "⚠️ Вы ещё не проходили тест. Пожалуйста, сначала пройдите тест.")

    elif call.data.startswith('answer_'):
        answer_index = int(call.data.split('_')[1])
        if user_id in user_data:
            user_data[user_id]['answers'].append(answer_index)
            user_data[user_id]['current_q'] += 1
            bot.answer_callback_query(call.id)

            if user_data[user_id]['current_q'] < len(questions):
                time.sleep(1)
                send_question(call.message.chat.id, user_id)
            else:
                result_profile = analyze_answers(user_data[user_id]['answers'])
                user_data[user_id]['result'] = result_profile
                send_final_result(call.message.chat.id, result_profile)

    elif call.data == 'university_info':
        # Показываем информацию по вузу
        # Для простоты покажем первый вуз из списка профиля, можно расширить логику
        if user_id in user_data and 'result' in user_data[user_id]:
            profile = user_data[user_id]['result']
            # Покажем инфо по первому вузу из списка
            uni_name = universities[profile][0][0]
            info = university_info.get(uni_name, "Информация о вузе недоступна.")
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, f"🏫 {uni_name}:\n{info}")
        else:
            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id, "⚠️ Сначала пройдите тест, чтобы получить информацию о вузах.")

def send_question(chat_id, user_id):
    q_index = user_data[user_id]['current_q']
    question = questions[q_index]
    markup = types.InlineKeyboardMarkup(row_width=1)
    for i, option in enumerate(question['options']):
        btn = types.InlineKeyboardButton(option['text'], callback_data=f'answer_{i}')
        markup.add(btn)
    bot.send_message(chat_id, f"❓ Вопрос {q_index + 1} из {len(questions)}:\n\n{question['text']}", reply_markup=markup)

def analyze_answers(answers):
    scores = [0, 0, 0]
    for q_index, ans_index in enumerate(answers):
        weights = questions[q_index]['options'][ans_index]['weights']
        for i in range(len(scores)):
            scores[i] += weights[i]
    max_score = max(scores)
    profile_index = scores.index(max_score)
    return profile_index

def send_final_result(chat_id, profile_index):
    profiles_desc = {
        0: "🛠 Вы склонны к техническим специальностям.",
        1: "📚 Вы склонны к гуманитарным специальностям.",
        2: "🤝 Вы склонны к социальным специальностям."
    }
    bot.send_message(chat_id, profiles_desc[profile_index])

    markup = types.InlineKeyboardMarkup(row_width=1)
    for uni, faculty in universities[profile_index]:
        btn = types.InlineKeyboardButton(f"{uni} - {faculty}", callback_data='university_info')
        markup.add(btn)
    bot.send_message(chat_id, "🎓 Рекомендуемые вузы и направления:", reply_markup=markup)

if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)
