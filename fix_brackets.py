import re

with open("app/src/main/java/com/example/ui/screens/HistoryScreen.kt", "r") as f:
    content = f.read()

content = content.replace("com.example.ui.components.BankLogo(bankName = tx.senderBankName, size = 16.dp)", "com.example.ui.components.BankLogo(bankName = tx.senderBankName, size = 16.dp)\n                }\n            }")

with open("app/src/main/java/com/example/ui/screens/HistoryScreen.kt", "w") as f:
    f.write(content)
