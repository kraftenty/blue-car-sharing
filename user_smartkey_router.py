from flask import Blueprint, render_template, session, request, redirect, url_for, flash
import sqlite3

user_smartkey_bp = Blueprint('user_smartkey_bp', __name__)

# smartkey
@user_smartkey_bp.route('/user/smartkey')
def root_user_smartkey():
    if session.get('user_session'):
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        user_id = session['user_session'][0]
        cursor.execute('''SELECT * FROM reservation WHERE user_id=?''', (user_id,))
        reservation_data = cursor.fetchone()
        if reservation_data is None:
            conn.close()
            return render_template('user/smartkey/noreservation.html')
        cursor.execute('''SELECT * FROM car WHERE number=?''', (reservation_data[1],))
        car_data = cursor.fetchone()
        cursor.execute('''SELECT * FROM model WHERE id=?''', (car_data[1],))
        model_data = cursor.fetchone()
        conn.close()
        return render_template('user/smartkey/smartkey.html',
            reservation_data=reservation_data, car_data=car_data, model_data=model_data)
    else:
        return render_template('user/auth/login_form.html')

@user_smartkey_bp.route('/user/smartkey/cancelreservation')
def root_user_smartkey_cancelreservation():
    if session.get('user_session'):
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        user_id = session['user_session'][0]
        cursor.execute('''DELETE FROM reservation WHERE user_id=?''', (user_id,))
        conn.commit()
        conn.close()
        return redirect('/user/smartkey',)
    else:
        return render_template('user/auth/login_form.html')