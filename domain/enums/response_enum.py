from enum import Enum


class ResponseEum(int, Enum):
    transfer_completed = 200
    not_authorized = 422
    not_implemented = 500