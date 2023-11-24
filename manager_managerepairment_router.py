from flask import Blueprint, render_template, session, request, redirect, flash
import sqlite3

manager_managerepairment_bp = Blueprint('manager_managerepairment_bp', __name__)

# manager manage repairment
@manager_managerepairment_bp.route('/manager/managerepairment')
def root_manager_managerepairment():
    if session.get('manager_session'):
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM repairment
        ''')
        repairment_data = cursor.fetchall()
        conn.close()
        return render_template('manager/manage_repairment/managerepairment.html',
                                repairment_data=repairment_data)
    else:
        return render_template('manager/auth/login_form.html')

@manager_managerepairment_bp.route('/manager/managerepairment/delete/<string:number>', methods=['GET'])
def root_manager_managerepairment_delete(number):
    if session.get('manager_session'):
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM repairment WHERE number=?''', (number,))
        conn.commit()
        conn.close()
        return redirect('/manager/managerepairment')
    else:   
        return render_template('manager/auth/login_form.html')

@manager_managerepairment_bp.route('/manager/managerepairment/add')
def root_manager_managerepairment_add():
    if session.get('manager_session'):
        return render_template('manager/manage_repairment/repairment_add.html')
    else:
        return render_template('manager/auth/login_form.html')

@manager_managerepairment_bp.route('/manager/managerepairment/add/process', methods=['POST'])
def root_manager_managerepairment_add_process():
    if session.get('manager_session') and request.method == 'POST':
        first_number = request.form['first_number']
        middle_number = request.form['middle_number']
        last_number = request.form  ['last_number']
        number = first_number + middle_number + last_number
        reason = request.form['reason']
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO repairment VALUES (?, ?)''',
            (number, reason)
        )
        conn.commit()
        conn.close()
        return redirect('/manager/managerepairment')
    else:
        return render_template('manager/auth/login_form.html')
