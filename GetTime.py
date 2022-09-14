
from datetime import date

future_date = date(2022, 9, 15)

today = date(1999,7,8)
remaining_days = (future_date - today).days

remaining_days = (remaining_days%3)+1
print(f"{remaining_days}")