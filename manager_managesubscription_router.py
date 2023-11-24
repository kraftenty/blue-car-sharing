from flask import Blueprint, render_template, session, request, redirect, flash
import sqlite3

manager_managesubscription_bp = Blueprint('manager_managesubscription_bp', __name__)

# manager manage subscription
@manager_managesubscription_bp.route('/manager/managesubscription')
def root_manager_managesubscription():
    if session.get('manager_session'):
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM subscribe''')
        subscribe_data = cursor.fetchall()
        conn.close()
        return render_template('manager/manage_subscription/managesubscription.html',
                                subscribe_data=subscribe_data)
    else:
        return render_template('manager/auth/login_form.html')

@manager_managesubscription_bp.route('/manager/managesubscription/delete/<string:user_id>', methods=['GET'])
def root_manager_managesubscription_delete(user_id):
    if session.get('manager_session'):
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM subscribe WHERE user_id=?''', (user_id,))
        conn.commit()
        conn.close()
        return redirect('/manager/managesubscription')
    else:   
        return render_template('manager/auth/login_form.html')
