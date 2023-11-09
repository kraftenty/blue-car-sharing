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

@main_bp.route('/user/smartkey/cancelreservation')
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

# findcar
@main_bp.route('/user/findcar')
def root_user_findcar():
    if session.get('user_session'):
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT start_date
                          FROM reservation 
                          WHERE user_id=?''', (session['user_session'][0],)
        )
        existing_reservation_start_date = cursor.fetchall()

        
        if existing_reservation_start_date:
            conn.close()
            return render_template('user/findcar/findcar_alreadyreserved.html',
                    existing_reservation_start_date=existing_reservation_start_date)
        else:
            cursor.execute('''SELECT * FROM zone''')
            zone_data = cursor.fetchall()
            unique_cities = set(zone[1] for zone in zone_data)
            unique_cities = list(unique_cities)
            unique_cities.sort()
            conn.close()
            return render_template('user/findcar/findcar.html', 
                    zone_data=zone_data, unique_cities=unique_cities)
    else:
        return render_template('user/auth/login_form.html')

@main_bp.route('/user/findcar/select', methods=['GET'])
def root_user_findcar_select():
    if session.get('user_session'):
        zone_id = request.args.get('zone_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT car.number, model.manufacturer, model.name, model.type,
                   model.capacity, model.drive_range, model.price_per_day, car.zone_id
            FROM car
            LEFT JOIN reservation ON car.number = reservation.car_number
            LEFT JOIN repairment ON car.number = repairment.number
            LEFT JOIN model ON car.model_id = model.id
            WHERE car.zone_id=?
                AND repairment.number IS NULL
                AND (reservation.car_number IS NULL OR (reservation.start_date > ? OR reservation.end_date < ?))
        ''', (zone_id, end_date, start_date))
        available_car_data = cursor.fetchall()
        conn.close()
        reservation_date_data = (start_date, end_date)
        return render_template('user/findcar/findcar_select.html',
                available_car_data=available_car_data, reservation_date_data=reservation_date_data)
    else:
        return render_template('user/auth/login_form.html')

@main_bp.route('/user/findcar/select/proceed', methods=['POST'])
def root_user_findcar_select_number():
    if session.get('user_session'):
        number = request.form['number']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        zone_id = request.form['zone_id']
        reservation_date_data = (start_date, end_date)
        conn = sqlite3.connect('data/data.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT car.number, model.manufacturer, model.name, model.type,
                          model.capacity, model.drive_range, model.price_per_day, model.id
                          FROM car
                          LEFT JOIN model ON car.model_id = model.id
                          WHERE car.number=?
                       ''', (number,))
        selected_car_data = cursor.fetchone()
        cursor.execute('''SELECT city, name FROM zone WHERE id=?''', (zone_id,))
        selected_zone_data = cursor.fetchone()
        cursor.execute('''SELECT * FROM subscribe WHERE user_id=?''', (session['user_session'][0],))
        subscribe_data = cursor.fetchone()
        if subscribe_data is None:
            subscribe_data = (1, 'You are Not a subscriber')
        else:
            subscribe_data = (2, 'You are Subscriber! Enjoy 50 percent discount')
        conn.close()
        return render_template('user/findcar/findcar_select_number.html',
                selected_car_data=selected_car_data,
                selected_zone_data=selected_zone_data,
                reservation_date_data=reservation_date_data,
                subscribe_data=subscribe_data)
    else:
        return render_template('user/auth/login_form.html')

@main_bp.route('/user/findcar/select/proceed/process', methods=['POST'])
def root_user_findcar_select_proceed_process():
    if session.get('user_session'):
        if request.method == 'POST':
            car_number = request.form['car_number']
            user_id = session['user_session'][0]
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            tot_price = request.form['tot_price']
            conn = sqlite3.connect('data/data.db')
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO reservation (car_number, user_id, start_date, end_date, tot_price)
                              VALUES (?, ?, ?, ?, ?)''',
                           (car_number, user_id, start_date, end_date, tot_price))
            conn.commit()
            conn.close()
            return redirect('/user')
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

# manager manage repairment
@main_bp.route('/manager/managerepairment')
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

@main_bp.route('/manager/managerepairment/delete/<string:number>', methods=['GET'])
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

@main_bp.route('/manager/managerepairment/add')
def root_manager_managerepairment_add():
    if session.get('manager_session'):
        return render_template('manager/manage_repairment/repairment_add.html')
    else:
        return render_template('manager/auth/login_form.html')

@main_bp.route('/manager/managerepairment/add/process', methods=['POST'])
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

# manager manage reservation
@main_bp.route('/manager/managereservation')
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

@main_bp.route('/manager/managereservation/delete/<int:id>', methods=['GET'])
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

@main_bp.route('/manager/viewincome')
def root_manager_viewincome():
    if session.get('manager_session'):
        return render_template('manager/view_income/viewincome.html')
    else:
        return render_template('manager/auth/login_form.html')

@main_bp.route('/manager/viewincome/calculated', methods=['POST'])
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