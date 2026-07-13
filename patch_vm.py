import re

with open('app/src/main/java/com/example/ui/PrankViewModel.kt', 'r') as f:
    text = f.read()

target = "    val bankAccounts: StateFlow<List<BankAccount>> = _bankAccounts.asStateFlow()"
replacement = "    val bankAccounts: StateFlow<List<BankAccount>> = _bankAccounts.asStateFlow()\n\n    private val _isShakeEnabled = MutableStateFlow(prefsManager.isShakeEnabled())\n    val isShakeEnabled: StateFlow<Boolean> = _isShakeEnabled.asStateFlow()\n    fun setShakeEnabled(enabled: Boolean) {\n        _isShakeEnabled.value = enabled\n        prefsManager.setShakeEnabled(enabled)\n    }"

text = text.replace(target, replacement)

with open('app/src/main/java/com/example/ui/PrankViewModel.kt', 'w') as f:
    f.write(text)
