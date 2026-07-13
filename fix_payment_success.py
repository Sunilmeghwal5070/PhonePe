import re

with open('app/src/main/java/com/example/ui/screens/PaymentSuccessScreen.kt', 'r') as f:
    text = f.read()

text = text.replace("    val view = LocalView.current\n", "")

with open('app/src/main/java/com/example/ui/screens/PaymentSuccessScreen.kt', 'w') as f:
    f.write(text)
