from enum import Enum

class AccountType(Enum):
    CHECKING = "입출금"
    SAVING = '저축'
    INVESTMENT = '투자'
    POINT = '포인트'
    LOAN = '대출'
    ETC = '기타'