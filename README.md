#  Hospital Appointment Booking System

## Overview
**Hospital** is a Django-based web application designed to manage hospital Appointments Booking efficiently. The system handles staff and patient accounts, appointments, and provides a responsive interface with role-based permissions.

---

## Features

### User Management
- **Staff and Patient Accounts**: Both staff and patients can create accounts and login using **mobile number and password**.
- **Admin Control**: Admin can **add, update, and delete** both staff and patient accounts via Django admin.

### Patient Appointment Management
- Patients can **book appointments** with doctors.
- Patients can **cancel their own appointments** after booking.
- Management and Admin can **update visit status** (`visited` / `not_visited`).
- **Search and filter** appointments by patient name, phone number, or specialist.

### User Experience
- **Responsive design** for desktop and mobile devices.
- **Pop-up modals** for booking and visit status updates.
- **Smooth alerts** for messages and actions.

---

## Technology Stack
- **Backend:** Python, Django  
- **Frontend:** HTML, CSS, Bootstrap 5, JavaScript  
- **Database:** SQLite (default)  

---

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/<jayabalaji1011>/Hospital.git
cd Hospital
