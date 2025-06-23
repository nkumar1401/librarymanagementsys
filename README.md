 Library Management System API – Django 

This is a backend system I built for managing a library, using Django and Django REST Framework. It includes basic features like book management, borrow request handling, JWT-based login system, and librarian/student roles.

---

 Key Features

- JWT Authentication (login, refresh)
- Role-based access: Librarian vs Student
- Book creation, update, delete (for librarians)
- Borrowing system with request/approve/return flows
- Auto-updates available copies using Django signals
- Book reviews with user association

---


```bash
# Clone the repo
git clone https://github.com/nkumar1401/librarymanagementsys.git
cd librarymanagementsys

# Set up virtual environment
python -m venv myenv
myenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start the server
python manage.py runserver
