from telebot import types


def sign_up(remove_button=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    sign_up_button = types.KeyboardButton('✅ Sign up')
    if remove_button:
        markup.row()
    markup.add(sign_up_button)
    return markup


def cancel():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cancel_button = types.KeyboardButton('❌ Cancel')

    markup.row(cancel_button)
    return markup


def share_my_phone_number():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    share_phone_number_button = types.KeyboardButton('📲Share Contact', request_contact=True)
    cancel_button = types.KeyboardButton('❌ Cancel')

    markup.row(share_phone_number_button, cancel_button)
    return markup


def main_menu_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    create_task_button = types.KeyboardButton('🆕 Create Task')
    view_tasks_button = types.KeyboardButton('📋 View Tasks')
    edit_task_category_button = types.KeyboardButton('🗂️ Task Utilities')

    edit_profile_button = types.KeyboardButton('👤️ Edit Profile')

    markup.row(create_task_button, view_tasks_button, edit_task_category_button)
    markup.add(edit_profile_button)

    return markup


def reminder():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    set_reminder_button = types.KeyboardButton('✅ YES')
    reminder_null_button = types.KeyboardButton('❌ NO')

    markup.row(set_reminder_button, reminder_null_button)
    return markup


def category_choose():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    existing_category_button = types.KeyboardButton('📑 Existing categories')
    new_category_button = types.KeyboardButton('🆕 Category')
    default_category_button = types.KeyboardButton('␀ Default ␀')
    cancel_button = types.KeyboardButton('❌ Cancel')

    markup.row(existing_category_button, new_category_button, default_category_button)
    markup.add(cancel_button)
    return markup


def back():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back_button = types.KeyboardButton('⬅️ Back')

    markup.add(back_button)
    return markup


def view_tasks_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    order_by_created_date_button = types.KeyboardButton('📅 Sort by Created Date')
    order_by_category_button = types.KeyboardButton('✨ Sort by Category')
    order_by_title = types.KeyboardButton('✏️ Sort by Title')
    back_button = types.KeyboardButton('⬅️ Back')

    markup.row(order_by_created_date_button, order_by_category_button, order_by_title)
    markup.add(back_button)
    return markup


def edit_profile():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    edit_first_name_button = types.KeyboardButton('📝 First Name')
    edit_last_name_button = types.KeyboardButton('📝 Last Name')
    edit_email_address_button = types.KeyboardButton('📩 Email Address')
    edit_phone_number_button = types.KeyboardButton('📲 Phone Number')
    back_button = types.KeyboardButton('⬅️ Back')

    markup.row(edit_first_name_button, edit_last_name_button, edit_email_address_button, edit_phone_number_button)
    markup.add(back_button)
    return markup


def utilities():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mark_task_done_button = types.KeyboardButton('📝 Complete Task ✅')
    mark_category_done_button = types.KeyboardButton('🗑️ Delete Category')
    back_button = types.KeyboardButton('⬅️ Back')

    markup.row(mark_task_done_button, mark_category_done_button)
    markup.add(back_button)
    return markup
