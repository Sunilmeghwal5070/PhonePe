import re

with open("app/src/main/java/com/example/ui/screens/BankAccountsScreen.kt", "r") as f:
    content = f.read()

pattern = r"""Box\(\s*modifier = Modifier\s*\.size\(40\.dp\)\s*\.border\(1\.dp, Color\(0xFFEEEEEE\), RoundedCornerShape\(8\.dp\)\),\s*contentAlignment = Alignment\.Center\s*\)\s*\{\s*coil\.compose\.AsyncImage\(\s*model = getBankLogoUrl\(account\.bankName\),\s*contentDescription = account\.bankName,\s*modifier = Modifier\.size\(32\.dp\)\.clip\(RoundedCornerShape\(8\.dp\)\),\s*contentScale = androidx\.compose\.ui\.layout\.ContentScale\.Fit\s*\)\s*\}"""
replacement = """com.example.ui.components.BankLogo(bankName = account.bankName, size = 40.dp)"""

content = re.sub(pattern, replacement, content)

with open("app/src/main/java/com/example/ui/screens/BankAccountsScreen.kt", "w") as f:
    f.write(content)
