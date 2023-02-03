import psycopg2

class DataBase():
    def __init__(self, conn):
        self.conn = conn

    def create_db(self):
        with self.conn.cursor() as cur:
            cur.execute('''
            DROP TABLE tell;
            DROP TABLE client;
            ''')

            cur.execute("""
            CREATE TABLE IF NOT EXISTS client(
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(40) NOT NULL,
                last_name VARCHAR(40) NOT NULL,
                email VARCHAR(40) NOT NULL UNIQUE,
                phones_number INTEGER
            );
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS tell(
                id SERIAL PRIMARY KEY,
                number INTEGER NOT NULL UNIQUE,
                client_id INTEGER NOT NULL REFERENCES client(id) ON DELETE CASCADE
            );
            """)
        print('Таблицы созданы')

    def add_client(self, first_name, last_name, email, phones=None):
        with self.conn.cursor() as cur:
            if self.find_client(email=email):
                print('такой клмент уже существует')
            cur.execute('''
            INSERT INTO client(first_name, last_name, email) VALUES(%s, %s, %s) RETURNING id;
            ''', (first_name, last_name, email))
            if phones is not None:
                client = cur.fetchall()[0]
                self.add_phone(phones, client)
        print('клиент добавлен')

    def add_phone(self, phone, client_id,):
        with self.conn.cursor() as cur:
            cur.execute('''
            INSERT INTO tell(number, client_id) VALUES(%s, %s);
            ''', (phone, client_id))
        print('телефон добавлен')

    def change_client(self, client_id, first_name=None, last_name=None, email=None):
        with self.conn.cursor() as cur:
            if first_name is not None:
                cur.execute('''
                UPDATE client SET first_name = %s
                WHERE id = %s;
                ''', (first_name, client_id))
                print('Успешно изменено')
            elif last_name is not None:
                cur.execute('''
                UPDATE client SET last_name = %s
                WHERE id = %s;
                ''', (last_name, client_id))
                print('Успешно изменено')
            elif email is not None:
                cur.execute('''
                UPDATE client SET email = %s
                WHERE id = %s;
                ''', (email, client_id))
                print('Успешно изменено')
            else:
                print('ошибка')

    def delete_phone(self, client_id, phone):
        with self.conn.cursor() as cur:
            cur.execute('''
            DELETE FROM tell 
            WHERE client_id=%s and number=%s
            RETURNING *;
            ''', (client_id, phone))
            if not cur.fetchall():
                return f'номера {phone} нет'
        print(f'телефон {phone} успешно удален')

    def delete_client(self, client_id):
        with self.conn.cursor() as cur:
            cur.execute('''
            DELETE FROM client 
            WHERE id=%s;
            ''', (client_id,))
        print('Пользователь удален')

    def find_client(self, id=None, first_name=None, last_name=None, email=None):
        with self.conn.cursor() as cur:
            cur.execute('''
            SELECT id, first_name, last_name, email FROM client 
            WHERE id=%s or first_name=%s or last_name=%s or email=%s
            ''', (id, first_name, last_name, email))
            return f'{cur.fetchall()}'


with psycopg2.connect(database="dvdrental", user="postgres", password="1207") as conn:
    data = DataBase(conn)
    data.create_db()
    data.add_client("sasha", "lebedev", 'email')
    data.add_client("gerald", "witcher", 'emaill', 5)
    data.add_phone(1111, 1)
    data.add_phone(1121, 1)
    data.add_phone(1131, 2)
    data.add_phone(1541, 2)
    data.change_client(2, 'Лютик')
    data.change_client(2, last_name='Бард')
    data.change_client(2, email='лютиклучший')
    data.change_client(1, email='sasha')
    data.delete_phone(2, 1131)
    data.delete_client(2)
    print(data.find_client(1))
conn.close()