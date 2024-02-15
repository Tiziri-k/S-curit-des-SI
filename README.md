
This  project implements a simple authentication system with user login and account creation features. Users can register accounts and log in to access protected routes.

## Features

- User account creation
- User login with authentication
- Protected routes for authenticated users
- Error handling for common scenarios


## Prerequisites

- Python 3.x
- Flask
- Flask-WTF
- Flask-Bcrypt
- SQLite

## Usage
Visit the registration page to create an account.
Log in using your credentials.
Access the protected route to see the example of a protected page.

## Project Structure
app.py: Main Flask application file.
templates/: HTML templates for rendering pages.
static/: Static files like images and stylesheets.
error.log: Log file for application errors.



## Security

### Password Hashing

User passwords are securely hashed using the `bcrypt` algorithm through Flask-Bcrypt. This ensures that passwords are not stored in plain text, adding an extra layer of protection to user accounts.

### CSRF Protection

Cross-Site Request Forgery (CSRF) attacks are mitigated through the use of Flask-WTF's CSRF protection. Unique tokens are generated and validated for each form submission, preventing malicious cross-site requests.

### Environment Variables

Sensitive information, such as the database URL, is stored in environment variables (see `.env` file).  to keep these variables confidential and not expose them in public repositories.

### Error Handling

The project includes basic error handling to provide informative error messages during development, while generic error messages are displayed in production to avoid exposing sensitive information.

### Session Management

Flask handles user authentication through session management. Ensure that session data is stored securely and consider implementing best practices for session security.

### Logging and Monitoring

Errors are logged to a file (`error.log`). For a production environment,  integrating a logging and monitoring system to detect and respond to security incidents.


