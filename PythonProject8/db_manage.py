import MySQLdb

class DBManager:
    def __init__(self, host="localhost", user="root", passwd="your_password", db="attendance_db"):
        self.conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS attendance (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            attendance_date DATE NOT NULL,
            attendance_time TIME NOT NULL
        )
        """
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def insert_attendance(self, name, date_str, time_str):
        insert_query = "INSERT INTO attendance (name, attendance_date, attendance_time) VALUES (%s, %s, %s)"
        self.cursor.execute(insert_query, (name, date_str, time_str))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
