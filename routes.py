from flask import Blueprint, render_template, session, request, redirect, url_for, flash
import sqlite3

main_bp = Blueprint('main', __name__)

# root
@main_bp.route('/')
def root():
    return render_template('index.html')

# user
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
        return redirect('/user')

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

# user subscription
def isOnSubscribe(user_id): # return True if user is on subscribe
    conn = sqlite3.connect('data/data.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT ? FROM subscribe''', (user_id,))
    ret = cursor.fetchone()
    conn.close()
    if ret:
        return True
    else:
        return False

@main_bp.route('/user/subscription')
def root_user_subscription():
    if session.get('user_session'):
        user_id = session['user_session'][0]
        if isOnSubscribe(user_id):
            return render_template('user/subscription/on_subscribe.html')
        else:
            return render_template('user/subscription/recommend_subscribe.html')
    else:
        return render_template('user/auth/login_form.html')

@main_bp.route('/user/subscription/process')
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

# smartkey
@main_bp.route('/user/smartkey')
def root_user_smartkey():
    if session.get('user_session'):
        return render_template('user/smartkey/smartkey.html')
    else:
        return render_template('user/auth/login_form.html')

# ------------------------------------------ manager
# manager auth
MANAGER_PASSWORD = 'manager1234'
MANAGER_SESSION_VALUE = '1234ABCD'
@main_bp.route('/manager')
def root_manager_login():
    if session.get('manager_session'):
        return render_template('manager/manager.html')
    else:
        return render_template('manager/auth/login_form.html')

@main_bp.route('/manager/login/process', methods=['POST'])
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

@main_bp.route('/manager/logout')
def root_manager_logout():
    if session.get('manager_session'):
        session.pop('manager_session', None)
        return redirect('/')
    else:
        return redirect('/manager')
    
# manager manage user
@main_bp.route('/manager/manageuser')
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

@main_bp.route('/manager/manageuser/delete/<string:user_id>', methods=['GET'])
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

# manager manage model
@main_bp.route('/manager/managemodel')
def root_manager_managemodel():
    if session.get('manager_session'):
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM model''')
        model_data = cursor.fetchall()
        conn.close()
        return render_template('manager/manage_model/managemodel.html',
                                model_data=model_data)
    else:
        return render_template('manager/auth/login_form.html')

@main_bp.route('/manager/managemodel/update/<int:model_id>', methods=['GET'])
def root_manager_managemodel_update(model_id):
    if session.get('manager_session'):
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM model WHERE id=?''', (model_id,))
        selected_model_data = cursor.fetchone()
        conn.close()
        return render_template('manager/manage_model/model_update.html',
                                selected_model_data=selected_model_data)
    else:
        return render_template('manager/auth/login_form.html')

@main_bp.route('/manager/managemodel/update/process/<int:model_id>', methods=['POST'])
def root_manager_managemodel_update_process(model_id):
    if session.get('manager_session') and request.method == 'POST':
        model_manufacturer = request.form['manufacturer']
        model_name = request.form['name']
        model_type = request.form['type']
        model_capacity = request.form['capacity']
        model_drive_range = request.form['drive_range']
        model_price_per_day = request.form['price_per_day']
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        cursor.execute('''UPDATE model 
                            SET manufacturer=?, name=?, type=?, capacity=?, drive_range=?, price_per_day=?
                            WHERE id=?''',
                        (model_manufacturer, model_name, model_type, model_capacity, model_drive_range, model_price_per_day, model_id))
        conn.commit()
        conn.close()
        return redirect('/manager/managemodel')
    else:
        return render_template('manager/auth/login_form.html')

@main_bp.route('/manager/managemodel/delete/<string:user_id>', methods=['GET'])
def root_manager_managemodel_delete(user_id):
    if session.get('manager_session'):
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM model WHERE id=?''', (user_id,))
        conn.commit()
        conn.close()
        return redirect('/manager/managemodel')
    else:   
        return render_template('manager/auth/login_form.html')

@main_bp.route('/manager/managemodel/create')
def root_manager_managemodel_create():
    if session.get('manager_session'):
        return render_template('manager/manage_model/model_create.html')
    else:
        return render_template('manager/auth/login_form.html')

@main_bp.route('/manager/managemodel/create/process', methods=['POST'])
def root_manager_managemodel_create_process():
    if session.get('manager_session') and request.method == 'POST':
        # Check if id is already exists
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        model_id = request.form['id']
        cursor.execute('''SELECT id FROM model WHERE id=?''', (model_id,))
        existing_id = cursor.fetchone()
        conn.close()
        if existing_id:
            flash('Model Create Failed. ID already exists.', 'error')
            return render_template('manager/manage_model/model_create.html')
        else:
            conn = sqlite3.connect('data/data.db')
            cursor = conn.cursor()
            model_id = request.form['id']
            model_manufacturer = request.form['manufacturer']
            model_name = request.form['name']
            model_type = request.form['type']
            model_capacity = request.form['capacity']
            model_drive_range = request.form['drive_range']
            model_price_per_day = request.form['price_per_day']
            cursor.execute('''INSERT INTO model VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (model_id, model_manufacturer, model_name,
                model_type, model_capacity, model_drive_range, model_price_per_day)
            )
            conn.commit()
            conn.close()
            return redirect('/manager/managemodel')
    else:
        return render_template('manager/auth/login_form.html')

# manager manage zone
@main_bp.route('/manager/managezone')
def root_manager_managezone():
    if session.get('manager_session'):
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM zone''')
        zone_data = cursor.fetchall()
        conn.close()
        return render_template('manager/manage_zone/managezone.html',
                                zone_data=zone_data)
    else:
        return render_template('manager/auth/login_form.html')

@main_bp.route('/manager/managezone/update/<int:zone_id>', methods=['GET'])
def root_manager_managezone_update(zone_id):
    if session.get('manager_session'):
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM zone WHERE id=?''', (zone_id,))
        selected_zone_data = cursor.fetchone()
        conn.close()
        return render_template('manager/manage_zone/zone_update.html',
                                selected_zone_data=selected_zone_data)
    else:
        return render_template('manager/auth/login_form.html')

@main_bp.route('/manager/managezone/update/process/<int:zone_id>', methods=['POST'])
def root_manager_managezone_update_process(zone_id):
    if session.get('manager_session') and request.method == 'POST':
        zone_city = request.form['city']
        zone_name = request.form['name']
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        cursor.execute('''UPDATE zone 
                            SET city=?, name=?
                            WHERE id=?''',
                        (zone_city, zone_name, zone_id))
        conn.commit()
        conn.close()
        return redirect('/manager/managezone')
    else:
        return render_template('manager/auth/login_form.html')
    
@main_bp.route('/manager/managezone/delete/<int:zone_id>', methods=['GET'])
def root_manager_managezone_delete(zone_id):
    if session.get('manager_session'):
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM zone WHERE id=?''', (zone_id,))
        conn.commit()
        conn.close()
        return redirect('/manager/managezone')
    else:   
        return render_template('manager/auth/login_form.html')

@main_bp.route('/manager/managezone/create')
def root_manager_managezone_create():
    if session.get('manager_session'):
        return render_template('manager/manage_zone/zone_create.html')
    else:
        return render_template('manager/auth/login_form.html')

@main_bp.route('/manager/managezone/create/process', methods=['POST'])
def root_manager_managezone_create_process():
    if session.get('manager_session') and request.method == 'POST':
        # Check if id is already exists
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        zone_id = request.form['id']
        cursor.execute('''SELECT id FROM zone WHERE id=?''', (zone_id,))
        existing_id = cursor.fetchone()
        conn.close()
        if existing_id:
            flash('Zone Create Failed. ID already exists.', 'error')
            return render_template('manager/manage_zone/zone_create.html')
        else:
            conn = sqlite3.connect('data/data.db')
            cursor = conn.cursor()
            zone_id = request.form['id']
            zone_city = request.form['city']
            zone_name = request.form['name']
            cursor.execute('''INSERT INTO zone VALUES (?, ?, ?)''',
                (zone_id, zone_city, zone_name)
            )
            conn.commit()
            conn.close()
            return redirect('/manager/managezone')
    else:
        return render_template('manager/auth/login_form.html')

# manager manage subscription
@main_bp.route('/manager/managesubscription')
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

@main_bp.route('/manager/managesubscription/delete/<string:user_id>', methods=['GET'])
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

# manager manage car
@main_bp.route('/manager/managecar')
def root_manager_managecar():
    if session.get('manager_session'):
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT car.number, car.model_id, model.manufacturer, model.name, car.zone_id, zone.city, zone.name
            FROM car
            JOIN model ON car.model_id = model.id
            JOIN zone ON car.zone_id = zone.id
        ''')
        car_data = cursor.fetchall()
        conn.close()
        return render_template('manager/manage_car/managecar.html',
                                car_data=car_data)
    else:
        return render_template('manager/auth/login_form.html')

# 예약되었는지 확인해보는 함수
def isReservedCar(number):
    conn = sqlite3.connect('data/data.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT car_number FROM reservation
                      WHERE car_number=?''', (number,))
    reserved_car_number = cursor.fetchone()
    conn.close()
    if reserved_car_number:
        return True
    else:
        return False

@main_bp.route('/manager/managecar/move/<string:number>', methods=['GET'])
def root_manager_managecar_move(number):
    if session.get('manager_session'):
        # 예약되었으면 이동 불가
        if isReservedCar(number):
            flash(f'You Cannot move {number}. This car is reserved', 'error')
            return render_template('manager/manage_car/managecar.html')
        else:
            conn = sqlite3.connect('data/data.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM car WHERE number=?''', (number,))
            selected_car_data = cursor.fetchone()
            cursor.execute('''SELECT * FROM zone''')
            zone_data = cursor.fetchall()
            conn.close()
            return render_template('manager/manage_car/car_move.html',
                        selected_car_data=selected_car_data, zone_data=zone_data)
    else:
        return render_template('manager/auth/login_form.html')

@main_bp.route('/manager/managecar/move/process/<string:number>', methods=['POST'])
def root_manager_managecar_move_process(number):
    if session.get('manager_session') and request.method == 'POST':
        zone_id = request.form['zone_id']
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        cursor.execute('''UPDATE car 
                            SET zone_id=?
                            WHERE number=?''',
                        (zone_id, number))
        conn.commit()
        conn.close()
        return redirect('/manager/managecar')
    else:
        return render_template('manager/auth/login_form.html')
    
@main_bp.route('/manager/managecar/delete/<string:number>', methods=['GET'])
def root_manager_managecar_delete(number):
    print('[INFO] root_manager_managecar_delete')
    if session.get('manager_session'):
        # 예약되었으면 삭제 불가
        if isReservedCar(number):
            flash(f'You Cannot move {number}. This car is reserved', 'error')
            return render_template('manager/manage_car/managecar.html')
        else:
            print('[INFO] root_manager_managecar_delete - not reserved')
            conn = sqlite3.connect('data/data.db')
            cursor = conn.cursor()
            cursor.execute('''DELETE FROM car WHERE number=?''', (number,))
            conn.commit()
            print('[INFO] root_manager_managecar_delete - deleted')
            conn.close()
            return redirect('/manager/managecar')
    else:   
        return render_template('manager/auth/login_form.html')

@main_bp.route('/manager/managecar/register')
def root_manager_managecar_register():
    if session.get('manager_session'):
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM zone''')
        zone_data = cursor.fetchall()
        cursor.execute('''SELECT * FROM model''')
        model_data = cursor.fetchall()
        conn.close()
        return render_template('manager/manage_car/car_register.html',
                zone_data=zone_data, model_data=model_data)
    else:
        return render_template('manager/auth/login_form.html')

@main_bp.route('/manager/managecar/register/process', methods=['POST'])
def root_manager_managecar_register_process():
    if session.get('manager_session') and request.method == 'POST':
        # 넘버가 이미 존재하는지 체크
        first_number = request.form['first_number']
        middle_number = request.form['middle_number']
        last_number = request.form  ['last_number']
        number = first_number + middle_number + last_number
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT number FROM car WHERE number=?''', (number,))
        existing_number = cursor.fetchone()
        conn.close()
        if existing_number:
            flash('Car Register Failed. Number already exists.', 'error')
            return redirect('/manager/managecar/register')
            # return render_template('manager/manage_car/car_register.html')
        else:
            conn = sqlite3.connect('data/data.db')
            cursor = conn.cursor()
            model_id = request.form['model_id']
            zone_id = request.form['zone_id']
            cursor.execute('''INSERT INTO car VALUES (?, ?, ?)''',
                (number, model_id, zone_id)
            )
            conn.commit()
            conn.close()
            return redirect('/manager/managecar')
    else:
        return render_template('manager/auth/login_form.html')