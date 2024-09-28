# Instagram Blog Django Application

## Overview

This is an Instagram-like blog application built using Django, featuring user profiles, post creation, commenting, and following functionalities. Users can share their posts, follow other users, and interact through comments.

## Features

- User registration and authentication
- Profile creation and updating
- Post creation with images and captions
- Commenting on posts
- Following and unfollowing users
- Responsive design for mobile and desktop

## Technologies Used

- Django
- Django Rest Framework
- PostgreSQL / SQLite (database)
- HTML, CSS, JavaScript (for frontend)
- Bootstrap (for responsive design)
- Pillow (for image handling)

## Installation

### Prerequisites

- Python 3.x
- Django
- Pip

### Steps

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/instagram-blog-django.git
   cd instagram-blog-django

2. **Create a virtual environment:**


python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install dependencies:**


pip install -r requirements.txt

4. **Setup the database:**

If using SQLite, it’s ready to go.
If using PostgreSQL, create a database and update settings.py with your database credentials.

5. **Run migrations:**


python manage.py migrate

6. **Create a superuser:**


python manage.py createsuperuser

7. **Run the server:**


python manage.py runserver

8. **Access the application:**

Open your web browser and go to http://127.0.0.1:8000/

## Usage
- Registration: Users can register to create a new account.
- Login: Registered users can log in to access their profiles.
- Profile: Users can view and edit their profiles.
- Posts: Users can create, view, and comment on posts.
- Follow/Unfollow: Users can follow or unfollow others.

## Contributing

Fork the project
- Create your feature branch (git checkout -b feature/YourFeature)
- Commit your changes (git commit -m 'Add some feature')
- Push to the branch (git push origin feature/YourFeature)
- Open a pull request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
Inspiration from Instagram
Django Documentation
Bootstrap for responsive design


### Customization

- Replace `https://github.com/yourusername/instagram-blog-django.git` with the actual repository link.
- Make sure the instructions reflect your project's specific requirements and dependencies.
- Add any additional features or notes that are relevant to your application.


## For appreciation and consultation
- gadafisteve001@gmail.com
- 0112284093