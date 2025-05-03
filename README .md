# CardioCheck – Cardiovascular Risk Assessment Web App

CardioCheck is a web-based application that enables users to assess their cardiovascular disease (CVD) risk, access educational health materials, and locate nearby hospitals for specialist care.

## Features

- Cardiovascular risk calculator based on QRISK3
- Educational resource library focused on lifestyle modification
- Hospital locator using Google Maps API
- Blog system with comments, replies, upvotes, and downvotes
- User authentication: signup, login, logout
- Admin-only creation of blogs and educational resources
- Fully mobile-responsive design

## Technology Stack

- Backend: Django 5.1
- Frontend: Bootstrap 5
- Database: PostgreSQL (Supabase)
- APIs: Google Maps & Places API
- Authentication: Django built-in authentication
- Deployment support: Gunicorn, Whitenoise

## Project Structure

core/
├── models.py
├── views.py
├── forms.py
├── templates/
│   ├── authentication/
│   ├── blogs/
│   ├── hospital_finder.html
│   ├── educational_resources.html
│   ├── risk_assessment/
│   ├── dashboard.html
│   ├── partials/
├── static/
manage.py
requirements.txt
README.md

## Setup Instructions

### 1. Clone the Project

```bash
git clone <repository-url>
cd CardiovascularProject

2. Create and Activate Virtual Environment

python -m venv venv
venv\Scripts\activate        # On Windows
source venv/bin/activate     # On Mac/Linux

3. Install Dependencies

pip install --upgrade pip
pip install -r requirements.txt

4. Create .env File

DATABASE_URL=your-database-url
SECRET_KEY=your-django-secret-key
DEBUG=True
GOOGLE_MAPS_API_KEY=your-google-maps-api-key

5. Apply Migrations

python manage.py migrate

6. Create a Superuser

python manage.py createsuperuser

7. Run the Server

python manage.py runserver

Environment Variables

Variable	Description
DATABASE_URL	PostgreSQL database connection string
SECRET_KEY	Django secret key
DEBUG	Set to True for development
GOOGLE_MAPS_API_KEY	Google Maps API Key for hospital locator

Deployment Notes
	•	Use Gunicorn as the WSGI server.
	•	Serve static files with Whitenoise.
	•	Secure environment variables properly.
	•	Set DEBUG=False and configure ALLOWED_HOSTS.

Future Enhancements
	•	Email notifications after assessment
	•	Historical risk tracking for users
	•	Machine learning-based advanced risk prediction

License

Academic use only. All rights reserved © 2025.
