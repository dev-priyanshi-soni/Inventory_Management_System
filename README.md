# Inventory Management System

## Overview
The Inventory Management System.

## Features
- **User Authentication**: Secure login and registration for users 
- **Product Management**: Add, edit, and delete products.
- **Caching**: Used Redis Caching for storing product details.
- **Postgres Database**: SQL based database used.
- **JWT Authentication Used** : Security purpose.


## Install requirements
   pip install -r requirements.txt

## Make migrations
   python manage.py makemigrations and then    
   python manage.py migrate

## Run the server
   python manage.py runserver
