with open('app/src/main/java/com/example/ui/screens/HistoryScreen.kt', 'r') as f:
    content = f.read()

content = content.replace("prank transaction", "transaction")
content = content.replace("prank payment", "payment")
content = content.replace("prank", "")
content = content.replace("Prank", "")
content = content.replace("Transaction", "Transaction") # just fixing case if needed
content = content.replace("Make a new  payment", "Make a new payment")

with open('app/src/main/java/com/example/ui/screens/HistoryScreen.kt', 'w') as f:
    f.write(content)
