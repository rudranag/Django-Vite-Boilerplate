# Django-React Integration Project

This project demonstrates the integration of Django (backend) with React (frontend) using Vite as the build tool for the React application.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Prerequisites](#prerequisites)
3. [Setup](#setup)
   - [Backend (Django) Setup](#backend-django-setup)
   - [Frontend (React) Setup](#frontend-react-setup)
4. [Running the Application](#running-the-application)
5. [Django-React Integration](#django-react-integration)
6. [Project Structure](#project-structure)
7. [Additional Notes](#additional-notes)

## Project Overview

This project combines a Django backend with a React frontend. Django serves as the API and handles server-side logic, while React provides a dynamic and responsive user interface.

## Prerequisites

- Python 3.11
- Node.js 20.11.0
- npm 10 

## Setup

### Backend (Django) Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <project-directory>
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install Django and other dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```
   python manage.py migrate
   ```

   Note: A superuser is automatically created during migration with the following credentials:
   - Username: admin
   - Password: admin

   You can use these credentials to access the Django admin interface.

### Frontend (React) Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   # or
   yarn install
   ```

## Running the Application in React Dev Mode

1. Start the Django development server:
   ```
   python manage.py runserver
   ```

2. In a separate terminal, build the React application:
   ```
   cd frontend
   npm run dev
   # or
   yarn dev
   ```

## Running the Application in React Production Mode

1. Remove `INTERNAL_IPS` variable from settings.py
2. Start the Django development server:
   ```
   python manage.py runserver
   ```

2. In a separate terminal, build the React application:
   ```
   cd frontend
   npm run build
   # or
   yarn build
   ```

3. Access the application:
   - Django admin: http://localhost:8000/admin/
   - React app: http://localhost:8000/r/
   - A Sample Todo App using Material UI: http://localhost:8000/r/todo

Note: The behavior of the React app in development and production environments is controlled by the `INTERNAL_IPS` setting in Django's `settings.py`. This setting determines whether the React app is served as static files by Django or if it should use the Vite development server.

## Django-React Integration

This project integrates Django and React using the following approach:

1. **Django as the Backend:**
   - Django serves as the API backend.
   - It handles database operations, authentication, and other server-side logic.
   - Django's `apps.vite_integration` app manages the integration with the React frontend.

2. **React as the Frontend:**
   - React application is set up using Vite for fast development and optimized production builds.
   - It's located in the `frontend` directory.

3. **Integration Mechanism and react_base.html:**
   - The integration is controlled by the `INTERNAL_IPS` setting in `settings.py`.
   - The `react_base.html` file in `apps/vite_integration/templates/` is crucial for rendering the React application within Django.
   - Behavior based on `INTERNAL_IPS`:
     - When the client IP is in `INTERNAL_IPS` (development mode):
       - It includes scripts to connect to the Vite development server (running on port 9900).
       - Enables Hot Module Replacement (HMR) for React.
       - Loads the main React entry point (`main.tsx`) from the Vite dev server.
     - When the client IP is not in `INTERNAL_IPS` (production mode):
       - React app is built using Vite.
       - Django serves the built React files as static assets.
       - Uses the `render_vite_bundle` template tag to include the correct React bundle.

4. **Routing:**
   - React Router handles frontend routing.
   - Django's URL configuration is set up to allow React to handle routes starting with `/r/`.

5. **API Communication:**
   - React uses Axios to make API calls to the Django backend.
   - Django Rest Framework is used to create API endpoints.

## Project Structure

```
project_root/
│
├── DjTodos/                 # Django project settings
├── apps/
│   ├── todos/               # Django app for todo functionality
│   ├── swagger/             # Django app for API documentation
│   └── vite_integration/    # Django app for React integration
│
├── frontend/                # React application
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── api/
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── manage.py
└── requirements.txt
```

## Additional Notes

- The project uses Django's session-based authentication.
- API documentation is available via Swagger UI at `/swagger/`.
- The React app is configured to proxy API requests to the Django server in development.
- Environment variables are managed using `django-environ` for the backend and Vite's env handling for the frontend.

For more detailed information on specific components or functionalities, please refer to the respective files and their comments in the project.