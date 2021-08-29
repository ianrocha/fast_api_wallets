from typing import Optional

from domain.models.user_model import UserModel
from infra.database_connection.mysql_connection import MySqlConnection


class UserRepository:
    def __init__(self):
        self.conn = MySqlConnection().connect_db()
        self.cursor = self.conn.cursor(dictionary=True)

    def get_user(self, user_id: int) -> dict:
        data = {
            "user_id": user_id
        }
        query = "SELECT * FROM users WHERE user_id = %(user_id)s"

        self.cursor.execute(query, data)
        return self.cursor.fetchone()

    def insert_user(self, user: UserModel) -> Optional[int]:
        query = "INSERT INTO users (name, document, email, password, is_shopkeeper, is_active) " \
                "VALUES (%(name)s, %(document)s, %(email)s, %(password)s, " \
                "%(is_shopkeeper)s, %(is_active)s);" \
                "SELECT LAST_INSERT_ID();"
        data = {
            "name": user.name,
            "document": user.document,
            "email": user.email,
            "password": user.password,
            "is_shopkeeper": user.is_shopkeeper,
            "is_active": user.is_active
        }

        result = self.cursor.execute(query, data, multi=True)
        last_inserted_id = next(result).lastrowid
        self.conn.commit()

        return last_inserted_id

    def inactivate_user(self, user_id: int):
        data = {
            "user_id": user_id
        }

        query = "UPDATE users " \
                "SET is_active = 0 " \
                "WHERE user_id = %(user_id)s"

        self.cursor.execute(query, data)
        self.conn.commit()
        return True
