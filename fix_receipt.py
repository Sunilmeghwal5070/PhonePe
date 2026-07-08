with open('app/src/main/java/com/example/ui/screens/ReceiptScreen.kt', 'r') as f:
    content = f.read()

content = content.replace("Check your prank bank balance!", "Check your bank balance!")
content = content.replace("Here you can enter any fake amount and surprise your friends!", "Enter the amount.")
content = content.replace("Fake Bank Balance", "Bank Balance")

with open('app/src/main/java/com/example/ui/screens/ReceiptScreen.kt', 'w') as f:
    f.write(content)
