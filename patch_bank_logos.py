import re
import os

files_to_patch = [
    "app/src/main/java/com/example/ui/screens/BankAccountsScreen.kt",
    "app/src/main/java/com/example/ui/screens/AccountDetailsScreen.kt",
    "app/src/main/java/com/example/ui/screens/AddBankAccountDetailsScreen.kt",
    "app/src/main/java/com/example/ui/screens/AddBankAccountScreen.kt"
]

for file in files_to_patch:
    with open(file, "r") as f:
        content = f.read()

    # Just replace coil.compose.AsyncImage or AsyncImage lines with BankLogo
    if "BankAccountsScreen.kt" in file:
        content = re.sub(r'AsyncImage\(\s*model = getBankLogoUrl\(account\.bankName\),\s*contentDescription = null,\s*modifier = Modifier\s*\.size\(40\.dp\)\s*\.clip\(CircleShape\)\s*\.background\(Color\.White\),\s*contentScale = ContentScale\.Fit\s*\)', 'com.example.ui.components.BankLogo(account.bankName, 40.dp)', content)
    elif "AccountDetailsScreen.kt" in file:
        content = re.sub(r'AsyncImage\(\s*model = getBankLogoUrl\(account\?\.bankName \?: "Bank"\),\s*contentDescription = null,\s*modifier = Modifier\.size\(48\.dp\)\.clip\(CircleShape\)\.background\(Color\.White\)\s*\)', 'com.example.ui.components.BankLogo(account?.bankName ?: "Bank", 48.dp)', content)
    elif "AddBankAccountDetailsScreen.kt" in file:
        content = re.sub(r'coil\.compose\.AsyncImage\(model = getBankLogoUrl\(bankName\), contentDescription = bankName, modifier = Modifier\.size\(32\.dp\)\.clip\(RoundedCornerShape\(8\.dp\)\), contentScale = androidx\.compose\.ui\.layout\.ContentScale\.Fit\)', 'com.example.ui.components.BankLogo(bankName, 32.dp)', content)
    elif "AddBankAccountScreen.kt" in file:
        content = re.sub(r'coil\.compose\.AsyncImage\(model = getBankLogoUrl\(name\), contentDescription = name, modifier = Modifier\.size\(32\.dp\)\.clip\(CircleShape\), contentScale = androidx\.compose\.ui\.layout\.ContentScale\.Fit\)', 'com.example.ui.components.BankLogo(name, 32.dp)', content)
        content = re.sub(r'coil\.compose\.AsyncImage\(model = getBankLogoUrl\(name\), contentDescription = name, modifier = Modifier\.size\(32\.dp\)\.clip\(RoundedCornerShape\(8\.dp\)\), contentScale = androidx\.compose\.ui\.layout\.ContentScale\.Fit\)', 'com.example.ui.components.BankLogo(name, 32.dp)', content)

    with open(file, "w") as f:
        f.write(content)
