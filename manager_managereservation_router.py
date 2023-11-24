from flask import Blueprint, render_template, session, request, redirect, flash
import sqlite3

manager_managereservation_bp = Blueprint('manager_managereservation_bp', __name__)

# manager manage reservation
@manager_managereservation_bp.route('/manager/managereservation')
def root_manager_managereservation():
    if session.get('manager_session'):
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM reservation
        ''')
        reservation_data = cursor.fetchall()
        conn.close()
        return render_template('manager/manage_reservation/managereservation.html',
                                reservation_data=reservation_data)
    else:
        return render_template('manager/auth/login_form.html')

@manager_managereservation_bp.route('/manager/managereservation/delete/<int:id>', methods=['GET'])
def root_manager_managereservation_delete(id):
    if session.get('manager_session'):
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM reservation WHERE id=?''', (id,))
        conn.commit()
        conn.close()
        return redirect('/manager/managereservation')
    else:   
        return render_template('manager/auth/login_form.html')