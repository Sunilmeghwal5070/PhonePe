import re

with open('/app/applet/app/src/main/java/com/example/ui/PrankViewModel.kt', 'r') as f:
    content = f.read()

# Change default bank account to SBI
old_default = '''        listOf(
            BankAccount(
                id = "1",
                bankName = "Union Bank",
                accountName = "John",
                bankDesc = "Union Bank Of India - 0365",
                type = ":  Saving Account",
                branch = ":  MUMBAI MAIN",
                ifsc = ":  UBIN0000000"
            )
        )'''
new_default = '''        listOf(
            BankAccount(
                id = "1",
                bankName = "State Bank of India",
                accountName = "John",
                bankDesc = "State Bank of India - 0365",
                type = ":  Saving Account",
                branch = ":  MUMBAI MAIN",
                ifsc = ":  SBIN0000000",
                balance = "Balance: ₹10",
                pin = "1234"
            )
        )'''
content = content.replace(old_default, new_default)

# Enforce max 2 accounts
old_add = '''    fun addBankAccount(account: BankAccount) {
        _bankAccounts.value = _bankAccounts.value + account
    }'''
new_add = '''    fun addBankAccount(account: BankAccount) {
        if (_bankAccounts.value.size < 2) {
            _bankAccounts.value = _bankAccounts.value + account
        }
    }'''
content = content.replace(old_add, new_add)

with open('/app/applet/app/src/main/java/com/example/ui/PrankViewModel.kt', 'w') as f:
    f.write(content)
