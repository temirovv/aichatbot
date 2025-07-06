import sqlite3


class User:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data



    

    def create_table_users(self):
        '''
            foydalanuvchilar uchun jadvalni hosil qilish metodi
        '''
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            telegram_id INTEGER NOT NULL,
            full_name VARCHAR(300),
            username VARCHAR(500),
            is_active BOOL DEFAULT 1,
            joined_at VARCHAR(255),
            language VARCHAR(2),
            PRIMARY KEY (telegram_id)
            );
        """
        self.execute(sql, commit=True)


    def create_user_history_table(self):
        '''
            foydalanuvchilarning tarixini saqlash uchun jadval
        '''
        sql = """CREATE TABLE IF NOT EXISTS UserHistory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            prompt TEXT,
            content TEXT,
            saved_at VARCHAR(255),
            FOREIGN KEY (user_id) REFERENCES Users(telegram_id)
        )"""
        self.execute(sql, commit=True)


    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, telegram_id: int, full_name :str, username: str, joined_at: int):
        sql = """
        INSERT OR IGNORE INTO Users(telegram_id, full_name, username, joined_at) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(telegram_id, full_name, username, joined_at), commit=True)


    def save_user_history(self, user_id: int, prompt: int, content: str, saved_at: int):
        sql = """
        INSERT INTO UserHistory(user_id, prompt, content, saved_at) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(user_id, prompt, content, saved_at), commit=True)

    def update_user_language(self, user_id: int, language: str):
        sql = """UPDATE Users SET language=? WHERE telegram_id=?"""
        self.execute(sql, parameters=(language, user_id), commit=True)

    def get_user_language(self, user_id: int):
        sql = """SELECT language FROM Users WHERE telegram_id=?"""
        return self.execute(sql, parameters=(user_id, ), fetchone=True)

    def get_user_history(self, **kwargs):
        sql = "SELECT * FROM UserHistory WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)


    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def get_users(self):
        sql = """SELECT telegram_id, full_name FROM Users"""
        return self.execute(sql, fetchall=True)
        

    def get_user_prompts(self, telegram_id: int):
        sql = """SELECT id, user_id, prompt FROM UserHistory WHERE user_id=?"""
        return self.execute(sql, parameters=(telegram_id, ), fetchall=True)

    def get_content_by_prompt(self, history_id):
        sql = """SELECT content FROM UserHistory WHERE id = ?"""
        return self.execute(sql, parameters=(history_id, ), fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)



def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")