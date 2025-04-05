# Trilli

## Overview
Trilli is a powerful and intuitive application designed to help teams and individuals manage their projects efficiently. With features like boards, tasks, and member management, users can organize and collaborate seamlessly.

## Features
### 1. Authentication
- **Login:** Users can securely log in to access their projects and tasks.
- **Register:** New users can create an account to start managing their tasks.

### 2. Boards Management
- **Create:** Users can create boards to organize different projects.
- **Read:** View all boards along with their details.
- **Update:** Edit board details as required.
- **Delete:** Remove boards that are no longer needed.

### 3. Member Management in Boards
- **Add Members:** Assign members to a board for collaborative task management. Assigned members will receive invitation e-mail.
- **Remove Members:** Remove members from a board when necessary.

### 4. Task Management in Boards
- **Create:** Add tasks to boards to track progress and deadlines.
- **Read:** View tasks and current statuses.
- **Update:** Edit task information, including status updates and due dates.
- **Delete:** Remove completed or unnecessary tasks from the boards.

## Demo
You can access the application trough this link `http://202.10.36.249:8000/login/` and use this account for signing in.
```
username: testuser1
password: cobauser1
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/naputami/trilli.git
   ```

2. Navigate to the project directory:
   ```bash
   cd trilli
   ```

3. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up Postgres:
    - Make sure PostgresSQL is installed and running on your machine
    - Create database and include these variable in `.env`
    ```
    PG_DATABASE=
    PG_USER=
    PG_PASSWORD=
    PG_HOST=
    PG_PORT=
    ```
6. Set up Mailjet:
    - create Mailjet account
    - Set up API key and include these variable in `.env`
    ```
    MJ_APIKEY_PUBLIC=
    MJ_APIKEY_PRIVATE=
    ```
6. Set up Redis:
   - Make sure Redis is installed and running on your machine.
   - You can install Redis via your system's package manager or download it from the [official website](https://redis.io/).
6. Configure Huey:
   - Ensure Huey is properly configured in your Django project's settings file.
   - Example:
     ```python
     HUEY = {
         'name': 'task_manager',
         'connection': {'host': '127.0.0.1', 'port': 6379},
         'consumer': {'workers': 4, 'worker_type': 'thread'},
     }
     ```

7. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

8. Start the Redis server.

9. Run the application:
```bash
  ./manage.py runserver
```
10. Start the Huey consumer:
 ```bash
    ./manage.py run_huey
 ```

## Usage
1. Register an account or log in with your credentials.
2. Create a board and add members to collaborate on projects.
3. Add, update, or delete tasks within boards to keep the workflow organized.
4. Use the intuitive interface to view and manage all tasks with ease.

## Technologies Used
- Fullstack Framework: Django
- Database: PostgreSQL
- Task Queue: Huey & Redis
- Styling UI: Tailwind CSS, Daisy UI
- E-mail Service: Mailjet
- VPS: Linux Debian 12