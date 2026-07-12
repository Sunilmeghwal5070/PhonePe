import re

with open('app/src/main/java/com/example/ui/screens/QrScreen.kt', 'r') as f:
    text = f.read()

target = """    val userProfile by viewModel.userProfileManager.userProfile.collectAsState()
    val primaryBank = userProfile.bankAccounts.firstOrNull { it.isPrimary } ?: userProfile.bankAccounts.firstOrNull()
    val bankName = primaryBank?.bankName ?: "State Bank Of India"
    val last4 = primaryBank?.accountNumber?.takeLast(4) ?: "0000"
    val upiId = userProfile.upiId.ifBlank { "unknown@ybl" }"""

replacement = """    val bankAccounts by viewModel.bankAccounts.collectAsState()
    val primaryBank = bankAccounts.firstOrNull()
    val bankName = primaryBank?.bankName ?: "State Bank Of India"
    val last4 = primaryBank?.bankDesc?.takeLast(4) ?: "0000"
    val upiId = primaryBank?.upiIds?.firstOrNull() ?: "unknown@ybl\""""

text = text.replace(target, replacement)

# Add missing import for asStateFlow / collectAsState if needed? It has import androidx.compose.runtime.*, so collectAsState is there.

with open('app/src/main/java/com/example/ui/screens/QrScreen.kt', 'w') as f:
    f.write(text)

