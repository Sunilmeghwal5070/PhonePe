with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    text = f.read()
text = text.replace('"Recent Prank Transactions"', '"Recent Transactions"')
text = text.replace('"No pranks have been made yet"', '"No transactions yet"')
with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(text)

with open('app/src/main/java/com/example/ui/screens/AlertsScreen.kt', 'r') as f:
    text = f.read()
text = text.replace('"Prank Master Medal received! 🏆"', '"Rewards unlocked! 🏆"')
with open('app/src/main/java/com/example/ui/screens/AlertsScreen.kt', 'w') as f:
    f.write(text)

with open('app/src/main/java/com/example/ui/screens/CreatePrankScreen.kt', 'r') as f:
    text = f.read()
text = text.replace('"New Prank Payment"', '"New Payment"')
with open('app/src/main/java/com/example/ui/screens/CreatePrankScreen.kt', 'w') as f:
    f.write(text)

with open('app/src/main/java/com/example/ui/screens/ReceiptScreen.kt', 'r') as f:
    text = f.read()
text = text.replace('*PhonePe Transaction Receipt* (Prank App)', '*PhonePe Transaction Receipt*')
text = text.replace('Created via PhonePe Prank Clone! 😉', 'Shared via PhonePe')
text = text.replace('"Prank Balance"', '"Check Balance"')
with open('app/src/main/java/com/example/ui/screens/ReceiptScreen.kt', 'w') as f:
    f.write(text)
