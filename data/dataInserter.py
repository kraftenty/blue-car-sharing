import sqlite3

def insertData():
    conn = sqlite3.connect('data/data.db')
    cursor = conn.cursor()

    # id INTEGER, manufacturer VARCHAR, name VARCHAR, type VARCHAR, capacity INTEGER, drive_range INTEGER, price_per_day INTEGER
    model_data = [
        (100, 'Hyundai', 'Kona Electric', 'SUV', 5, 417, 45000),
        (101, 'Hyundai', 'IONIQ 5', 'SUV', 5, 458, 52000),
        (102, 'Hyundai', 'IONIQ 6', 'Sedan', 5, 524, 65000),
        (103, 'Hyundai', 'IONIQ 5 N', 'SUV', 5, 351, 95000),
        (104, 'Hyundai', 'Genesis Electrified G80', 'Sedan', 5, 427, 110000),
        (200, 'Kia', 'Ray EV', 'Other', 4, 205, 35000),
        (201, 'Kia', 'Niro EV', 'SUV', 5, 401, 55000),
        (202, 'Kia', 'Niro Plus', 'SUV', 5, 392, 57000),
        (203, 'Kia', 'EV6', 'SUV', 5, 342, 72000),
        (204, 'Kia', 'EV6 GT', 'SUV', 5, 342, 85000),
        (205, 'Kia', 'EV9', 'SUV', 7, 501, 105000),
        (300, 'Chevrolet', 'Bolt EV', 'Other', 5, 414, 48000),
        (301, 'Chevrolet', 'Bolt EUV', 'SUV', 5, 403, 50000),
        (400, 'Polestar', 'Polestar 2', 'Sedan', 5, 417, 86000),
        (500, 'Tesla', 'Model S', 'Sedan', 5, 555, 135000),
        (501, 'Tesla', 'Model 3', 'Sedan', 5, 480, 75000),
        (502, 'Tesla', 'Model X', 'SUV', 5, 478, 145000),
        (503, 'Tesla', 'Model Y', 'SUV', 5, 350, 85000)
    ]
    for model in model_data:
        cursor.execute('''
            INSERT INTO model (id, manufacturer, name, type, capacity, drive_range, price_per_day)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', model)
    conn.commit()

    # id INTEGER, city VARCHAR, name VARCHAR
    zone_data = [
        (1000, 'Seoul', 'Gongneung Station exit no.1'),
        (1001, 'Seoul', 'Sangbong Station exit no.3'),
        (2000, 'Incheon', 'Incheon Int\'l Airport Terminal 1'),
        (3000, 'Gyeonggi', 'Bundang-gu Office'),
        (4000, 'Gangwon', 'Wonju Bus Terminal'),
        (5000, 'ChungBuk','Cheongju-si Office'),
        (6000, 'ChungNam', 'Cheonan Station exit no.1'),
        (7000, 'Sejong', 'Sejong Government Complex'),
        (8000, 'Daejeon', 'Tahnbang Station exit no.5'),
        (8001, 'Daejeon', 'Daejeon Station Parking Lot'),
        (9000, 'GyeongBuk', 'Pohang Bus Terminal'),
        (10000, 'GyeongNam', 'Gimhae-si Office'),
        (11000, 'Daegu','Dong-Daegu Bus Terminal'),
        (12000, 'Ulsan', 'Taehwa Station Parking Lot'),
        (13000, 'Busan', 'Bexco Parking Lot'),
        (13001, 'Busan', 'Suyeong-gu Office'),
        (14000, 'JeonBuk', 'Lotte Department Store Jeonju'),
        (15000, 'JeonNam', 'Yeosu Expo Parking Lot'),
        (16000, 'Gwangju', 'U-Square'),
        (16001, 'Gwangju', 'Chosun University Parking Lot.5')
    ]
    for zone in zone_data:
        cursor.execute('''
            INSERT INTO zone (id, city, name)
            VALUES (?, ?, ?)
        ''', zone)
    conn.commit()

    # number INTEGER, model_id INTEGER, zone_id INTEGER
    car_data = [
        ('132HA0718', 104, 1000),
        ('145HEO2693', 501, 1000),
        ('124HO7437', 502, 1000),
        ('124HA3871', 202, 1000),
        ('135HEO7452', 300, 1000),
        ('142HA6153', 400, 1001),
        ('140HEO5120', 100, 1001),
        ('127HA9387', 204, 1001),
        ('121HEO8440', 501, 1001),
        ('148HO3019', 500, 1001),
        ('132HA6546', 203, 2000),
        ('138HEO4138', 201, 2000),
        ('130HO4123', 101, 2000),
        ('138HA4197', 503, 2000),
        ('133HO2396', 503, 2000),
        ('124HA1276', 102, 3000),
        ('125HO9079', 102, 3000),
        ('148HA2743', 502, 3000),
        ('124HEO7093', 202, 3000),
        ('145HO7207', 204, 3000),
        ('123HA6046', 100, 4000),
        ('127HEO8361', 501, 4000),
        ('139HA1501', 103, 4000),
        ('128HEO1917', 500, 4000),
        ('141HO8443', 502, 4000),
        ('133HEO2809', 500, 5000),
        ('144HO2576', 100, 5000),
        ('136HA3803', 204, 5000),
        ('126HA3902', 501, 5000),
        ('132HO4516', 102, 5000),
        ('140HA7259', 1000, 6000),
        ('141HO8234', 300, 6000),
        ('124HA9001', 101, 6000),
        ('138HO5551', 503, 6000),
        ('133HO6514', 203, 6000),
        ('127HO9942', 104, 7000),
        ('125HA3282', 204, 7000),
        ('146HA4127', 104, 7000),
        ('147HO6424', 500, 7000),
        ('137HO5485', 500, 7000),
        ('134HO2143', 203, 8000),
        ('125HEO6091', 501, 8000),
        ('122HA4648', 102, 8000),
        ('127HEO7741', 200, 8000),
        ('134HA2831', 502, 8000),
        ('135HA2149', 500, 8001),
        ('126HO6412', 502, 8001),
        ('137HA1523', 202, 8001),
        ('140HO8023', 100, 8001),
        ('143HO1318', 201, 8001),
        ('137HA7853', 102, 9000),
        ('142HA5292', 202, 9000),
        ('147HEO3115', 204, 9000),
        ('131HA3845', 103, 9000),
        ('145HA4907', 101, 9000),
        ('130HO2357', 202, 10000),
        ('143HEO3403', 300, 10000),
        ('130HEO8283', 104, 10000),
        ('141HO7319', 101, 10000),
        ('133HEO6947', 500, 10000),
        ('138HO7849', 1001, 11000),
        ('146HO4987', 204, 11000),
        ('140HO3025', 502, 11000),
        ('139HA2716', 500, 11000),
        ('134HEO6507', 101, 11000),
        ('132HEO4372', 203, 12000),
        ('125HO3422', 201, 12000),
        ('124HA9240', 300, 12000),
        ('128HO4594', 502, 12000),
        ('131HO3729', 100, 12000),
        ('126HEO9380', 100, 13000),
        ('137HO6201', 501, 13000),
        ('122HEO8425', 501, 13000),
        ('123HA4193', 104, 13000),
        ('127HA8317', 102, 13000),
        ('133HA2842', 500, 13001),
        ('143HEO4300', 101, 13001),
        ('149HO3024', 202, 14000),
        ('143HO1961', 100, 14000),
        ('125HO5130', 104, 14000),
        ('125HEO2355', 501, 14000),
        ('132HEO9630', 502, 14000),
        ('140HEO8213', 500, 15000),
        ('129HO6717', 100, 15000),
        ('126HO9362', 502, 15000),
        ('128HA6936', 102, 15000),
        ('123HEO7649', 501, 15000),
        ('142HO3046', 500, 16000),
        ('129HEO6537', 103, 16000),
        ('131HA3195', 100, 16000),
        ('136HO4486', 202, 16000),
        ('145HO6243', 201, 16000),
        ('139HA2845', 500, 16001),
        ('144HEO4309', 101, 16001),
        ('144HO3087', 202, 16001),
        ('135HO5127', 104, 16001),
        ('141HEO2385', 501, 16001)
    ]
    for car in car_data:
        cursor.execute('''
            INSERT INTO car (number, model_id, zone_id)
            VALUES (?, ?, ?)
        ''', car)
    conn.commit()

    conn.close()
    return