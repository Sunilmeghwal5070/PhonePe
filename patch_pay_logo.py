import re

with open('/app/applet/app/src/main/java/com/example/ui/screens/PayAmountScreen.kt', 'r') as f:
    content = f.read()

old_logo = '''// Bank Logo Placeholder
                            Box(modifier = Modifier.size(32.dp).background(Color.White, CircleShape).border(1.dp, Color.LightGray, CircleShape), contentAlignment = Alignment.Center) {
                                Text(selectedBank.bankName.take(1), color = PhonePePurple, fontWeight = FontWeight.Bold)
                            }'''
new_logo = '''// Bank Logo Placeholder
                            com.example.ui.components.BankLogo(selectedBank.bankName, 32.dp)'''

content = content.replace(old_logo, new_logo)

with open('/app/applet/app/src/main/java/com/example/ui/screens/PayAmountScreen.kt', 'w') as f:
    f.write(content)

