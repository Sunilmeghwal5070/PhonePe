with open("app/src/main/java/com/example/ui/PrankViewModel.kt", "r") as f:
    content = f.read()

new_method = """    fun updateBankAccount(account: BankAccount) {
        val newList = _bankAccounts.value.map { if (it.id == account.id) account else it }
        _bankAccounts.value = newList
        prefsManager.saveBankAccounts(newList)
    }

    fun deleteBankAccount(accountId: String) {
        val newList = _bankAccounts.value.filter { it.id != accountId }
        _bankAccounts.value = newList
        prefsManager.saveBankAccounts(newList)
    }"""

content = content.replace("""    fun updateBankAccount(account: BankAccount) {
        val newList = _bankAccounts.value.map { if (it.id == account.id) account else it }
        _bankAccounts.value = newList
        prefsManager.saveBankAccounts(newList)
    }""", new_method)

with open("app/src/main/java/com/example/ui/PrankViewModel.kt", "w") as f:
    f.write(content)
