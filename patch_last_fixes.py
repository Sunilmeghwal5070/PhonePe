import re

# 1. Fix accName -> name in AccountDetailsScreen.kt
with open("app/src/main/java/com/example/ui/screens/AccountDetailsScreen.kt", "r") as f:
    content = f.read()
content = content.replace("accountName = accName,", "accountName = name,")
with open("app/src/main/java/com/example/ui/screens/AccountDetailsScreen.kt", "w") as f:
    f.write(content)

# 2. Fix accName -> name in AddBankAccountDetailsScreen.kt
with open("app/src/main/java/com/example/ui/screens/AddBankAccountDetailsScreen.kt", "r") as f:
    content = f.read()
content = content.replace("accountName = accName,", "accountName = name,")
with open("app/src/main/java/com/example/ui/screens/AddBankAccountDetailsScreen.kt", "w") as f:
    f.write(content)

# 3. Fix KeyboardArrowRight in RechargeScreens.kt
with open("app/src/main/java/com/example/ui/screens/RechargeScreens.kt", "r") as f:
    content = f.read()
content = content.replace("Icons.AutoMirrored.Filled.KeyboardArrowRight", "Icons.Default.KeyboardArrowRight")
with open("app/src/main/java/com/example/ui/screens/RechargeScreens.kt", "w") as f:
    f.write(content)

