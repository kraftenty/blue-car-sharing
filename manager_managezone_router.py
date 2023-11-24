from flask import Blueprint, render_template, session, request, redirect, flash
import sqlite3

manager_managezone_bp = Blueprint('manager_managezone', __name__)

# manager manage zone
@manager_managezone_bp.route('/manager/managezone')
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

@manager_managezone_bp.route('/manager/managezone/update/<int:zone_id>', methods=['GET'])
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

@manager_managezone_bp.route('/manager/managezone/update/process/<int:zone_id>', methods=['POST'])
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
    
@manager_managezone_bp.route('/manager/managezone/delete/<int:zone_id>', methods=['GET'])
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

@manager_managezone_bp.route('/manager/managezone/create')
def root_manager_managezone_create():
    if session.get('manager_session'):
        return render_template('manager/manage_zone/zone_create.html')
    else:
        return render_template('manager/auth/login_form.html')

@manager_managezone_bp.route('/manager/managezone/create/process', methods=['POST'])
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