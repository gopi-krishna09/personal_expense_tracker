import mysql.connector

class Database:
    def __init__(self, host="localhost", user="root", password="gopi", database="expense_tracker_db"):
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.connection.cursor()
            self.create_table()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            raise

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date DATE NOT NULL,
            category VARCHAR(100) NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            description TEXT
        )''')
        self.connection.commit()

    def insert(self, date, category, amount, description):
        self.cursor.execute("INSERT INTO expenses (date, category, amount, description) VALUES (%s, %s, %s, %s)",
                            (date, category, amount, description))
        self.connection.commit()

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM expenses")
        return self.cursor.fetchall()

    def fetch_by_date(self, date):
        self.cursor.execute("SELECT * FROM expenses WHERE date=%s", (date,))
        return self.cursor.fetchall()

    def update(self, expense_id, date, category, amount, description):
        self.cursor.execute("UPDATE expenses SET date=%s, category=%s, amount=%s, description=%s WHERE id=%s",
                            (date, category, amount, description, expense_id))
        self.connection.commit()

    def delete(self, expense_id):
        self.cursor.execute("DELETE FROM expenses WHERE id=%s", (expense_id,))
        self.connection.commit()

    def __del__(self):
        self.connection.close()
