import os

import PythonDatabase
import telebot
import buttons
from datetime import datetime
import time
from dotenv import load_dotenv


load_dotenv()
API_KEY = str(os.getenv('API_KEY'))
bot = telebot.TeleBot(API_KEY)

# To store user details until it is being added to the database file
user_data = {}

# To store message_ids of the incorrect User messages and Error handling bot messages
list_of_messages = []


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # START # # # # # # # # # # # # # # # # # # # # # # # # # # #
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_full_name = PythonDatabase.check_if_user_registered(user_id)
    if user_full_name:
        bot.send_message(user_id, f'Welcome back {user_full_name[0]} {user_full_name[1]}!\n\n'
                                  f'How can I help you?',
                         reply_markup=buttons.main_menu_buttons())
        bot.register_next_step_handler(message, main_menu)

    else:
        bot.send_message(user_id, 'Welcome to the Task Manager bot!\n\n'
                                  'Please sign up !', reply_markup=buttons.sign_up())
        bot.register_next_step_handler(message, user_registration)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # Registration  # # # # # # # # # # # # # # # # # # # # # # # # #

def user_registration(message):
    user_id = message.from_user.id
    if message.text == '✅ Sign up':
        user_data['user_id'] = user_id
        delete_error_messages(user_id)  # Deleting unnecessary messages
        bot.send_message(user_id, 'Please type in your First Name 💬',
                         reply_markup=buttons.cancel())
        bot.register_next_step_handler(message, get_first_name)
    else:
        user_response = message.message_id
        list_of_messages.append(user_response)
        bot_response = bot.send_message(user_id, '🔽 Please sign up by clicking the button below! 🔽',
                                        reply_markup=buttons.sign_up())
        list_of_messages.append(bot_response.message_id)
        bot.register_next_step_handler(message, user_registration)


def get_first_name(message):
    user_id = message.from_user.id
    if message.text == '❌ Cancel':
        cancel_button_registration(message, user_id)
    else:
        if message.text.isalpha():
            delete_error_messages(user_id)  # Deleting unnecessary messages

            first_name = message.text.capitalize()
            user_data['first_name'] = first_name
            print(user_data)
            bot.send_message(user_id, 'Please type in your Last Name 💬', reply_markup=buttons.cancel())
            bot.register_next_step_handler(message, get_last_name)
        else:
            user_response = message.message_id
            list_of_messages.append(user_response)
            bot_response = bot.send_message(user_id, '❌ Error invalid First Name! ❌\n\n'
                                                     '🔄 Please try again to type in your First Name 🔄')
            list_of_messages.append(bot_response.message_id)
            bot.register_next_step_handler(message, get_first_name)


def get_last_name(message):
    user_id = message.from_user.id
    if message.text == '❌ Cancel':
        cancel_button_registration(message, user_id)
    else:
        if message.text.isalpha():
            delete_error_messages(user_id)  # Deleting unnecessary messages

            last_name = message.text.capitalize()
            user_data['last_name'] = last_name
            print(user_data)
            bot.send_message(user_id, 'Please type in your Email Address 📩', reply_markup=buttons.cancel())
            bot.register_next_step_handler(message, get_email_address)
        else:
            user_response = message.message_id
            list_of_messages.append(user_response)

            bot_response = bot.send_message(user_id, ' ❌ Error invalid Last Name! ❌\n\n'
                                                     '🔄 Please try again to type in your Last Name 🔄')
            list_of_messages.append(bot_response.message_id)
            bot.register_next_step_handler(message, get_last_name)


def get_email_address(message):
    user_id = message.from_user.id
    email_address = message.text.strip()
    parts = email_address.split('.')
    if message.text == '❌ Cancel':
        cancel_button_registration(message, user_id)
    else:
        if '@' in email_address and not email_address.startswith('@') and not email_address.endswith('@') \
                and email_address.count('@') == 1 and ".." not in email_address and not email_address.startswith('.') \
                and not email_address.endswith('.') and '.' in email_address.split('@')[-1] and parts[-1].isalpha() \
                and len(parts[-1]) >= 2:

            delete_error_messages(user_id)  # Deleting unnecessary messages

            user_data['email_address'] = email_address
            print(user_data)
            bot.send_message(user_id, 'Please share your contact 📞',
                             reply_markup=buttons.share_my_phone_number())
            bot.register_next_step_handler(message, get_phone_number)
        else:
            user_response = message.message_id
            list_of_messages.append(user_response)

            bot_response = bot.send_message(user_id, '❌ Error invalid email address! ❌\n\n'
                                                     '🔄 Please try again to type in your Email Address 🔄')
            list_of_messages.append(bot_response.message_id)
            bot.register_next_step_handler(message, get_email_address)


def get_phone_number(message):
    user_id = message.chat.id
    if message.text == '❌ Cancel':
        cancel_button_registration(message, user_id)
    elif message.contact:

        delete_error_messages(user_id)  # Deleting unnecessary messages

        phone_number = '+' + message.contact.phone_number
        user_data['phone_number'] = phone_number
        bot.send_message(user_id, f'🎉🎉🎉 Congratulations, {user_data['last_name']} {user_data['first_name']}  🎉🎉🎉\n\n'
                                  f'You have successfully signed up to the Task Manager bot ✅',
                         reply_markup=buttons.main_menu_buttons())

        # Adding user to the Database
        PythonDatabase.add_user(user_data)

        bot.register_next_step_handler(message, main_menu)
        list_of_messages.clear()
        user_data.clear()
    else:
        user_response = message.message_id
        list_of_messages.append(user_response)

        bot_response = bot.send_message(user_id, ' 🔽 Please share contact by button below! 🔽')
        list_of_messages.append(bot_response.message_id)
        bot.register_next_step_handler(message, get_phone_number)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # Main Menu # # # # # # # # # # # # # # # # # # # # # # # # # # #

def main_menu(message):
    user_id = message.chat.id
    if message.text == '🆕 Create Task':
        delete_error_messages(user_id)  # Deleting unnecessary messages
        bot.send_message(user_id, "📜 Once a task is just begun, never leave it till it's done."
                                  " Be the labour great or small, do it well or not at all\n\n"
                                  "In Creating task you can set:\n\n"
                                  "✏️ Title:\n"
                                  "📃 Description:\n"
                                  "⏰ Reminder date:\n"
                                  "✨ Category:\n"
                                  "📅 Creation date\n\n"
                                  "Please type in task title 💬", reply_markup=buttons.cancel())
        bot.register_next_step_handler(message, task_title)
    elif message.text == '📋 View Tasks':
        delete_error_messages(user_id)  # Deleting unnecessary messages
        view_all_tasks = PythonDatabase.view_all_tasks(user_id)
        if view_all_tasks:
            header = '📜 Be like a postage stamp, stick to one thing until you get there.\n\n '
            header += 'ALl tasks details:'
            text_str = ''
            for index, task in enumerate(view_all_tasks, start=1):
                category_name = PythonDatabase.getting_category_name_by_id(user_id, task[6])
                category_name = category_name[0]
                created_date_str = datetime.strptime(task[4], '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d')
                created_time_str = datetime.strptime(task[4], '%Y-%m-%d %H:%M:%S.%f').strftime('%H:%M %p')
                if task[5] is not None:
                    reminder_date_str = datetime.strptime(task[5], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                    reminder_time_str = datetime.strptime(task[5], '%Y-%m-%d %H:%M:%S').strftime('%H:%M %p')
                else:
                    reminder_date_str = 'NULL'
                    reminder_time_str = 'NULL'

                text_str += (f'\n\n#️⃣ ID: {index}\n'
                             f'✏️ Title: {task[2]}\n'
                             f'📃 Description: {task[3]}\n'
                             f'⏰ Reminder date: {reminder_date_str};  ⌚️ Time: {reminder_time_str}\n'
                             f'✨ Category: {category_name}\n'
                             f'📅 Created day: {created_date_str}; ⌚️ Time; {created_time_str}\n'
                             f'{"-" * 100}')
            bot.send_message(user_id, f'{header} {text_str}', reply_markup=buttons.view_tasks_menu())
            bot.register_next_step_handler(message, view_tasks_menu)
        else:
            no_tasks_found(message, user_id)
    elif message.text == '🗂️ Task Utilities':
        delete_error_messages(user_id)  # Deleting unnecessary messages
        bot.send_message(user_id, f'🔽 Please use buttons below 🔽', reply_markup=buttons.utilities())
        bot.register_next_step_handler(message, utilities_menu)
    elif message.text == '👤️ Edit Profile':
        delete_error_messages(user_id)  # Deleting unnecessary messages
        bot.send_message(user_id, f'🔽 Please use the buttons below to update your details 🔽',
                         reply_markup=buttons.edit_profile())
        bot.register_next_step_handler(message, edit_profile_menu)

    else:
        user_response = message.message_id
        list_of_messages.append(user_response)
        user_full_name = PythonDatabase.check_if_user_registered(user_id)
        if user_full_name:
            bot_response = bot.send_message(user_id, f'🔽 Please, {user_full_name[0]} {user_full_name[1]} '
                                                     f'use buttons below! 🔽')
        else:
            bot_response = bot.send_message(user_id, f'🔽 Please use buttons below! 🔽')
        list_of_messages.append(bot_response.message_id)
        bot.register_next_step_handler(message, main_menu)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # Task adding # # # # # # # # # # # # # # # # # # # # # # # # # #


def task_title(message):
    user_id = message.chat.id
    if message.text == '❌ Cancel':
        cancel_button_task(message, user_id)
    else:
        user_data['user_id'] = user_id
        user_data['task_name'] = message.text
        bot.send_message(user_id, "✅ Task title is successfully saved\n\n"
                                  "Please type in description 💬", reply_markup=buttons.cancel())
        bot.register_next_step_handler(message, task_description, user_id)


def task_description(message, user_id):
    if message.text == '❌ Cancel':
        cancel_button_task(message, user_id)
    else:
        user_data['task_description'] = message.text
        bot.send_message(user_id, "✅ Task description is successfully saved\n\n"
                                  "Do you want to set reminder ❓", reply_markup=buttons.reminder())
        bot.register_next_step_handler(message, reminder)


def reminder(message):
    user_id = message.chat.id
    today_date = datetime.now()
    user_data['task_creation_date'] = today_date
    if message.text == '✅ YES':
        delete_error_messages(user_id)  # Deleting unnecessary messages
        bot.send_message(user_id, '⏰ Setting reminder:\n\n'
                                  '📅 Reminder date(YYYY-MM-DD):\n'
                                  '⌚️ Reminder time(HH:mm):\n\n'
                                  'Please first enter the reminder date  (e.g., YYYY-MM-DD) 💬',
                         reply_markup=buttons.cancel())
        bot.register_next_step_handler(message, process_reminder_date)
    elif message.text == '❌ NO':
        delete_error_messages(user_id)  # Deleting unnecessary messages
        bot.send_message(user_id, '⏰Reminder is not set\n\n'
                                  '🔽 Category buttons 🔽', reply_markup=buttons.category_choose())
        bot.register_next_step_handler(message, category_variants)
    else:
        user_response = message.message_id
        list_of_messages.append(user_response)

        bot_response = bot.send_message(user_id, '🔽 Please use buttons below! 🔽')
        list_of_messages.append(bot_response)
        bot.register_next_step_handler(message, reminder)


def process_reminder_date(message):
    user_id = message.from_user.id
    if message.text == '❌ Cancel':
        cancel_button_task(message, user_id)
    else:
        reminder_date = message.text
        try:
            reminder_date = datetime.strptime(reminder_date, '%Y-%m-%d').date()
            if reminder_date < datetime.now().date():
                user_response = message.message_id
                list_of_messages.append(user_response)
                bot_response = bot.send_message(user_id,
                                                "‼️You cannot set a reminder for the past ‼️\n\n"
                                                " Please enter a valid future date and time 💬")
                list_of_messages.append(bot_response.message_id)
                bot.register_next_step_handler(message, process_reminder_date)
            else:
                delete_error_messages(user_id)  # Deleting unnecessary messages
                user_data['reminder_date'] = reminder_date
                bot.send_message(user_id, f"✅ Date is successfully saved and set\n\n"
                                          f"Now, please enter the time in the format HH:MM 💬",
                                 reply_markup=buttons.cancel())
                bot.register_next_step_handler(message, process_reminder_time)
        except ValueError:
            user_response = message.message_id
            list_of_messages.append(user_response)
            bot_response = bot.send_message(user_id, "❌ Invalid date format  ❌\n\n"
                                                     " Please enter in the format YYYY-MM-DD 💬")
            list_of_messages.append(bot_response.message_id)
            bot.register_next_step_handler(message, process_reminder_date)


def process_reminder_time(message):
    user_id = message.from_user.id
    if message.text == '❌ Cancel':
        cancel_button_task(message, user_id)
    else:
        reminder_time = message.text
        try:
            reminder_time = datetime.strptime(reminder_time, '%H:%M').time()
            if reminder_time < datetime.now().time():
                user_response = message.message_id
                list_of_messages.append(user_response)
                bot_response = bot.send_message(user_id,
                                                "‼️You cannot set a reminder for the past time‼️\n\n"
                                                " Please enter a valid future time 💬")
                list_of_messages.append(bot_response.message_id)
                bot.register_next_step_handler(message, process_reminder_time)
            else:
                delete_error_messages(user_id)  # Deleting unnecessary messages
                user_data['reminder_time'] = reminder_time
                reminder_date_time = datetime.combine(user_data['reminder_date'], user_data['reminder_time'])
                user_data['task_reminder_date'] = reminder_date_time
                bot.send_message(user_id, f"✅ Reminder is successfully set for:\n\n"
                                          f" 📅 Reminder date: {user_data['reminder_date']}\n"
                                          f" ⌚️ Time: {user_data['reminder_time']}\n\n"
                                          f"🔽 Category buttons 🔽",
                                 reply_markup=buttons.category_choose())
                bot.register_next_step_handler(message, category_variants)
        except ValueError:
            user_response = message.message_id
            list_of_messages.append(user_response)
            bot_response = bot.send_message(user_id, "❌Invalid time format ❌\n\n"
                                                     " Please enter in the format HH:MM 💬")
            list_of_messages.append(bot_response.message_id)
            bot.register_next_step_handler(message, process_reminder_time)


# # # # # # # # # # # # # # # # # # # # # # # # # # Task category menu  # # # # # # # # # # # # # # # # # # # # # # # #

def category_variants(message):
    user_id = message.chat.id
    if message.text == '❌ Cancel':
        cancel_button_task(message, user_id)
    elif message.text == '📑 Existing categories':
        delete_error_messages(user_id)  # Deleting unnecessary messages
        bot.send_message(user_id, '🔎 Searching for categories...')
        all_categories = PythonDatabase.check_category(user_id)
        if all_categories is not None:
            category_name_list = []
            response = 'All categories:\n\n'
            for index, category in enumerate(all_categories, start=1):
                category_name = category[2]
                response += f'{index}. {category_name}\n'
                category_name_list.append(category_name)

            bot.send_message(user_id, response + '\nPlease enter the Category NAME 💬', reply_markup=buttons.back())
            bot.register_next_step_handler(message, all_categories_handling, category_name_list)
        else:
            bot.send_message(user_id, '‼️No categories were found. Please create a new category ‼️',
                             reply_markup=buttons.back())
            bot.register_next_step_handler(message, no_category_handling)
    elif message.text == '🆕 Category':
        delete_error_messages(user_id)  # Deleting unnecessary messages
        bot.send_message(user_id, 'Type in the new Category NAME 💬',
                         reply_markup=buttons.back())
        bot.register_next_step_handler(message, create_new_category, user_id)
    elif message.text == '␀ Default ␀':
        delete_error_messages(user_id)  # Deleting unnecessary messages
        category_name = 'Other'
        try:
            PythonDatabase.add_new_category(user_id, category_name)
        except None:
            pass

        category_id = PythonDatabase.getting_category_id(user_id, category_name)
        category_id = category_id[0]
        user_data['category_id'] = category_id
        user_data['category_name'] = category_name
        print(f'Other: {user_data}')
        task_details_show(message, user_id, category_name)
    else:
        user_response = message.message_id
        list_of_messages.append(user_response)

        bot_response = bot.send_message(user_id, '🔽 Please use buttons below! 🔽')
        list_of_messages.append(bot_response.message_id)
        bot.register_next_step_handler(message, category_variants)


def all_categories_handling(message, category_name_list):
    user_id = message.chat.id
    if message.text == '⬅️ Back':
        delete_error_messages(user_id)  # Deleting unnecessary messages
        bot.send_message(user_id, '✨Category menu', reply_markup=buttons.category_choose())
        bot.register_next_step_handler(message, category_variants)
    elif message.text.isalpha():
        category_name = str(message.text)
        if category_name in category_name_list:
            delete_error_messages(user_id)  # Deleting unnecessary messages
            category_id = PythonDatabase.getting_category_id(user_id, category_name)
            category_id = category_id[0]
            user_data['category_id'] = category_id
            user_data['category_name'] = category_name
            print(f'All categories handling: {user_data}')
            task_details_show(message, user_id, category_name)
        else:
            user_response = message.message_id
            list_of_messages.append(user_response)
            bot_response = bot.send_message(user_id, '❗️Please enter a valid Category NAME ❗️️\n\n'
                                                     '🔽 Or press button below! 🔽')
            list_of_messages.append(bot_response.message_id)
            bot.register_next_step_handler(message, all_categories_handling, category_name_list)
    else:
        user_response = message.message_id
        list_of_messages.append(user_response)
        bot_response = bot.send_message(user_id, '❗️Please enter Category NAME ❗️\n\n'
                                                 '🔽 Or press button below! 🔽')
        list_of_messages.append(bot_response.message_id)
        bot.register_next_step_handler(message, all_categories_handling, category_name_list)


def no_category_handling(message):
    user_id = message.chat.id
    if message.text == '⬅️ Back':
        delete_error_messages(user_id)  # Deleting unnecessary messages
        bot.send_message(user_id, '✨Category menu', reply_markup=buttons.category_choose())
        bot.register_next_step_handler(message, category_variants)
    else:
        user_response = message.message_id
        list_of_messages.append(user_response)

        bot_response = bot.send_message(user_id, '🔽 Please use button below! 🔽')
        list_of_messages.append(bot_response.message_id)
        bot.register_next_step_handler(message, no_category_handling)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # Adding new category  # # # # # # # # # # # # # # # # # # # # # #

def create_new_category(message, user_id):
    if message.text == '⬅️ Back':
        delete_error_messages(user_id)  # Deleting unnecessary messages
        bot.send_message(user_id, '✨Category menu', reply_markup=buttons.category_choose())
        bot.register_next_step_handler(message, category_variants)
    else:
        category_name = message.text
        new_category = PythonDatabase.add_new_category(user_id, category_name)
        if new_category is not None:
            category_id = PythonDatabase.getting_category_id(user_id, category_name)
            category_id = category_id[0]
            user_data['category_id'] = category_id
            user_data['category_name'] = category_name
            print(f'New category {user_data}')
            task_details_show(message, user_id, category_name)
        else:
            bot.send_message(user_id, f'‼️Category "{category_name}" already exists ‼️\n\n'
                                      f'🔽 Category buttons 🔽',
                             reply_markup=buttons.category_choose())
            bot.register_next_step_handler(message, category_variants)


def delete_error_messages(user_id):
    if len(list_of_messages) > 0:
        for msg_id in list_of_messages:
            bot.delete_message(user_id, msg_id)
        list_of_messages.clear()
    return list_of_messages


def cancel_button_registration(message, user_id):
    bot.send_message(user_id, '‼️Registration is canceled ‼️\n\n'
                              '🔽 Click button below if want to sign up 🔽', reply_markup=buttons.sign_up())
    bot.register_next_step_handler(message, user_registration)
    user_data.clear()
    list_of_messages.clear()


def cancel_button_task(message, user_id):
    delete_error_messages(user_id)  # Deleting unnecessary messages
    bot.send_message(user_id, '⚖️ Main Menu:', reply_markup=buttons.main_menu_buttons())
    bot.register_next_step_handler(message, main_menu)
    user_data.clear()


def datetime_now_show():
    current_date_time = datetime.now()
    current_date = current_date_time.strftime('%Y-%m-%d')
    current_time = current_date_time.strftime('%I:%M %p')
    show_user_today_date_time = f'📅 Creation date: {current_date}; ⌚️Time: {current_time}'
    return show_user_today_date_time


def datetime_reminder_show():
    reminder_date_time = user_data['task_reminder_date']
    reminder_date = reminder_date_time.strftime('%Y-%m-%d')
    reminder_time = reminder_date_time.strftime('%I:%M %p')
    show_user_reminder_date_time = f'⏰ Reminder date: {reminder_date}; ⌚️Time: {reminder_time}'
    return show_user_reminder_date_time


def task_details_show(message, user_id, category_name):
    if 'task_reminder_date' in user_data:
        bot.send_message(user_id, f'✅ Category "{category_name}" is successfully saved and set\n\n\n'
                                  f'📜 Task details:\n\n'
                                  f"✏️ Title: {user_data['task_name']}\n"
                                  f"📃 Description: {user_data['task_description']}\n"
                                  f"{datetime_reminder_show()}\n"
                                  f"✨ Category: {user_data['category_name']}\n"
                                  f"{datetime_now_show()}\n\n"
                                  f"✅ Task is successfully saved and set ✅",
                         reply_markup=buttons.main_menu_buttons())
        PythonDatabase.add_new_task(user_data)
        bot.register_next_step_handler(message, main_menu)
        full_name = PythonDatabase.check_if_user_registered(user_id)
        send_reminder_message(message, text= f'\n\n\n{full_name[0]} {full_name[1]}, this is a reminder 💬\n\n'
                                            f'⏰ You have a scheduled task  "{user_data['task_name']}"\n\n\n',
                              reminder_date=user_data['task_reminder_date'])
    else:
        bot.send_message(user_id, f'✅ Category "{category_name}" is successfully saved and set\n\n\n'
                                  f'📜 Task details:\n\n'
                                  f"✏️ Title: {user_data['task_name']}\n"
                                  f"📃 Description: {user_data['task_description']}\n"
                                  f"⏰ Reminder date: NULL\n"
                                  f"✨ Category: {user_data['category_name']}\n"
                                  f"{datetime_now_show()}\n\n"
                                  f"✅ Task is successfully saved and set ✅",
                         reply_markup=buttons.main_menu_buttons())
        PythonDatabase.add_new_task_without_reminder_date(user_data)
        bot.register_next_step_handler(message, main_menu)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # View all tasks  # # # # # # # # # # # # # # # # # # # # # # # #

def truncate_text(text, max_length):
    return text if len(text) <= max_length else text[:max_length - 6] + '...'


def no_tasks_found(message, user_id):
    bot.send_message(user_id, f'‼️No tasks were found ‼️', reply_markup=buttons.view_tasks_menu())
    bot.register_next_step_handler(message, view_tasks_menu)


def view_tasks_menu(message):
    user_id = message.chat.id
    if message.text == '⬅️ Back':
        delete_error_messages(user_id)  # Deleting unnecessary messages
        bot.send_message(user_id, '⚖️ Main Menu', reply_markup=buttons.main_menu_buttons())
        bot.register_next_step_handler(message, main_menu)
    elif message.text == '📅 Sort by Created Date':
        delete_error_messages(user_id)  # Deleting unnecessary messages
        all_tasks = PythonDatabase.order_by_creation_date(user_id)
        if all_tasks:
            header = f"{'#️⃣ID':<10}  {'✏️Task Title':<45}  {'📅Creation Date':<35}  {'⌚️Time':<25}\n"
            header += '-' * 100 + '\n\n'
            text_str = ''
            for index, task in enumerate(all_tasks, start=1):
                created_date_str = datetime.strptime(task[4], '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d')
                created_time_str = datetime.strptime(task[4], '%Y-%m-%d %H:%M:%S.%f').strftime('%H:%M %p')
                task_title_name = truncate_text(task[2], 15)

                text_str += (f'{f'{index}.':<15}  {task_title_name:<50}  {created_date_str:<35}'
                             f'  {created_time_str:<25}\n')
            bot.send_message(user_id, f'\n\n{header}{text_str}\n\n', reply_markup=buttons.view_tasks_menu())
            bot.register_next_step_handler(message, view_tasks_menu)
        else:
            no_tasks_found(message, user_id)
    elif message.text == '✨ Sort by Category':
        delete_error_messages(user_id)  # Deleting unnecessary messages
        get_all_tasks = PythonDatabase.order_by_category(user_id)
        if get_all_tasks:
            header = f"{'#️⃣ID':<10}  {'✏️Task Title':<30} {'✨Category':<30} {'📅Reminder Date':<25} {'⌚️Time':<10}\n"
            header += '-' * 100 + '\n\n'
            text_str = ''
            for index, task in enumerate(get_all_tasks, start=1):
                category_name = PythonDatabase.getting_category_name_by_id(user_id, task[6])
                category_name = category_name[0]
                task_title_name = truncate_text(task[2], 15)
                category_name = truncate_text(category_name, 14)
                if task[5] is not None:
                    reminder_date_str = datetime.strptime(task[5], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                    reminder_time_str = datetime.strptime(task[5], '%Y-%m-%d %H:%M:%S').strftime('%H:%M %p')
                else:
                    reminder_date_str = '      NULL     '
                    reminder_time_str = '          NULL'

                text_str += (f'{f'{index}.':<15}  {task_title_name:<32}  {category_name:<35} {reminder_date_str:<30}'
                             f' {reminder_time_str:<10} \n')

            bot.send_message(user_id, f'\n\n{header}{text_str}\n\n', reply_markup=buttons.view_tasks_menu())
            bot.register_next_step_handler(message, view_tasks_menu)
        else:
            no_tasks_found(message, user_id)
    elif message.text == '✏️ Sort by Title':
        delete_error_messages(user_id)  # Deleting unnecessary messages
        get_all_tasks = PythonDatabase.order_by_title(user_id)
        if get_all_tasks:
            header = f"{'#️⃣ID':<10}  {'✏️Task Title':<25} {'📑Task Description':<10}\n"
            header += '-' * 100 + '\n\n'
            text_str = ''
            for index, task in enumerate(get_all_tasks, start=1):
                task_title_name = truncate_text(task[2], 15)
                task_description_column = truncate_text(task[3], 70)

                text_str += f'{f'{index}.':<15}  {task_title_name:<25} {task_description_column:<10}\n'

            bot.send_message(user_id, f'\n\n{header}{text_str}\n\n', reply_markup=buttons.view_tasks_menu())
            bot.register_next_step_handler(message, view_tasks_menu)
        else:
            no_tasks_found(message, user_id)
    else:
        user_response = message.message_id
        list_of_messages.append(user_response)

        bot_response = bot.send_message(user_id, '🔽 Please use buttons below! 🔽')
        list_of_messages.append(bot_response.message_id)
        bot.register_next_step_handler(message, view_tasks_menu)


def edit_profile_menu(message):
    user_id = message.chat.id
    if message.text == '⬅️ Back':
        delete_error_messages(user_id)  # Deleting unnecessary messages
        bot.send_message(user_id, '⚖️ Main Menu', reply_markup=buttons.main_menu_buttons())
        bot.register_next_step_handler(message, main_menu)
    elif message.text == '📝 First Name':
        delete_error_messages(user_id)  # Deleting unnecessary messages
        bot.send_message(user_id, 'Please type in new First Name 💬', reply_markup=buttons.back())
        bot.register_next_step_handler(message, edit_first_name)
    elif message.text == '📝 Last Name':
        delete_error_messages(user_id)  # Deleting unnecessary messages
        bot.send_message(user_id, 'Please type in new Last Name 💬', reply_markup=buttons.back())
        bot.register_next_step_handler(message, edit_last_name)
    elif message.text == '📩 Email Address':
        delete_error_messages(user_id)  # Deleting unnecessary messages
        bot.send_message(user_id, 'Please type in new Email Address 💬', reply_markup=buttons.back())
        bot.register_next_step_handler(message, edit_email_address)
    elif message.text == '📲 Phone Number':
        delete_error_messages(user_id)  # Deleting unnecessary messages
        bot.send_message(user_id, 'Please type in new Phone Number(+998) 💬', reply_markup=buttons.back())
        bot.register_next_step_handler(message, edit_phone_number)
    else:
        user_response = message.message_id
        list_of_messages.append(user_response)

        bot_response = bot.send_message(user_id, '🔽 Please use buttons below! 🔽', reply_markup=buttons.back())
        list_of_messages.append(bot_response.message_id)
        bot.register_next_step_handler(message, edit_email_address)


def edit_first_name(message):
    user_id = message.chat.id
    if message.text == '⬅️ Back':
        delete_error_messages(user_id)  # Deleting unnecessary messages
        bot.send_message(user_id, '🛠️ Edit Profile Menu', reply_markup=buttons.edit_profile())
        bot.register_next_step_handler(message, edit_profile_menu)
    else:
        if message.text.isalpha():
            first_name = message.text.capitalize()
            new_first_name = PythonDatabase.change_first_name(first_name, user_id)
            if new_first_name:
                delete_error_messages(user_id)  # Deleting unnecessary messages
                bot.send_message(user_id, f'✅ Changes are successfully saved ✅',
                                 reply_markup=buttons.edit_profile())
                bot.register_next_step_handler(message, edit_profile_menu)
            else:
                bot.send_message(user_id, '‼️ Error in changing First name ‼️'
                                          'Please try again later 💬', reply_markup=buttons.back())
                bot.register_next_step_handler(message, edit_email_address)
        else:
            user_response = message.message_id
            list_of_messages.append(user_response)

            bot_response = bot.send_message(user_id, '❌ Error invalid First Name ❌'
                                                     '🔄 Please try again to type in your New First Name 🔄',
                                            reply_markup=buttons.back())
            list_of_messages.append(bot_response.message_id)
            bot.register_next_step_handler(message, edit_first_name)


def edit_last_name(message):
    user_id = message.chat.id
    if message.text == '⬅️ Back':
        delete_error_messages(user_id)  # Deleting unnecessary messages
        bot.send_message(user_id, '🛠️ Edit Profile Menu', reply_markup=buttons.edit_profile())
        bot.register_next_step_handler(message, edit_profile_menu)
    else:
        if message.text.isalpha():
            last_name = message.text.capitalize()
            new_last_name = PythonDatabase.change_last_name(last_name, user_id)
            if new_last_name:
                delete_error_messages(user_id)  # Deleting unnecessary messages
                bot.send_message(user_id, f'✅ Changes are successfully saved ✅',
                                 reply_markup=buttons.edit_profile())
                bot.register_next_step_handler(message, edit_profile_menu)
            else:
                bot.send_message(user_id, '‼️ Error in changing Last name ‼️'
                                          'Please try again later 💬', reply_markup=buttons.back())
                bot.register_next_step_handler(message, edit_last_name)
        else:
            user_response = message.message_id
            list_of_messages.append(user_response)

            bot_response = bot.send_message(user_id, '❌ Error invalid Last Name ❌\n\n'
                                                     '🔄 Please try again to type in your New Last Name 🔄',
                                            reply_markup=buttons.back())
            list_of_messages.append(bot_response.message_id)
            bot.register_next_step_handler(message, edit_last_name)


def edit_email_address(message):
    user_id = message.chat.id
    if message.text == '⬅️ Back':
        delete_error_messages(user_id)  # Deleting unnecessary messages
        bot.send_message(user_id, '🛠️ Edit Profile Menu', reply_markup=buttons.edit_profile())
        bot.register_next_step_handler(message, edit_profile_menu)
    else:
        email_address = message.text.strip()
        parts = email_address.split('.')
        if '@' in email_address and not email_address.startswith('@') and not email_address.endswith('@') \
                and email_address.count('@') == 1 and ".." not in email_address and not email_address.startswith('.') \
                and not email_address.endswith('.') and '.' in email_address.split('@')[-1] and parts[-1].isalpha() \
                and len(parts[-1]) >= 2:
            new_email_address = PythonDatabase.change_email_address(email_address, user_id)
            if new_email_address:
                delete_error_messages(user_id)  # Deleting unnecessary messages
                bot.send_message(user_id, f'✅ Changes are successfully saved ✅',
                                 reply_markup=buttons.edit_profile())
                bot.register_next_step_handler(message, edit_profile_menu)
            else:
                bot.send_message(user_id, '‼️ Error in changing Email Address ‼️'
                                          'Please try again later 💬', reply_markup=buttons.back())
                bot.register_next_step_handler(message, edit_email_address)
        else:
            user_response = message.message_id
            list_of_messages.append(user_response)

            bot_response = bot.send_message(user_id, '❌ Error invalid email address! ❌\n\n'
                                                     '🔄 Please try again to type in your New Email Address 🔄',
                                            reply_markup=buttons.back())
            list_of_messages.append(bot_response.message_id)
            bot.register_next_step_handler(message, edit_email_address)


def edit_phone_number(message):
    user_id = message.chat.id
    if message.text == '⬅️ Back':
        delete_error_messages(user_id)  # Deleting unnecessary messages
        bot.send_message(user_id, '🛠️ Edit Profile Menu', reply_markup=buttons.edit_profile())
        bot.register_next_step_handler(message, edit_profile_menu)
    else:
        phone_number = message.text.strip()
        if phone_number.startswith('+998'):
            phone_number_second_part = phone_number[4:]
            if phone_number_second_part.isdigit() and len(phone_number_second_part) == 9:
                new_phone_number = PythonDatabase.change_phone_number(phone_number, user_id)
                if new_phone_number:
                    delete_error_messages(user_id)  # Deleting unnecessary messages
                    bot.send_message(user_id, f'✅ Changes are successfully saved ✅',
                                     reply_markup=buttons.edit_profile())
                    bot.register_next_step_handler(message, edit_profile_menu)
                else:
                    bot.send_message(user_id, '‼️ Error in changing Phone Number ‼️'
                                              'Please try again later 💬', reply_markup=buttons.back())
                    bot.register_next_step_handler(message, edit_phone_number)
            else:
                user_response = message.message_id
                list_of_messages.append(user_response)
                bot_response = bot.send_message(user_id,
                                                '‼️ Error: Invalid format. Ensure the number after +998'
                                                ' is 9 digits long and contains only numbers ‼️',
                                                reply_markup=buttons.back())
                list_of_messages.append(bot_response.message_id)
                bot.register_next_step_handler(message, edit_phone_number)
        else:
            user_response = message.message_id
            list_of_messages.append(user_response)

            bot_response = bot.send_message(user_id, '‼️ Error: Ensure your new phone number starts with "+998". ‼️',
                                            reply_markup=buttons.back())
            list_of_messages.append(bot_response.message_id)
            bot.register_next_step_handler(message, edit_phone_number)


def utilities_menu(message):
    user_id = message.chat.id
    if message.text == '⬅️ Back':
        cancel_button_task(message, user_id)
    elif message.text == '📝 Complete Task ✅':
        delete_error_messages(user_id)  # Deleting unnecessary messages
        view_only_tasks = PythonDatabase.view_only_tasks(user_id)
        tasks_list = []
        if view_only_tasks:
            header = f"{'#️⃣ID':<25}  {'✏️Task Title'}\n"
            header += '-' * 80 + '\n\n'
            line = '-' * 80 + '\n\n'
            text_str = ''
            for index, task in enumerate(view_only_tasks, start=1):
                task_name = task[0]
                tasks_list.append(task_name)
                text_str += f'{f'{index}.':<30}   {task_name}\n'

            bot.send_message(user_id, f'\n\n{header}{text_str}\n{line}'
                                      f'Please enter Task Title to delete it 💬', reply_markup=buttons.back())
            bot.register_next_step_handler(message, complete_task, tasks_list)
        else:
            bot.send_message(user_id, f'‼️ No tasks found ‼️\n\n'
                                      f'Please first create tasks 💬', reply_markup=buttons.back())
            bot.register_next_step_handler(message, utilities_menu)
    elif message.text == '🗑️ Delete Category':
        delete_error_messages(user_id)  # Deleting unnecessary messages
        view_all_categories = PythonDatabase.view_only_categories(user_id)
        category_list = []
        if view_all_categories:
            header = f"{'#️⃣ID':<25}  {'✨Category'}\n"
            header += '-' * 80 + '\n\n'
            line = '-' * 80 + '\n\n'
            text_str = ''
            for index, category in enumerate(view_all_categories, start=1):
                category_name = category[0]
                category_list.append(category_name)
                text_str += f'{f'{index}.':<30}  {category_name}\n'

            bot.send_message(user_id, f'\n\n\n{header}{text_str}\n{line}'
                                      f'Please enter Category Name to delete it 💬',
                             reply_markup=buttons.back())
            bot.register_next_step_handler(message, complete_category, category_list)
    else:
        user_response = message.message_id
        list_of_messages.append(user_response)

        bot_response = bot.send_message(user_id, '️ ❌ Error: Invalid symbols❌\n\n'
                                                 '🔽 Please use buttons below 🔽',
                                        reply_markup=buttons.utilities())
        list_of_messages.append(bot_response.message_id)
        bot.register_next_step_handler(message, utilities_menu)


def complete_task(message, task_list):
    user_id = message.chat.id
    if message.text == '⬅️ Back':
        delete_error_messages(user_id)  # Deleting unnecessary messages
        bot.send_message(user_id, '🗂️ Utilities Menu:', reply_markup=buttons.utilities())
        bot.register_next_step_handler(message, utilities_menu)
    else:
        task_name = message.text
        if task_name in task_list:
            delete_error_messages(user_id)  # Deleting unnecessary messages
            delete_task = PythonDatabase.delete_task(user_id, task_name)
            task_list.remove(task_name)
            if delete_task:
                bot.send_message(user_id, f'✅ "{task_name}" is completed ✅', reply_markup=buttons.utilities())
                bot.register_next_step_handler(message, utilities_menu)
            else:
                bot.send_message(user_id, '‼️ Error in completing task ‼️'
                                          'Please try again later 💬', reply_markup=buttons.back())
                bot.register_next_step_handler(message, utilities_menu)
        else:
            user_response = message.message_id
            list_of_messages.append(user_response)

            bot_response = bot.send_message(user_id, '‼️ Error: Invalid Task Title ‼️',
                                            reply_markup=buttons.back())
            list_of_messages.append(bot_response.message_id)
            bot.register_next_step_handler(message, complete_task, task_list)


def complete_category(message, category_list):
    user_id = message.chat.id
    if message.text == '⬅️ Back':
        delete_error_messages(user_id)  # Deleting unnecessary messages
        bot.send_message(user_id, '🗂️ Utilities Menu:', reply_markup=buttons.utilities())
        bot.register_next_step_handler(message, utilities_menu)
    else:
        category_name = message.text
        category_id = PythonDatabase.getting_category_id(user_id, category_name)
        if category_id:
            delete_error_messages(user_id)
            category_id = category_id[0]
            check_if_category_id_in_task_details_database = \
                PythonDatabase.check_if_category_id_in_database(user_id, category_id)
            if check_if_category_id_in_task_details_database:
                bot.send_message(user_id, f'‼️ ERROR: This Category is assigned to the task(s) ‼️\n\n'
                                          f'❌ Deletion is restricted ❌', reply_markup=buttons.utilities())
                bot.register_next_step_handler(message, utilities_menu)
            else:
                delete_category = PythonDatabase.delete_category(user_id, category_name)
                if delete_category:
                    bot.send_message(user_id, f'✅ Category is successfully deleted\n\n', reply_markup=buttons.back())
                    category_list.remove(category_name)
                    bot.register_next_step_handler(message, complete_category, category_list)
                else:
                    bot.send_message(user_id, f'‼️ ERROR: Deletion is failed‼️\n\n'
                                              f'Please try again later 💬', reply_markup=buttons.utilities())
                    bot.register_next_step_handler(message, utilities_menu)
        else:
            user_response = message.message_id
            list_of_messages.append(user_response)

            bot_response = bot.send_message(user_id, f'❌ ERROR: Invalid Category NAME ❌️\n\n',
                                            reply_markup=buttons.back())
            list_of_messages.append(bot_response.message_id)
            bot.register_next_step_handler(message, complete_category, category_list)


def send_reminder_message(message, text, reminder_date):
    user_id = message.chat.id
    current_datetime = datetime.now()
    delay_seconds = (reminder_date - current_datetime).total_seconds()

    check_remidner_date = sql.execute('''SELECT user_id, task_name, task_reminder_date 
                       FROM to_do_tasks 
                       WHERE task_reminder_date <= ?''', (current_datetime,)).fetchall()
    if check_remidner_date:
        # Wait until it's time to send the message
        if delay_seconds > 0:
            time.sleep(delay_seconds)

        # Send the message
        try:
            bot.send_message(user_id, text)
        except Exception as e:
            print(f"Error sending reminder message: {e}")
    else:
        pass


bot.infinity_polling()
