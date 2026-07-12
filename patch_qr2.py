import re

with open('app/src/main/java/com/example/ui/screens/QrScreen.kt', 'r') as f:
    text = f.read()

# Fix QrScreen parameters
pattern_sig = r'fun QrScreen\(onBack: \(\) -> Unit = \{\}\) \{'
new_sig = """import com.example.ui.PrankViewModel
fun QrScreen(viewModel: PrankViewModel, onBack: () -> Unit = {}) {"""

text = re.sub(r'fun QrScreen\(onBack: \(\) -> Unit = \{\}\) \{', new_sig, text)

# Insert val banks and upiId
pattern_vars = r'val upiId = "sunilmeghwal6367@ybl"'
new_vars = """val userProfile by viewModel.userProfileManager.userProfile.collectAsState()
    val primaryBank = userProfile.bankAccounts.firstOrNull { it.isPrimary } ?: userProfile.bankAccounts.firstOrNull()
    val bankName = primaryBank?.bankName ?: "State Bank Of India"
    val last4 = primaryBank?.accountNumber?.takeLast(4) ?: "0000"
    val upiId = userProfile.upiId.ifBlank { "unknown@ybl" }"""
text = text.replace(pattern_vars, new_vars)

# Fix the logo
pattern_logo = r'model = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Union_Bank_of_India_Logo.svg/1024px-Union_Bank_of_India_Logo.svg.png"'
new_logo = 'model = getBankLogoUrl(bankName)'
text = text.replace(pattern_logo, new_logo)

# Fix the bank name text
pattern_text = r'text = "Union Bank Of India - 0365"'
new_text = 'text = "$bankName - $last4"'
text = text.replace(pattern_text, new_text)

with open('app/src/main/java/com/example/ui/screens/QrScreen.kt', 'w') as f:
    f.write(text)

