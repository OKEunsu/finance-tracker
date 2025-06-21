from models.categoryType import ExpenseCategory
from models.account import AccountType

account_map = {
    "입출금": AccountType.CHECKING,
    "저축": AccountType.SAVING,
    "투자": AccountType.INVESTMENT,
    "대출": AccountType.LOAN,
    "기타": AccountType.ETC
}

spend_map = {
    "주거통신": ExpenseCategory.HOUSING_COMMUNICATION,
    "보험세금기타금융": ExpenseCategory.FINANCIAL_OBLIGATIONS,
    "구독서비스": ExpenseCategory.SUBSCRIPTIONS,
    "편의점마트잡화": ExpenseCategory.CONVENIENCE,
    "배달": ExpenseCategory.DELIVERY,
    "식비": ExpenseCategory.FOOD,
    "교통": ExpenseCategory.TRANSPORT,
    "생활": ExpenseCategory.LIVING,
    "쇼핑": ExpenseCategory.SHOPPING,
    "카페간식": ExpenseCategory.CAFE_SNACK,
    "술유흥": ExpenseCategory.ALCOHOL,
    "미용": ExpenseCategory.BEAUTY,
    "교육": ExpenseCategory.EDUCATION,
    "의료건강피트니스": ExpenseCategory.HEALTH,
    "취미여가": ExpenseCategory.HOBBY,
    "여행": ExpenseCategory.TRAVEL,
    "후원": ExpenseCategory.DONATION,
    "경조사비": ExpenseCategory.CEREMONY,
    "이체": ExpenseCategory.SEND_TRANSFER,
    "기타": ExpenseCategory.ETC,
}
