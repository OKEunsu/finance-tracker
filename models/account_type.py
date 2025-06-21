from enum import Enum

class AccountType(Enum):
    CHECKING = "입출금"
    SAVING = '저축'
    INVESTMENT = '투자'
    LOAN = '대출'
    ETC = '기타'
        
if __name__ == '__main__':
    print(AccountType.CHECKING.value)