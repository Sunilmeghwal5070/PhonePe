import re

with open("app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt", "r") as f:
    content = f.read()

# Replace SuccessScreen signature
content = content.replace("fun SuccessScreen(account: BankAccount?, viewModel: PrankViewModel, onBack: () -> Unit) {", "fun SuccessScreen(accountId: String?, viewModel: PrankViewModel, onBack: () -> Unit) {\n    val bankAccounts by viewModel.bankAccounts.collectAsState()\n    val account = bankAccounts.find { it.id == accountId }")

# In CheckBalanceScreen, replace SuccessScreen(selectedAccount, ...) with SuccessScreen(selectedAccount?.id, ...)
content = content.replace("SuccessScreen(selectedAccount, viewModel, onBack)", "SuccessScreen(selectedAccount?.id, viewModel, onBack)")

with open("app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt", "w") as f:
    f.write(content)
