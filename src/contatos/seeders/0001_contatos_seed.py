import pymysql.cursors
from contextlib import contextmanager
from datetime import datetime
from faker import Faker
from random import randint

fake = Faker("pt_BR")


@contextmanager
def conecta():
    conection = pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        port=3002,
        db='agenda',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        yield conection
    finally:
        print('Fechando conexão')
        conection.close()


def populate_db():
    sql = """
        INSERT INTO contatos_contact (name, last_name, phone, email,
        created_at, description, category_id, `show`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """

    for i in range(200):
        with conecta() as con:
            with con.cursor() as cursor:
                cursor.execute(sql, (
                    fake.name(),
                    fake.last_name(),
                    fake.phone_number(),
                    fake.email(),
                    f'{datetime.now()}',
                    fake.text(),
                    randint(1, 5),
                    1
                ))
                con.commit()


if __name__ == '__main__':
    populate_db()
