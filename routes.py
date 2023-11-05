from flask import Blueprint, render_template, session, request, redirect, url_for, flash
import sqlite3

main_bp = Blueprint('main', __name__)

# root
@main_bp.route('/')
def root():
    return render_template('index.html')

# user
@main_bp.route('/user/login')
def root_user_login():
    return render_template('user/login_form.html')

@main_bp.route('/user/login/process', methods=['POST'])
def root_user_login_process():
    if request.method == 'POST':
        id = request.form['id']
        passwd = request.form['passwd']

        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()

        cursor.execute('''SELECT id, name
                          FROM user 
                          WHERE id=? AND passwd=?''', 
                       (id, passwd))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['user'] = user
            return redirect('/user')
        else:
            flash('Login Failed. Please check your ID and Password.', 'error')
    return render_template('user/login_form.html')

@main_bp.route('/user/logout')
def root_user_logout():
    if 'user_id' in session:
        session.pop('user', None)
        return redirect('/')
    else:
        pass

@main_bp.route('/user/signup')
def root_user_signup():
    return render_template('user/signup_form.html')

@main_bp.route('/user/signup/process', methods=['POST'])
def root_user_signup_process():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        passwd = request.form['passwd']
        phone = request.form['phone']
        birthday = request.form['birthday']
        license_num = request.form['license_num']
        expiration_date = request.form['expiration_date']
        card_num = request.form['card_num']
        card_valid_thru = request.form['card_valid_thru']
        card_cvc = request.form['card_cvc']
        
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO user (id, name, passwd, phone, birthday)
                       VALUES (?, ?, ?, ?, ?)''',
                       (id, name, passwd, phone, birthday))
        cursor.execute('''INSERT INTO license (user_id, license_num, expiration_date)
                       VALUES (?, ?, ?)''',
                       (id, license_num, expiration_date))
        cursor.execute('''INSERT INTO payment (user_id, card_num, card_valid_thru, card_cvc)
                        VALUES (?, ?, ?, ?)''',
                       (id, card_num, card_valid_thru, card_cvc)) 
        conn.commit()
        conn.close()
        return redirect('/user/signup/success')
    return render_template('user/signup_form.html')

@main_bp.route('/user/signup/success')
def root_user_signup_success():
    return render_template('user/signup_success.html')

@main_bp.route('/user')
def root_user():
    if session.get('user_id'):
        return render_template('user/user.html')
    else:
        return redirect('/user/login')

# manager
@main_bp.route('/manager/login')
def root_manager_login():
    return render_template('manager/login_form.html')
