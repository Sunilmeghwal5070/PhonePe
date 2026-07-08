with open('/app/applet/app/src/main/java/com/example/ui/PrankViewModel.kt', 'r') as f:
    content = f.read()

content = content.replace('val balance: String = "Balance: ₹----"', 'val balance: Double = 1297.0')

# deduct balance on payment
import re

target = """        viewModelScope.launch {
            val resolvedTxId = customTxId.ifBlank { generateTransactionId() }"""

replacement = """        viewModelScope.launch {
            val resolvedTxId = customTxId.ifBlank { generateTransactionId() }
            
            // Deduct balance
            val actualAmount = if (amount <= 0.0) 100.0 else amount
            _bankAccounts.value = _bankAccounts.value.map { acc ->
                if (acc.bankName == bankName || acc.bankDesc.contains(bankLast4)) {
                    acc.copy(balance = acc.balance - actualAmount)
                } else acc
            }
"""

content = content.replace(target, replacement)

with open('/app/applet/app/src/main/java/com/example/ui/PrankViewModel.kt', 'w') as f:
    f.write(content)
