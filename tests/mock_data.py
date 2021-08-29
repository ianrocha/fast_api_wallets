def mock_user():
    user_mock = {
        "user_id": 4,
        "name": "Testonildo",
        "document": "12345",
        "email": "testonildo@test.com",
        "password": "54321",
        "is_shopkeeper": False,
        "is_active": True,
    }
    return user_mock


def mock_wallet():
    return {
        "wallet_id": 5,
        "user_id": 5,
        "total": 43590.50
    }


def mock_transaction_transfer():
    return {
        "origin_user_id": 4,
        "origin_wallet_id": 4,
        "destination_wallet_id": 5,
        "transaction_type_id": 2,
        "value": 150.00
    }


def mock_getcode():
    return 201


def mock_read_authorized():
    return b'{"message": "Autorizado"}'


def mock_read_not_authorized():
    return b'{"message": "Nao Autorizado"}'
