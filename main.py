from database import init_db, SessionLocal
from models.account import Account
from models.account_type import AccountType
from models.asset_snapshot import AssetSnapshot

init_db()
db = SessionLocal()

# 계좌 생성
acc = Account(bank_name="카카오뱅크", account_name="생활비", account_type=AccountType.CHECKING)
db.add(acc)
db.commit()
db.refresh(acc)

# 월별 잔액 기록
snap = AssetSnapshot(account_id=acc.id, year_month="2024-06", balance=125000)
db.add(snap)
db.commit()

# 확인
for snapshot in db.query(AssetSnapshot).all():
    print(snapshot.year_month, snapshot.balance)
