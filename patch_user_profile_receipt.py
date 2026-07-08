import re

with open("app/src/main/java/com/example/ui/screens/ReceiptScreen.kt", "r") as f:
    content = f.read()

# Let's see if it's there
if "val userProfile by" not in content:
    content = content.replace("val tx by viewModel.selectedTransaction.collectAsState()", "val tx by viewModel.selectedTransaction.collectAsState()\n    val userProfile by viewModel.userProfileManager.userProfile.collectAsState()")

with open("app/src/main/java/com/example/ui/screens/ReceiptScreen.kt", "w") as f:
    f.write(content)
