import re

with open("app/src/main/java/com/example/ui/screens/HistoryScreen.kt", "r") as f:
    content = f.read()

pattern = r"""// PhonePe Icon Placeholder \(S logo\)[\s\S]*?Text\(\s*text = "S",\s*color = Color\(0xFF5f259f\),\s*fontSize = 10\.sp,\s*fontWeight = FontWeight\.ExtraBold,\s*fontStyle = androidx\.compose\.ui\.text\.font\.FontStyle\.Italic\s*\)\s*\}\s*\}"""

replacement = """// Bank Logo
                    com.example.ui.components.BankLogo(bankName = tx.senderBankName, size = 16.dp)"""

content = re.sub(pattern, replacement, content)

with open("app/src/main/java/com/example/ui/screens/HistoryScreen.kt", "w") as f:
    f.write(content)
