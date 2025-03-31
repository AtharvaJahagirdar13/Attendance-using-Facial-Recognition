import mysql.connector as MySQLdb
class StudentDBManager:
    def __init__(self, host="localhost", user="root", passwd="AnkitaGadre18", db="attendance_db"):
        self.conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS student_details (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE,
            age VARCHAR(20),
            gender VARCHAR(20)
        )
        """
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def insert_or_update_student(self, name, age, gender):
        # Check if a record for this student already exists
        select_query = "SELECT id FROM student_details WHERE name=%s"
        self.cursor.execute(select_query, (name,))
        result = self.cursor.fetchone()
        if result:
            # Update existing record
            update_query = "UPDATE student_details SET age=%s, gender=%s WHERE name=%s"
            self.cursor.execute(update_query, (age, gender, name))
        else:
            # Insert new record
            insert_query = "INSERT INTO student_details (name, age, gender) VALUES (%s, %s, %s)"
            self.cursor.execute(insert_query, (name, age, gender))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
