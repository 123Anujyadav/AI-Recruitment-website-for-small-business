# Admin Panel Access

This document contains the credentials and instructions for accessing the Django admin panel of the TalentAI MVP application.

## Credentials

- **Username**: `admin`
- **Password**: `admin123`

## How to Access

1. Ensure the backend server is running:
   ```bash
   python manage.py runserver
   ```
   (Or double-click the `run.bat` file).

2. Open your web browser and navigate to:
   [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

3. Log in using the credentials provided above.

## Features Available

From the admin panel, you can:
- View and manage Users (Both Candidates and Employers).
- View, create, update, and delete Jobs manually.
- Inspect and manage Job Applications and match scores.

*Note: These credentials are for local development and demonstration purposes only. You can create more admin users using the `python manage.py createsuperuser` command.*
