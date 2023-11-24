from flask import Blueprint, render_template, session, request, redirect, flash
import sqlite3

manager_viewincome_bp = Blueprint('manager_viewincome_bp', __name__)

# viewincome
@manager_viewincome_bp.route('/manager/viewincome')
def root_manager_viewincome():
    if session.get('manager_session'):
        return render_template('manager/view_income/viewincome.html')
    else:
        return render_template('manager/auth/login_form.html')

@manager_viewincome_bp.route('/manager/viewincome/calculated', methods=['POST'])
def root_manager_viewincome_calculated():
    if session.get('manager_session') and request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        date_information = (start_date, end_date)
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT SUM(tot_price)
                          FROM reservation 
                          WHERE start_date >= ? AND end_date <= ?''', (start_date, end_date))
        total_income = cursor.fetchone()
        cursor.execute('''SELECT COUNT(subscribe.user_id)
                          FROM subscribe''')
        total_subscriber = cursor.fetchone()
        conn.close()
        return render_template('manager/view_income/income_calculated.html',
                                total_income=total_income,
                                total_subscriber=total_subscriber,
                                date_information=date_information)
    else:
        return render_template('manager/auth/login_form.html')