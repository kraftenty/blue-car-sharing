from flask import Blueprint, render_template, session, request, redirect, flash
import sqlite3

manager_managemodel_bp = Blueprint('manager_managemodel_bp', __name__)


# manager manage model
@manager_managemodel_bp.route('/manager/managemodel')
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

@manager_managemodel_bp.route('/manager/managemodel/update/<int:model_id>', methods=['GET'])
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

@manager_managemodel_bp.route('/manager/managemodel/update/process/<int:model_id>', methods=['POST'])
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

@manager_managemodel_bp.route('/manager/managemodel/delete/<string:user_id>', methods=['GET'])
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

@manager_managemodel_bp.route('/manager/managemodel/create')
def root_manager_managemodel_create():
    if session.get('manager_session'):
        return render_template('manager/manage_model/model_create.html')
    else:
        return render_template('manager/auth/login_form.html')

@manager_managemodel_bp.route('/manager/managemodel/create/process', methods=['POST'])
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