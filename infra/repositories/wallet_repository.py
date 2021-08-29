import mysql.connector

from domain.models.transaction_model import TransactionModel
from infra.database_connection.mysql_connection import MySqlConnection


class WalletRepository:
    def __init__(self):
        self.conn = MySqlConnection().connect_db()
        self.cursor = self.conn.cursor(dictionary=True)

    def get_user_wallet(self, user_id: int):
        data = {
            "user_id": user_id
        }
        query = "SELECT * FROM wallets WHERE user_id = %(user_id)s"

        self.cursor.execute(query, data)
        return self.cursor.fetchone()

    def insert_wallet(self, user_id: int, total: float = 0.0) -> bool:
        data = {
            "user_id": user_id,
            "total": total
        }
        query = "INSERT INTO wallets (user_id, total) " \
                "VALUES (%(user_id)s, %(total)s);"

        self.cursor.execute(query, data)
        self.conn.commit()
        return True

    def do_deposit(self, transaction_model: TransactionModel) -> bool:
        try:
            prev_destination_total = self.select_total(wallet_id=transaction_model.destination_wallet_id)
            new_destination_total = prev_destination_total + transaction_model.value
            self.update_wallet_total(wallet_id=transaction_model.destination_wallet_id, total=new_destination_total)
            self.conn.commit()
            return True
        except mysql.connector.Error as error:
            self.conn.rollback()
            return False

    def do_transfer(self, transaction_model: TransactionModel):
        try:

            prev_origin_total = self.select_total(wallet_id=transaction_model.origin_wallet_id)
            new_origin_total = prev_origin_total - transaction_model.value

            self.update_wallet_total(wallet_id=transaction_model.origin_wallet_id, total=new_origin_total)

            prev_destination_total = self.select_total(wallet_id=transaction_model.destination_wallet_id)
            new_destination_total = prev_destination_total + transaction_model.value
            self.update_wallet_total(wallet_id=transaction_model.destination_wallet_id, total=new_destination_total)

            self.conn.commit()
            return True
        except mysql.connector.Error as error:
            self.conn.rollback()
            return False

    def select_total(self, wallet_id: int) -> float:
        data = {
            "wallet_id": wallet_id
        }
        prev_query = "SELECT total FROM wallets WHERE wallet_id = %(wallet_id)s FOR UPDATE OF wallets;"
        self.cursor.execute(prev_query, data)
        result = self.cursor.fetchone()
        return result.get("total")

    def update_wallet_total(self, wallet_id: int, total: float):
        data = {
            "wallet_id": wallet_id,
            "total": total
        }
        update_query = "UPDATE wallets SET total = %(total)s WHERE wallet_id = %(wallet_id)s;"
        self.cursor.execute(update_query, data)
