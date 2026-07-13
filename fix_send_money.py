import re

with open('app/src/main/java/com/example/ui/screens/SendMoneyScreen.kt', 'r') as f:
    text = f.read()

text = text.replace("transactions.groupBy { it.receiverName }", "transactions.groupBy { it.receiverName.trim() }")

with open('app/src/main/java/com/example/ui/screens/SendMoneyScreen.kt', 'w') as f:
    f.write(text)
