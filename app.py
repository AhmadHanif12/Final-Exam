from flask import Flask, request, render_template, jsonify, redirect, url_for, flash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
import logging
from datetime import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

# Configure logging
logging.basicConfig(
    filename='security.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages

# Configure Flask-Limiter with explicit memory storage
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri="memory://",
    default_limits=["200 per day", "50 per hour"]
)

# Configure CSP and security headers with Talisman
csp = {
    'default-src': "'self'",
    'script-src': "'self'",
    'style-src': "'self'",
    'img-src': "'self'",
    'font-src': "'self'",
    'frame-ancestors': "'none'",
}

Talisman(
    app,
    force_https=True,
    strict_transport_security=True,
    session_cookie_secure=True,
    content_security_policy=csp
)

# In-memory storage for demonstration
users = {}

# Security logging decorator
def log_security_event(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logging.info(f'Security event: {f.__name__} accessed by {request.remote_addr}')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
@log_security_event
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users:
            flash('Username already exists')
            return redirect(url_for('signup'))
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long')
            return redirect(url_for('signup'))
            
        # Store hashed password
        users[username] = {
            'password': generate_password_hash(password),
            'created_at': datetime.now()
        }
        
        logging.info(f'New user registered: {username}')
        flash('Registration successful! Please login.')
        return redirect(url_for('index'))
        
    return render_template('signup.html')

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
@log_security_event
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    user = users.get(username)
    if user and check_password_hash(user['password'], password):
        logging.info(f'Successful login for user: {username}')
        return jsonify({"status": "success"})
    
    logging.warning(f'Failed login attempt from IP: {request.remote_addr}')
    return jsonify({"status": "failed"}), 401

@app.route('/sensitive-data')
@limiter.limit("10 per minute")
@log_security_event
def sensitive_data():
    return jsonify({"data": "This is sensitive information"})

@app.errorhandler(429)
def ratelimit_handler(e):
    logging.warning(f'Rate limit exceeded by IP: {request.remote_addr}')
    return jsonify({"error": "Rate limit exceeded"}), 429

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        ssl_context=('cert.pem', 'key.pem'),
        debug=True
    )  # Set debug=False in production 