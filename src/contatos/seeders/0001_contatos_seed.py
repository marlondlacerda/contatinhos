import pymysql.cursors
from contextlib import contextmanager
from datetime import datetime
from faker import Faker
from random import randint
from dotenv import dotenv_values
from pathlib import Path
import urllib.request
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
fake = Faker("pt_BR")
dotenv = dotenv_values(str(BASE_DIR / ".env"))


@contextmanager
def conecta():
    conection = pymysql.connect(
        host=dotenv["DB_HOST"],
        user=dotenv["DB_USER"],
        password=dotenv["DB_PASS"],
        port=int(dotenv["DB_PORT"]),
        db=dotenv["DB_NAME"],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        yield conection
    finally:
        print('Dados inseridos com sucesso!')
        print('Fechando conexão...')
        conection.close()


def populate_category():
    categorys = [
                    "Amigos",
                    "Trabalho",
                    "Familia",
                    "Outros",
                    "Conhecidos",
                    "Amigos da internet",
                    "Faculdade"
                ]
    sql = "INSERT INTO contatos_categoy (name, created_at) VALUES (%s, %s)"

    with conecta() as con:
        with con.cursor() as cursor:
            for category in categorys:
                cursor.execute(sql, (category, f'{datetime.now()}'))
                con.commit()


def populate_contacts():
    sql = """
        INSERT INTO contatos_contact (name, last_name, image, phone, email,
        created_at, description, category_id, `show`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    for i in range(100):
        fake_name = fake.name()
        imgURL = fake.image_url(width=250, height=250)
        ano_atual = datetime.now().year
        mes_atual = datetime.now().month
        path = f"{BASE_DIR}/src/media/pictures/{ano_atual}/{mes_atual}"
        path_img = f"{path}/{fake_name}.jpg"

        if not os.path.exists(path):
            os.makedirs(path)

        while True:
            try:
                urllib.request.urlretrieve(
                    imgURL,
                    path_img,
                )
                break
            except Exception as e:
                print(e)
                imgURL = fake.image_url(width=250, height=250)

        with conecta() as con:
            with con.cursor() as cursor:
                cursor.execute(sql, (
                    fake_name,
                    fake.last_name(),
                    f"/pictures/{ano_atual}/{mes_atual}/{fake_name}.jpg",
                    fake.phone_number(),
                    fake.email(),
                    f'{datetime.now()}',
                    fake.text(),
                    randint(1, 7),
                    1
                ))
                con.commit()


if __name__ == '__main__':
    populate_category()
    print('Categoria populada')
    populate_contacts()
    print('Contatos inseridos com sucesso')
