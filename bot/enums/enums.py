from enum import Enum

class OrderStatuses(Enum):
    paid = "paid"
    pending = "pending"
    nonpaid = "nonpaid"