from flask import Blueprint, render_template, session, request, redirect, flash
import sqlite3

manager_manageuser_bp = Blueprint('manager_manageuser_bp', __name__)

# manager manage user
@manager_manageuser_bp.route('/manager/manageuser')
def root_manager_manageuser():
    if session.get('manager_session'):
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT u.id, u.name, u.passwd, u.phone, u.birthday,
                   l.license_num, l.expiration_date,
                   p.card_num, p.card_valid_thru, p.card_cvc
            FROM user AS u
            INNER JOIN license AS l ON u.id = l.user_id
            INNER JOIN payment AS p ON u.id = p.user_id
        ''')
        joined_user_data = cursor.fetchall()
        conn.close()
        return render_template('manager/manage_user/manageuser.html',
                                joined_user_data=joined_user_data)
    else:
        return render_template('manager/auth/login_form.html')

@manager_manageuser_bp.route('/manager/manageuser/delete/<string:user_id>', methods=['GET'])
def root_manager_manageuser_delete(user_id):
    if session.get('manager_session'):
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM user WHERE id=?''', (user_id,))
        conn.commit()
        conn.close()
        return redirect('/manager/manageuser')
    else:   
        return render_template('manager/auth/login_form.html')