from models.categoryType import SubCategory
from models.categoryType import AccountType

account_map = {
    "입출금": AccountType.CHECKING,
    "저축": AccountType.SAVING,
    "투자": AccountType.INVESTMENT,
    "대출": AccountType.LOAN,
    "기타": AccountType.ETC
}

spend_map = {
    "주거통신": SubCategory.HOUSING_COMMUNICATION,
    "보험세금기타금융": SubCategory.FINANCIAL_OBLIGATIONS,
    "구독서비스": SubCategory.SUBSCRIPTIONS,
    "편의점마트잡화": SubCategory.CONVENIENCE,
    "배달": SubCategory.DELIVERY,
    "식비": SubCategory.FOOD,
    "교통": SubCategory.TRANSPORT,
    "생활": SubCategory.LIVING,
    "쇼핑": SubCategory.SHOPPING,
    "카페간식": SubCategory.CAFE_SNACK,
    "술유흥": SubCategory.ALCOHOL,
    "미용": SubCategory.BEAUTY,
    "교육": SubCategory.EDUCATION,
    "의료건강피트니스": SubCategory.HEALTH,
    "취미여가": SubCategory.HOBBY,
    "여행": SubCategory.TRAVEL,
    "후원": SubCategory.DONATION,
    "경조사비": SubCategory.CEREMONY,
    "이체": SubCategory.SEND_TRANSFER,
    "기타": SubCategory.ETC,
}
