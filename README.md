# Employee Management System (EMS) – Django + DRF + JWT

A production-ready backend for managing **employees, departments, attendance, and leave requests**.

## Quickstart

```bash
python -m venv venv
Windows: venv\Scripts\activate  #source venv/bin/activate (Mac)
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Swagger docs: `http://127.0.0.1:8000/swagger/`

## Roles
- `admin`, `hr`, `manager`, `employee`

## Auth
- `POST /api/users/` – register
- `POST /api/token/` – login (JWT)
- `POST /api/token/refresh/` – refresh access token

## Core Endpoints
- Departments: `/api/departments/` (Admin/HR)
- Employees: `/api/employees/` (Admin/HR full; Manager dept-only; Employee self)
- Attendance: `/api/attendance/` (Employees create own; Manager/HR manage all)
- Leaves: `/api/leaves/` (+ `/api/leaves/{id}/approve/`, `/api/leaves/{id}/reject/` for Manager/HR/Admin)
```