import re

with open("app/src/main/java/com/example/ui/screens/WrongPinScreen.kt", "r") as f:
    content = f.read()

# I will add an errorType enum or just pass the text explicitly.
# Let's pass the text explicitly.

content = content.replace('text = "Wrong UPI PIN",', 'text = if (errorTitle.contains("balance", ignoreCase = true)) "Insufficient Balance" else "Wrong UPI PIN",')
content = content.replace('text = "You\'ve entered the wrong UPI PIN. Please check and try again.",', 'text = if (errorTitle.contains("balance", ignoreCase = true)) "Your bank account does not have sufficient balance for this transaction." else "You\'ve entered the wrong UPI PIN. Please check and try again.",')

# Wait, the screenshot shows "Unable to fetch bank balance" for wrong pin because errorTitle has default "Unable to fetch bank balance".
# I'll fix the default error title for WrongPinScreen.
content = content.replace('errorTitle: String = "Unable to fetch bank\\nbalance",', 'errorTitle: String = "Payment failed",')
content = content.replace('text = if (errorTitle.contains("balance", ignoreCase = true)) "Insufficient Balance" else "Wrong UPI PIN",', 'text = if (errorTitle.contains("Insufficient", ignoreCase = true)) "Insufficient Balance" else "Wrong UPI PIN",')
content = content.replace('text = if (errorTitle.contains("balance", ignoreCase = true)) "Your bank account does not have sufficient balance for this transaction." else "You\'ve entered the wrong UPI PIN. Please check and try again.",', 'text = if (errorTitle.contains("Insufficient", ignoreCase = true)) "Your bank account does not have sufficient balance for this transaction. Please try again with a lower amount or use another account." else "You\'ve entered the wrong UPI PIN. Please check and try again.",')

with open("app/src/main/java/com/example/ui/screens/WrongPinScreen.kt", "w") as f:
    f.write(content)
