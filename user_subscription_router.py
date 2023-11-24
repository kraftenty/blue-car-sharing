from flask import Blueprint, render_template, session, request, redirect, url_for, flash
import sqlite3

user_subscription_bp = Blueprint('user_subscription_bp', __name__)

# user subscription
def isOnSubscribe(user_id): # return True if user is on subscribe
    conn = sqlite3.connect('data/data.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM subscribe
                   WHERE user_id=?''', (user_id,))
    ret = cursor.fetchone()
    print(f'[INFO] ret  : {ret}')
    conn.close()
    if ret:
        return True
    else:
        return False

@user_subscription_bp.route('/user/subscription')
def root_user_subscription():
    if session.get('user_session'):
        user_id = session['user_session'][0]
        print(f'[INFO] user_id: {user_id}')
        print(f'[INFO] isOnSubscribe: {isOnSubscribe(user_id)}')
        if isOnSubscribe(user_id):
            return render_template('user/subscription/on_subscribe.html')
        else:
            return render_template('user/subscription/recommend_subscribe.html')
    else:
        return render_template('user/auth/login_form.html')

@user_subscription_bp.route('/user/subscription/process')
def root_user_subscription_process():
    if session.get('user_session'):
        user_id = session['user_session'][0]
        if not isOnSubscribe(user_id): # subscribe
            conn = sqlite3.connect('data/data.db')
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO subscribe (user_id) VALUES (?)''', (user_id,))
            conn.commit()
            conn.close()
            return redirect('/user/subscription')
        else: # unsubscribe
            conn = sqlite3.connect('data/data.db')
            cursor = conn.cursor()
            cursor.execute('''DELETE FROM subscribe WHERE user_id=?''', (user_id,))
            conn.commit()
            conn.close()
            return redirect('/user/subscription')
    else:
        return render_template('user/auth/login_form.html')