from flask import Blueprint, render_template, session, request, redirect, flash
import sqlite3

manager_auth_bp = Blueprint('manager_auth_bp', __name__)

# manager auth
MANAGER_PASSWORD = 'manager1234'
MANAGER_SESSION_VALUE = '1234ABCD'
@manager_auth_bp.route('/manager')
def root_manager_login():
    if session.get('manager_session'):
        return render_template('manager/manager.html')
    else:
        return render_template('manager/auth/login_form.html')

@manager_auth_bp.route('/manager/login/process', methods=['POST'])
def root_manager_login_process():
    if request.method == 'POST':
        password = request.form['password']
        if password == MANAGER_PASSWORD:
            print(f'[INFO] manager 인증 성공')
            session['manager_session'] = MANAGER_SESSION_VALUE
            return redirect('/manager')
        else:
            flash('Login Failed. Incorrect manager password', 'error')
    return render_template('manager/auth/login_form.html')

@manager_auth_bp.route('/manager/logout')
def root_manager_logout():
    if session.get('manager_session'):
        session.pop('manager_session', None)
        return redirect('/')
    else:
        return redirect('/manager')