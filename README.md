# Recibos Online - Python Flask Version

This is a Python Flask version of the original PHP receipt generation system, using PostgreSQL instead of MySQL.

## Features
- User registration and login
- Receipt generation with payer and receiver details
- Receipt viewing and printing
- Receipt history

## Setup

1. Install PostgreSQL and create a database named 'recibos'.

2. Install Python dependencies:
   ```
   pip install flask sqlalchemy psycopg2-binary flask-wtf flask-login
   ```

3. Update `config.py` with your PostgreSQL connection details.

4. Run the database initialization:
   ```
   python init_db.py
   ```

5. Run the application:
   ```
   python app.py
   ```

6. Access the application at http://localhost:5000

## Original Project
This is based on the PHP project located at `d:\Programacao Web\recibo\`, maintaining identical layout and functionalities.