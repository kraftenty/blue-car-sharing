from flask import Blueprint, render_template, session, request, redirect, flash
import sqlite3

manager_managecar_bp = Blueprint('manager_managecar_bp', __name__)

# manager manage car
@manager_managecar_bp.route('/manager/managecar')
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

@manager_managecar_bp.route('/manager/managecar/move/<string:number>', methods=['GET'])
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

@manager_managecar_bp.route('/manager/managecar/move/process/<string:number>', methods=['POST'])
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
    
@manager_managecar_bp.route('/manager/managecar/delete/<string:number>', methods=['GET'])
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

@manager_managecar_bp.route('/manager/managecar/register')
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

@manager_managecar_bp.route('/manager/managecar/register/process', methods=['POST'])
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
