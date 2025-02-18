import re

price = "gaming123!"
match = re.search(r'\d+', price)
price_value = int(match.group(0))
print(f"{price_value}")