# Telegram Task Manager Bot

A **Python-based Telegram bot** that helps users manage their tasks and schedules. The bot allows users to create, view, and manage tasks with features like reminders, categories, and profile management. Built using the **PyTelegramBotAPI** library, this bot provides a comprehensive task management solution.

## Features

### User Management
- **User Registration**: New users can sign up with their personal details
- **Profile Management**: Users can edit their profile information
- **Secure Data Storage**: User information is stored safely in a database

### Task Management
- **Create Tasks**: Add new tasks with titles, descriptions, and optional reminders
- **View Tasks**: Multiple ways to view and sort tasks
- **Categories**: Organize tasks by custom categories
- **Task Completion**: Mark tasks as complete when finished
- **Reminders**: Set optional reminders for tasks

### Task Organization
- **Custom Categories**: Create and manage task categories
- **Sorting Options**: Sort tasks by:
  - Creation date
  - Category
  - Title
- **Task Details**: View comprehensive task information including:
  - Title
  - Description
  - Category
  - Creation date/time
  - Reminder date/time (if set)

### User Interface
- **Interactive Buttons**: Easy navigation through button menus
- **Step-by-step Process**: Guided task creation and management
- **Error Handling**: Clear error messages and input validation
- **Back Navigation**: Easy return to previous menus

## Requirements

- Python 3.x
- PyTelegramBotAPI
- SQLite (for database management)

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/Task-Management-bot.git
```

2. Install required dependencies
```bash
pip install -r requirements.txt
```

3. Configure the bot

- Create `.env` file to store the Telegram API_KEY
```python
bot = telebot.TeleBot(API_KEY)
```

4. Run the bot
```bash
python task_manager_bot.py
```

## Usage

### Initial Setup
1. Start the bot with `/start`
2. Register by providing:
   - First Name
   - Last Name
   - Email Address
   - Phone Number

### Creating Tasks
1. Select "🆕 Create Task"
2. Enter task title
3. Provide task description
4. Choose whether to set a reminder
5. Select or create a category
6. Confirm task creation

### Viewing Tasks
1. Select "📋 View Tasks"
2. Choose sorting method:
   - 📅 Sort by Created Date
   - ✨ Sort by Category
   - ✏️ Sort by Title

### Managing Tasks
1. Select "🗂️ Task Utilities"
2. Choose action:
   - 📝 Complete Task ✅
   - 🗑️ Delete Category

### Profile Management
1. Select "👤️ Edit Profile"
2. Choose what to edit:
   - First Name
   - Last Name
   - Email Address
   - Phone Number

## Features in Details

### Task Creation
- **Title & Description**: Add detailed task information
- **Reminders**: Optional date and time reminders
- **Categories**: Organize tasks by custom categories
- **Creation Timestamp**: Automatic recording of creation time

### Task Viewing
- **Multiple Views**: Different sorting options for task lists
- **Detailed View**: Comprehensive task information display
- **Category Organization**: View tasks by their categories

### Task Management
- **Task Completion**: Mark tasks as complete
- **Category Management**: Create and delete categories
- **Task Organization**: Keep tasks organized by categories

### Profile Management
- **Edit Details**: Update personal information
- **Data Validation**: Ensure correct format for contact details
- **Profile Updates**: Seamless profile information updates

## Error Handling

The bot includes comprehensive error handling for:
- Invalid input formats
- Missing information
- Incorrect dates/times
- Invalid phone numbers
- Invalid email formats


## Author

- Developed by **GhostKX**
- Github: **[GhostKX](https://github.com/GhostKX/Task-Management-bot)**

## Acknowledgments

- PyTelegramBotAPI team for the excellent bot framework
- Contributors who have helped improve the bot
- Users who provide valuable feedback

## Support

For support, please create an issue in the GitHub repository or contact the maintainers.