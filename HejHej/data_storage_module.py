import sqlite3

class DataStorage:
    def __init__(self):
        self.conn = sqlite3.connect('dodgeball.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS measurements
                            (timestamp DATETIME, velocity1 FLOAT, velocity2 FLOAT,
                            accuracy1 FLOAT, accuracy2 FLOAT)''')

    def save_measurement(self, timestamp, velocity1, velocity2, accuracy1, accuracy2):
        self.cursor.execute('''INSERT INTO measurements VALUES (?,?,?,?,?)''',
                            (timestamp, velocity1, velocity2, accuracy1, accuracy2))
        self.conn.commit()

    def retrieve_measurements(self):
        self.cursor.execute('''SELECT * FROM measurements''')
        return self.cursor.fetchall()
