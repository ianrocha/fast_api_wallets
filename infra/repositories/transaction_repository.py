from datetime import datetime

from domain.models.transaction_model import TransactionModel
from infra.database_connection.mysql_connection import MySqlConnection


class TransactionRepository:
    def __init__(self):
        self.conn = MySqlConnection().connect_db()
        self.cursor = self.conn.cursor(dictionary=True)

    def save_historic(self, transaction_model: TransactionModel) -> bool:
        data = {
            "origin_wallet_id": transaction_model.origin_wallet_id,
            "destination_wallet_id": transaction_model.destination_wallet_id,
            "transaction_type_id": transaction_model.transaction_type_id,
            "value": transaction_model.value,
            "operation_date": transaction_model.operation_date or datetime.now(),
        }

        query = "INSERT INTO financial_transactions (origin_wallet_id, destination_wallet_id," \
                "transaction_type_id, movement_value, operation_date) " \
                "VALUES (%(origin_wallet_id)s, %(destination_wallet_id)s," \
                "%(transaction_type_id)s, %(value)s, %(operation_date)s);"

        self.cursor.execute(query, data)
        self.conn.commit()
        return True
