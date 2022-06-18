import pymysql.cursors
from contextlib import contextmanager
from datetime import datetime
from faker import Faker
from random import randint
from dotenv import dotenv_values
from pathlib import Path
import urllib.request
import os


class FakeData:
    def __init__(self):
        self.fake = Faker("pt_BR")
        self._fake_name = self.fake.name()
        self._fake_last_name = self.fake.last_name()
        self._fake_phone = self.fake.phone_number()
        self._fake_email = self.fake.email()
        self._fake_date = datetime.now().strftime("%Y/%m")
        self._imgURL = self.fake.image_url(width=300, height=300)
        self._fake_img = f"/pictures/{self._fake_date}/{self._fake_name}.jpg"
        self._fake_description = self.fake.text(max_nb_chars=200)
        self._fake_category = randint(1, 8)
        self._show = 1


class Connection:
    def __init__(self):
        self._BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        self.__dotenv_path = dotenv_values(str(self._BASE_DIR / ".env"))
        self._connection = self._get_connection()

    @contextmanager
    def _get_connection(self):
        connection = pymysql.connect(
            host=self.__dotenv_path["DB_HOST"],
            port=int(self.__dotenv_path["DB_PORT"]),
            user=self.__dotenv_path["DB_USER"],
            password=self.__dotenv_path["DB_PASS"],
            db=self.__dotenv_path["DB_NAME"],
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )

        try:
            yield connection
        except Exception as e:
            print(e)
        finally:
            print(
                "\nThe request on Database has been completed \n"
                "Closing Connection... \n"
            )
            connection.close()


class Seeder(Connection):
    def run(self, count, create_category=False):
        if not self._check_superuser():
            return print(
                "Error: \n"
                "You need to create a superuser before run this script. \n"
                "Please, run the following command: \n"
                "       'make superuser' \n"
            )
        else:
            print("Superuser found! \n" "Starting seeding... \n")

        if create_category:
            self._populate_category()

        self._populate_contacts(count)
        self._populate_contacts_user(count)

    def _check_superuser(self):
        sql = "SELECT * FROM auth_user WHERE id = 1"
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                user = cursor.fetchone()
                if user is None:
                    return False
                else:
                    return True

    def _populate_category(self):
        sql = "INSERT INTO contatos_categoy (name, created_at) VALUES (%s, %s)"
        categories = [
            "Amigos",
            "Trabalho",
            "Colegas",
            "Família",
            "Conhecidos",
            "Amigos da Internet",
            "Outros",
            "Faculdade",
        ]

        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                for category in categories:
                    cursor.execute(sql, (category, datetime.now()))
                    connection.commit()
                    print(f"Category: {category} created successfully!")

    @staticmethod
    def _check_path(path):
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def _download_img(imgURL, path_img):
        fake = Faker("pt_BR")

        while True:
            try:
                urllib.request.urlretrieve(
                    imgURL,
                    path_img,
                )
                break
            except Exception:
                print("Error: Unable to download Image, trying again!")
                imgURL = fake.image_url(width=250, height=250)

    def _populate_contacts(self, count):
        sql = """
            INSERT INTO contatos_contact (name, last_name, image, phone, email,
            created_at, description, category_id, `show`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                for i in range(count):
                    contact = FakeData()
                    fake_date = contact._fake_date
                    path = f"{self._BASE_DIR}/src/media/pictures/{fake_date}"
                    path_img = f"{path}/{contact._fake_name}.jpg"

                    self._check_path(path)
                    self._download_img(contact._imgURL, path_img)
                    cursor.execute(
                        sql,
                        (
                            contact._fake_name,
                            contact._fake_last_name,
                            contact._fake_img,
                            contact._fake_phone,
                            contact._fake_email,
                            datetime.now(),
                            contact._fake_description,
                            contact._fake_category,
                            contact._show,
                        ),
                    )
                    connection.commit()
                    print(
                        f"Contact: {contact._fake_name} created successfully!"
                    )

    def _populate_contacts_user(self, count):
        sql = """
            INSERT INTO contatos_contacts_user (contact_id, user_id)
            VALUES (%s, %s);
        """

        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                for i in range(count):
                    cursor.execute(sql, (i + 1, 1))
                    connection.commit()
                    print(
                        f"contact_user with id: {i + 1} created successfully!"
                    )


if __name__ == "__main__":
    seed_category = Seeder()

    while True:
        try:
            quantidade = int(input("Quantidade de contatos a serem criados: "))
            check_category = input("Deseja criar categorias? (S/N): ")

            if check_category.upper() == "S":
                seed_category.run(quantidade, create_category=True)
            else:
                seed_category.run(quantidade)

            print("Seeding finished!")
            break
        except ValueError:
            print("Error: Please use a number!")
            continue
