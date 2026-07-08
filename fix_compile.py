import re

with open("app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt", "r") as f:
    content = f.read()

content = content.replace("account = selectedAccount,", "accountId = selectedAccount?.id,")

with open("app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/ui/screens/CreatePrankScreen.kt", "r") as f:
    content = f.read()

content = content.replace("""val finalAmount = amount.toDoubleOrNull() ?: 100.0
                    val finalAmount = amount.toDoubleOrNull() ?: 100.0""", """val finalAmount = amount.toDoubleOrNull() ?: 100.0""")

with open("app/src/main/java/com/example/ui/screens/CreatePrankScreen.kt", "w") as f:
    f.write(content)

