# Django Fintech Payment Project

A Fintech-style Django project with user authentication, KYC submission, dashboard features, transactions, and more.

Follow the steps below to set up and run this project locally.

---

## Installation & Setup

### **1. Install Dependencies**

Open a terminal in the project root directory (where `manage.py` exists) and run:

```bash
pip install -r requirements.txt


### Create a .env File

In the root directory, create a new file named .env and add:

SECRET_KEY=your_django_project_secret_key
DEBUG=your_debug_value

Use True or False for the debug value based on your environment.

### Create a Superuser (Admin Account)

Run the following command:

python manage.py createsuperuser


Enter your desired username, email, and password.
When prompted about password validation, type: y

to bypass the strength check.


### Start the Development Server

Run:

python manage.py runserver


The project will now be available at:

http://127.0.0.1:8000/

###. Access the Admin Panel

Open:

http://127.0.0.1:8000/admin

Log in using the superuser credentials you created.


Project Structure -->
payment_prj/ – Main Django project
account/ – User accounts, KYC, dashboard
core/ – Transactions, transfers, cards
userauths/ – Custom user authentication
templates/ – HTML templates
static/ – CSS, JS, images
media/ – Uploaded user files

You're Ready!

The project should now be running fully on your local machine.
If you encounter any issues, feel free to ask for help.
