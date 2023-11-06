from flask import Blueprint, render_template, session, request, redirect, url_for, flash
import sqlite3

main_bp = Blueprint('main', __name__)

# root
@main_bp.route('/')
def root():
    return render_template('index.html')

@main_bp.route('/user/login/process', methods=['POST'])
def root_user_login_process():
    if request.method == 'POST':
        id = request.form['id']
        passwd = request.form['passwd']
        print(f'[INFO] 입력된 id: {id}, passwd: {passwd}')

        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()

        cursor.execute('''SELECT id
                          FROM user 
                          WHERE id=? AND passwd=?''', 
                       (id, passwd))
        user_id = cursor.fetchone()
        conn.close()
        if user_id:
            session['user_session'] = user_id
            return redirect('/user')
        else:
            flash('Login Failed. Please check your ID and Password.', 'error')
    return render_template('user/auth/login_form.html')

@main_bp.route('/user/logout')
def root_user_logout():
    if 'user_session' in session:
        session.pop('user_session', None)
        return redirect('/')
    else:
        pass

@main_bp.route('/user/signup')
def root_user_signup():
    return render_template('user/auth/signup_form.html')

@main_bp.route('/user/signup/process', methods=['POST'])
def root_user_signup_process():
    if request.method == 'POST':
        # check if id is already exists
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        id = request.form['id']
        cursor.execute('''SELECT id FROM user WHERE id=?''', (id,))
        existing_id = cursor.fetchone()
        conn.close()

        if existing_id: #if id is already exists
            flash('Signup Failed. ID already exists.', 'error')
            return render_template('user/auth/signup_form.html')
        else:
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
    return render_template('user/auth/signup_form.html')

@main_bp.route('/user/signup/success')
def root_user_signup_success():
    return render_template('user/auth/signup_success.html')

@main_bp.route('/user')
def root_user():
    if session.get('user_session'):
        return render_template('user/user.html')
    else:
        return render_template('user/auth/login_form.html')
    
@main_bp.route('/user/account')
def root_user_account():
    if session.get('user_session'):
        return render_template('user/auth/account.html')
    else:
        return render_template('user/auth/login_form.html')

@main_bp.route('/user/account/edit')
def root_user_account_edit():
    if session.get('user_session'):
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        user_id = session['user_session'][0]
        cursor.execute('''SELECT name, passwd, phone, birthday
                          FROM user 
                          WHERE id=?''', 
                       (user_id,))
        user = cursor.fetchone()
        cursor.execute('''SELECT license_num, expiration_date
                          FROM license 
                          WHERE user_id=?''', 
                       (user_id,))
        license = cursor.fetchone()
        cursor.execute('''SELECT card_num, card_valid_thru, card_cvc
                          FROM payment 
                          WHERE user_id=?''', 
                       (user_id,))
        payment = cursor.fetchone()
        conn.close()
        return render_template('user/auth/account_edit_form.html', user=user, license=license, payment=payment)
    else:
        return render_template('user/auth/login_form.html')

@main_bp.route('/user/account/edit/process', methods=['POST'])
def root_user_account_edit_process():
    if session.get('user_session'):
        if request.method == 'POST':
            id = session['user_session'][0]
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
            cursor.execute('''UPDATE user 
                              SET name=?, passwd=?, phone=?, birthday=?
                              WHERE id=?''',
                           (name, passwd, phone, birthday, id))
            cursor.execute('''UPDATE license 
                              SET license_num=?, expiration_date=?
                              WHERE user_id=?''',
                           (license_num, expiration_date, id))
            cursor.execute('''UPDATE payment 
                              SET card_num=?, card_valid_thru=?, card_cvc=?
                              WHERE user_id=?''',
                           (card_num, card_valid_thru, card_cvc, id))
            conn.commit()
            conn.close()
            return redirect('/user/account')
    else:
        return render_template('user/auth/login_form.html')

@main_bp.route('/user/account/delete')
def root_user_account_delete():
    if session.get('user_session'):
        return render_template('user/auth/account_delete.html')
    else:
        return render_template('user/auth/login_form.html')

@main_bp.route('/user/account/delete/process')
def root_user_account_delete_process():
    if session.get('user_session'):
        id = session['user_session'][0]
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM user WHERE id=?''', (id,))
        conn.commit()
        conn.close()
        return redirect('/user/logout')
    else:
        return render_template('user/auth/login_form.html')

# manager
@main_bp.route('/manager/login/process', methods=['POST'])
def root_manager_login_process():
    MANAGER_PASSWORD = 'manager1234'
    MANAGER_SESSION_VALUE = '1234ABCD'
    if request.method == 'POST':
        password = request.form['password']

        if password == MANAGER_PASSWORD:
            print(f'[INFO] manager 인증 성공')
            session['manager'] = MANAGER_SESSION_VALUE
            return redirect('/manager')
        else:
            flash('Login Failed. Incorrect manager password', 'error')
    return render_template('manager/auth/login_form.html')


@main_bp.route('/manager')
def root_manager_login():
    if session.get('manager'):
        return render_template('manager/manager.html')
    else:
        return render_template('manager/auth/login_form.html')
