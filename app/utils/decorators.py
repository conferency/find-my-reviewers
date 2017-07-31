from functools import wraps
from app import app
from config import anon
from flask import session, redirect, url_for, current_app


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        with app.app_context():
            if 'profile' not in session:
                if not current_app.config["ALLOW_ANON"]:
                    # Redirect to Login page here
                    return redirect(url_for('main.login'))
                else:
                    session['profile'] = anon
            else:
                print(session['profile'])
            return f(*args, **kwargs)
    return decorated
