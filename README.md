# Healthcare Backend

Django REST Framework backend for the healthcare assignment. It supports user registration/login with JWT, patient management, doctor management, and patient-doctor assignment.

## Tech Stack

- Django
- Django REST Framework
- PostgreSQL
- djangorestframework-simplejwt

## Setup

```bash
pip install -r requirements.txt
copy .env.example .env
```

Update `.env` with your PostgreSQL credentials, then run:

```bash
python manage.py migrate
python manage.py runserver
```

## API Endpoints

Base URL:

```text
http://127.0.0.1:8000
```

For protected APIs, first register or login, copy the `access` token, then in Postman use:

```text
Authorization > Type: Bearer Token > Token: <access_token>
```

### Authentication

- `POST /api/auth/register/`
- `POST /api/auth/login/`

Register body:

```json
{
  "name": "Asha Sharma",
  "email": "asha@example.com",
  "password": "StrongPass123"
}
```

Login returns `access` and `refresh` tokens. Use the access token on protected APIs:

```http
Authorization: Bearer <access_token>
```

### Patients

- `POST /api/patients/`
- `GET /api/patients/`
- `GET /api/patients/<id>/`
- `PUT /api/patients/<id>/`
- `DELETE /api/patients/<id>/`

Patient body:

```json
{
  "name": "Patient One",
  "age": 30,
  "gender": "male",
  "phone": "9876543210",
  "address": "Mumbai",
  "medical_history": "Diabetes"
}
```

### Doctors

- `POST /api/doctors/`
- `GET /api/doctors/`
- `GET /api/doctors/<id>/`
- `PUT /api/doctors/<id>/`
- `DELETE /api/doctors/<id>/`

Doctor body:

```json
{
  "name": "Dr Rao",
  "specialization": "Cardiology",
  "phone": "9876543210",
  "email": "rao@example.com"
}
```

### Patient-Doctor Mappings

- `POST /api/mappings/`
- `GET /api/mappings/`
- `GET /api/mappings/<patient_id>/`
- `DELETE /api/mappings/<id>/`

Mapping body:

```json
{
  "patient": 1,
  "doctor": 1
}
```

## Postman Testing

Use `Authorization: No Auth` for register and login.

1. Register

```text
POST http://127.0.0.1:8000/api/auth/register/
```

```json
{
  "name": "Test User",
  "email": "test@example.com",
  "password": "StrongPass123"
}
```

2. Login

```text
POST http://127.0.0.1:8000/api/auth/login/
```

```json
{
  "email": "test@example.com",
  "password": "StrongPass123"
}
```

Use the returned `access` token as a Bearer token for the remaining requests.

3. Add patient

```text
POST http://127.0.0.1:8000/api/patients/
```

```json
{
  "name": "Rahul Sharma",
  "age": 32,
  "gender": "male",
  "phone": "9876543210",
  "address": "Delhi",
  "medical_history": "No major illness"
}
```

4. Patient read/update APIs

```text
GET    http://127.0.0.1:8000/api/patients/
GET    http://127.0.0.1:8000/api/patients/1/
PUT    http://127.0.0.1:8000/api/patients/1/
```

PUT body:

```json
{
  "name": "Rahul Sharma",
  "age": 33,
  "gender": "male",
  "phone": "9876543210",
  "address": "Mumbai",
  "medical_history": "No major illness"
}
```

5. Add doctor

```text
POST http://127.0.0.1:8000/api/doctors/
```

```json
{
  "name": "Dr Mehta",
  "specialization": "Cardiology",
  "phone": "9876543211",
  "email": "mehta@example.com"
}
```

6. Doctor read/update APIs

```text
GET    http://127.0.0.1:8000/api/doctors/
GET    http://127.0.0.1:8000/api/doctors/1/
PUT    http://127.0.0.1:8000/api/doctors/1/
```

PUT body:

```json
{
  "name": "Dr Mehta",
  "specialization": "Neurology",
  "phone": "9876543211",
  "email": "mehta@example.com"
}
```

7. Mapping APIs

Make sure patient `1` and doctor `1` exist before creating a mapping.

```text
POST   http://127.0.0.1:8000/api/mappings/
GET    http://127.0.0.1:8000/api/mappings/
GET    http://127.0.0.1:8000/api/mappings/1/
DELETE http://127.0.0.1:8000/api/mappings/1/
```

POST body:

```json
{
  "patient": 1,
  "doctor": 1
}
```

For `GET /api/mappings/1/`, `1` is the `patient_id`. For `DELETE /api/mappings/1/`, `1` is the mapping ID.

8. Delete patient or doctor after mapping tests

```text
DELETE http://127.0.0.1:8000/api/patients/1/
DELETE http://127.0.0.1:8000/api/doctors/1/
```

## Tests

The project is configured for PostgreSQL by default. For local automated tests without PostgreSQL, use SQLite only for the test run:

```powershell
$env:DB_ENGINE="django.db.backends.sqlite3"; python manage.py test
```
