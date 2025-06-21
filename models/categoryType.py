from enum import Enum

class AccountType(Enum):
    CHECKING = "입출금"
    SAVING = '저축'
    INVESTMENT = '투자'
    LOAN = '대출'
    ETC = '기타'
        
class SubCategory(str, Enum):
    HOUSING_COMMUNICATION = "주거통신"
    FINANCIAL_OBLIGATIONS = "보험세금기타금융"
    SUBSCRIPTIONS = "구독서비스"
    CONVENIENCE = "편의점마트잡화"
    DELIVERY = "배달"
    FOOD = "식비"
    TRANSPORT = "교통"
    LIVING = "생활"
    SHOPPING = "쇼핑"
    CAFE_SNACK = "카페간식"
    ALCOHOL = "술유흥"
    BEAUTY = "미용"
    EDUCATION = "교육"
    HEALTH = "의료건강피트니스"
    HOBBY = "취미여가"
    TRAVEL = "여행"
    DONATION = "후원"
    CEREMONY = "경조사비"
    SEND_TRANSFER = "이체"
    ETC = "기타"

