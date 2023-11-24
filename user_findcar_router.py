from flask import Blueprint, render_template, session, request, redirect, url_for, flash
import sqlite3

user_findcar_bp = Blueprint('user_findcar_bp', __name__)

# findcar
@user_findcar_bp.route('/user/findcar')
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

@user_findcar_bp.route('/user/findcar/select', methods=['GET'])
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

@user_findcar_bp.route('/user/findcar/select/proceed', methods=['POST'])
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

@user_findcar_bp.route('/user/findcar/select/proceed/process', methods=['POST'])
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

