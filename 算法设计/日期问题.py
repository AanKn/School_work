import datetime
a = list(map(int, input().split('/')))
dates = set()


def valid_date(year, month, day):
    try:
        dates.add(datetime.date(1900+year, month, day))
    except ValueError:
        pass
    try:
        dates.add(datetime.date(2000+year, month, day))
    except ValueError:
        pass


valid_date(a[0], a[1], a[2])  # 年月日
valid_date(a[2], a[0], a[1])  # 月日年
valid_date(a[2], a[1], a[0])  # 日月年
date_1 = []
for date in dates:
    if datetime.date(2059, 12, 31) >= date >= datetime.date(1960, 1, 1):
        date_1.append(date)
date_1.sort()
for i in date_1:
    print(i)
