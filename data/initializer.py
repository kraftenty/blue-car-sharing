import sqlite3
import os
import data.dataInserter as dataInserter

db_filename = 'data/data.db'

def initialize():
    if os.path.exists(db_filename):
        print('[INFO] Database already exists. Nothing to initialize.')
        return
    
    print('[INFO] Initializing database...')
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    # Create user table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id VARCHAR PRIMARY KEY NOT NULL,
            name VARCHAR NOT NULL,
            passwd VARCHAR NOT NULL,
            phone VARCHAR NOT NULL,
            birthday DATE NOT NULL
        );
    ''')
    # Create license table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS license (
            user_id VARCHAR PRIMARY KEY NOT NULL,
            license_num VARCHAR NOT NULL,
            expiration_date DATE NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user(id)
        );
    ''')
    # Create payment table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payment (
            user_id VARCHAR PRIMARY KEY NOT NULL,
            card_num VARCHAR NOT NULL,
            card_valid_thru VARCHAR NOT NULL,
            card_cvc VARCHAR NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user(id)
        );
    ''')
    # Create car table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS car (
            number VARCHAR PRIMARY KEY NOT NULL,
            model_id INTEGER NOT NULL,
            zone_id INTEGER NOT NULL,
            FOREIGN KEY (model_id) REFERENCES model(id),
            FOREIGN KEY (zone_id) REFERENCES zone(id)
        );
    ''')
    # Create model table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS model (
            id INTEGER PRIMARY KEY NOT NULL,
            manufacturer VARCHAR NOT NULL,
            name VARCHAR NOT NULL,
            type VARCHAR NOT NULL,
            capacity INTEGER NOT NULL,
            drive_range INTEGER NOT NULL,
            price_per_day INTEGER NOT NULL
        );
    ''')
    # Create zone table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS zone (
            id INTEGER PRIMARY KEY NOT NULL,
            city VARCHAR NOT NULL,
            name VARCHAR NOT NULL
        );
    ''')
    # Create repairment table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS repairment (
            number VARCHAR PRIMARY KEY NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            FOREIGN KEY (number) REFERENCES car(number)
        );
    ''')
    # Create subscribe table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscribe (
            user_id VARCHAR PRIMARY KEY NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user(id)
        );
    ''')
    # Create reservation table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_number VARCHAR NOT NULL,
            user_id VARCHAR NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            tot_price INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user(id),
            FOREIGN KEY (car_number) REFERENCES car(number)
        );
    ''')
    conn.close()
    print('[INFO] Database initialized.')

    print('[INFO] Inserting data...')
    dataInserter.insertData()
    print('[INFO] Data inserted.')
