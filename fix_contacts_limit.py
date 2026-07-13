import re

with open('app/src/main/java/com/example/ui/screens/RechargeScreens.kt', 'r') as f:
    text = f.read()

text = text.replace("items(filteredContacts.take(50)) { contact ->", "items(filteredContacts) { contact ->")

with open('app/src/main/java/com/example/ui/screens/RechargeScreens.kt', 'w') as f:
    f.write(text)
