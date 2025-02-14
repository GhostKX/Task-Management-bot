import sqlite3

connection = sqlite3.connect('task_manager.db')

sql = connection.cursor()

sql.execute('''CREATE TABLE IF NOT EXISTS user_details(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email_address TEXT NOT NULL,
            phone_number TEXT NOT NULL);''')

sql.execute('''CREATE TABLE IF NOT EXISTS category_details(
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            category_name TEXT NOT NULL,
            UNIQUE (user_id, category_name),
            FOREIGN KEY (user_id) REFERENCES user_details (user_id));''')

sql.execute('''CREATE TABLE IF NOT EXISTS task_details(
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            task_name TEXT NOT NULL,
            task_description TEXT NOT NULL,
            task_creation_date DATETIME NOT NULL,
            task_reminder_date DATETIME DEFAULT NULL,
            category_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user_details (user_id),
            FOREIGN KEY (category_id) REFERENCES category_details (category_id) ON DELETE RESTRICT);''')

connection.commit()
connection.close()


def check_if_user_registered(user_id):
    connection = sqlite3.connect('task_manager.db')
    sql = connection.cursor()
    check_user = sql.execute('SELECT last_name, first_name FROM user_details '
                             'WHERE user_id = ?', (user_id,)).fetchone()
    connection.close()
    print(check_user)
    return check_user


def add_user(user_data):
    connection = sqlite3.connect('task_manager.db')
    sql = connection.cursor()
    add_user_to_database = sql.execute('INSERT INTO user_details'
                                       '(user_id, first_name, last_name, email_address, phone_number)'
                                       'VALUES (?, ?, ?, ?, ?)',
                                       (user_data['user_id'], user_data['first_name'],
                                        user_data['last_name'], user_data['email_address'], user_data['phone_number']))
    connection.commit()
    connection.close()
    return add_user_to_database


def check_category(user_id):
    connection = sqlite3.connect('task_manager.db')
    sql = connection.cursor()
    all_categories = sql.execute('SELECT * FROM category_details WHERE user_id = ? ORDER BY category_id',
                                 (user_id,)).fetchall()
    connection.close()
    if all_categories:
        return all_categories
    else:
        return None


def check_one_category_name(user_id, category_name):
    connection = sqlite3.connect('task_manager.db')
    sql = connection.cursor()
    check_category_name = sql.execute('SELECT * FROM category_details WHERE user_id = ? and category_name = ?',
                                      (user_id, category_name)).fetchall()
    connection.close()
    return check_category_name


def add_new_category(user_id, category_name):
    connection = sqlite3.connect('task_manager.db')
    sql = connection.cursor()
    if check_one_category_name(user_id, category_name):
        return None
    else:
        add_category = sql.execute('INSERT INTO category_details(user_id, category_name) VALUES(?, ?)',
                                   (user_id, category_name))
        connection.commit()
        connection.close()
        return add_category


def getting_category_id(user_id, category_name):
    connection = sqlite3.connect('task_manager.db')
    sql = connection.cursor()
    category_id = sql.execute('SELECT category_id FROM category_details WHERE user_id = ? and category_name = ?',
                              (user_id, category_name)).fetchone()
    connection.close()
    return category_id


def add_new_task(user_data):
    connection = sqlite3.connect('task_manager.db')
    sql = connection.cursor()
    add_task = sql.execute('INSERT INTO task_details(user_id, task_name, task_description, task_creation_date,'
                           'task_reminder_date, category_id) VALUES (?, ?, ?, ?, ?, ?)',
                           (user_data['user_id'], user_data['task_name'], user_data['task_description'],
                            user_data['task_creation_date'], user_data['task_reminder_date'], user_data['category_id']))
    connection.commit()
    connection.close()
    return add_task


def add_new_task_without_reminder_date(user_data):
    connection = sqlite3.connect('task_manager.db')
    sql = connection.cursor()
    add_task = sql.execute('INSERT INTO task_details(user_id, task_name, task_description, task_creation_date,'
                           'category_id) VALUES (?, ?, ?, ?, ?)',
                           (user_data['user_id'], user_data['task_name'], user_data['task_description'],
                            user_data['task_creation_date'], user_data['category_id']))
    connection.commit()
    connection.close()
    return add_task


def getting_category_name_by_id(user_id, category_id):
    connection = sqlite3.connect('task_manager.db')
    sql = connection.cursor()
    get_category_name = sql.execute('SELECT category_name FROM category_details WHERE user_id = ? AND category_id = ?',
                                    (user_id, category_id)).fetchone()
    connection.close()
    return get_category_name


def view_all_tasks(user_id):
    connection = sqlite3.connect('task_manager.db')
    sql = connection.cursor()
    get_all_tasks = sql.execute('SELECT * FROM task_details WHERE user_id = ? ORDER BY task_id',
                                (user_id,)).fetchall()

    connection.close()
    return get_all_tasks


def order_by_creation_date(user_id):
    connection = sqlite3.connect('task_manager.db')
    sql = connection.cursor()
    get_all_tasks = sql.execute('SELECT * FROM task_details WHERE user_id = ? ORDER BY task_creation_date',
                                (user_id,)).fetchall()
    connection.close()
    return get_all_tasks


def order_by_category(user_id):
    connection = sqlite3.connect('task_manager.db')
    sql = connection.cursor()
    get_all_tasks = sql.execute('SELECT * FROM task_details WHERE user_id = ? ORDER BY category_id',
                                (user_id,)).fetchall()
    connection.close()
    return get_all_tasks


def order_by_title(user_id):
    connection = sqlite3.connect('task_manager.db')
    sql = connection.cursor()
    get_all_tasks = sql.execute('SELECT * FROM task_details WHERE user_id = ? ORDER BY task_name',
                                (user_id,)).fetchall()
    connection.close()
    return get_all_tasks


def change_first_name(first_name, user_id):
    connection = sqlite3.connect('task_manager.db')
    sql = connection.cursor()
    edit_first_name = sql.execute('UPDATE user_details SET first_name = ? WHERE user_id = ?',
                                  (first_name, user_id))
    connection.commit()
    connection.close()
    return edit_first_name


def change_last_name(last_name, user_id):
    connection = sqlite3.connect('task_manager.db')
    sql = connection.cursor()
    edit_last_name = sql.execute('UPDATE user_details SET last_name = ? WHERE user_id = ?',
                                 (last_name, user_id))
    connection.commit()
    connection.close()
    return edit_last_name


def change_email_address(email_address, user_id):
    connection = sqlite3.connect('task_manager.db')
    sql = connection.cursor()
    edit_email_address = sql.execute('UPDATE user_details SET email_address = ? WHERE user_id = ?',
                                     (email_address, user_id))
    connection.commit()
    connection.close()
    return edit_email_address


def change_phone_number(phone_number, user_id):
    connection = sqlite3.connect('task_manager.db')
    sql = connection.cursor()
    edit_phone_number = sql.execute('UPDATE user_details SET phone_number = ? WHERE user_id = ?',
                                    (phone_number, user_id))
    connection.commit()
    connection.close()
    return edit_phone_number


def view_only_tasks(user_id):
    connection = sqlite3.connect('task_manager.db')
    sql = connection.cursor()
    view_tasks_button = sql.execute('SELECT task_name FROM task_details WHERE user_id = ? ORDER BY task_id',
                                    (user_id,)).fetchall()
    connection.close()
    return view_tasks_button


def delete_task(user_id, task_name):
    connection = sqlite3.connect('task_manager.db')
    sql = connection.cursor()
    finish_task = sql.execute('DELETE FROM task_details WHERE user_id = ? AND task_name = ?',
                              (user_id, task_name))
    connection.commit()
    connection.close()
    return finish_task


def view_only_categories(user_id):
    connection = sqlite3.connect('task_manager.db')
    sql = connection.cursor()
    delete_category = (sql.execute('SELECT category_name FROM category_details WHERE user_id = ? ORDER BY category_id',
                                   (user_id,)).fetchall())

    connection.close()
    return delete_category


def check_if_category_id_in_database(user_id, category_id):
    connection = sqlite3.connect('task_manager.db')
    sql = connection.cursor()
    check_if_exist = sql.execute('SELECT * FROM task_details WHERE user_id = ? AND category_id = ?',
                                 (user_id, category_id)).fetchall()
    connection.close()
    return check_if_exist


def delete_category(user_id, category_name):
    connection = sqlite3.connect('task_manager.db')
    sql = connection.cursor()
    delete_category_name = sql.execute('DELETE FROM category_details WHERE user_id = ? AND category_name = ?',
                                       (user_id, category_name))
    connection.commit()
    connection.close()
    return delete_category_name
