import re

with open("app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt", "r") as f:
    content = f.read()

pattern = r"Canvas\(modifier = Modifier\.size\(24\.dp\)\) \{.*?drawPath\(path2, color = Color\(0xFFFFC107\), style = Stroke\(width = 2\.dp\.toPx\(\)\)\)\n\s*\}"
replacement = """if (account != null) {
                com.example.ui.components.BankLogo(bankName = account.bankName, size = 24.dp)
            } else {
                Icon(Icons.Default.AccountBalance, contentDescription = null, tint = Color(0xFF1976D2), modifier = Modifier.size(24.dp))
            }"""

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt", "w") as f:
    f.write(content)
