closing_price = 0

with open("NIFTY-I.csv") as a:
    # content = a.readlines()[-200:]
    content = a.readlines()[-50:]
    for line in content:
        tokens = line.split(",")
        close = tokens[4]

        closing_price += float(close)

print(closing_price / 50)
