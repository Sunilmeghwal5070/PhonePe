import re

with open('/app/applet/app/src/main/java/com/example/ui/screens/BankAccountsScreen.kt', 'r') as f:
    content = f.read()

content = re.sub(r'    var name by remember \{ mutableStateOf\("Sunil"\) \}\n', '', content)
content = content.replace(
    'BasicTextField(value = name, onValueChange = { name = it }, textStyle = TextStyle(fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.Black), modifier = Modifier.weight(1f))',
    'Text("Sunil", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.Black, modifier = Modifier.weight(1f))'
)

with open('/app/applet/app/src/main/java/com/example/ui/screens/BankAccountsScreen.kt', 'w') as f:
    f.write(content)
