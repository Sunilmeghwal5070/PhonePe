import re

with open('/app/applet/app/src/main/java/com/example/ui/screens/AccountDetailsScreen.kt', 'r') as f:
    content = f.read()

# Remove the state variables
content = re.sub(r'    var name by remember \{ mutableStateOf\("Sunil"\) \}\n', '', content)
content = re.sub(r'    var bankDesc by remember \{ mutableStateOf\("Union Bank Of India - 0365"\) \}\n', '', content)
content = re.sub(r'    var accType by remember \{ mutableStateOf\(":  Saving Account"\) \}\n', '', content)
content = re.sub(r'    var branch by remember \{ mutableStateOf\(":  NIMBAHERA"\) \}\n', '', content)
content = re.sub(r'    var ifsc by remember \{ mutableStateOf\(":  UBIN0918610"\) \}\n', '', content)
content = re.sub(r'    var upiPinStatus by remember \{ mutableStateOf\("4 digit UPI PIN exists"\) \}\n', '', content)
content = re.sub(r'    var balance by remember \{ mutableStateOf\("Balance: ₹----"\) \}\n', '', content)

# Replace BasicTextField with Text
content = content.replace(
    'BasicTextField(value = name, onValueChange = { name = it }, textStyle = TextStyle(fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color.Black))',
    'Text("Sunil", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color.Black)'
)
content = content.replace(
    'BasicTextField(value = bankDesc, onValueChange = { bankDesc = it }, textStyle = TextStyle(fontSize = 14.sp, color = Color.Gray))',
    'Text("Union Bank Of India - 0365", fontSize = 14.sp, color = Color.Gray)'
)
content = content.replace(
    'BasicTextField(value = accType, onValueChange = { accType = it }, textStyle = TextStyle(fontSize = 14.sp, color = Color.Gray))',
    'Text(":  Saving Account", fontSize = 14.sp, color = Color.Gray)'
)
content = content.replace(
    'BasicTextField(value = branch, onValueChange = { branch = it }, textStyle = TextStyle(fontSize = 14.sp, color = Color.Gray))',
    'Text(":  NIMBAHERA", fontSize = 14.sp, color = Color.Gray)'
)
content = content.replace(
    'BasicTextField(value = ifsc, onValueChange = { ifsc = it }, textStyle = TextStyle(fontSize = 14.sp, color = Color.Gray))',
    'Text(":  UBIN0918610", fontSize = 14.sp, color = Color.Gray)'
)
content = content.replace(
    'BasicTextField(value = upiPinStatus, onValueChange = { upiPinStatus = it }, textStyle = TextStyle(fontSize = 14.sp, color = Color.Gray))',
    'Text("4 digit UPI PIN exists", fontSize = 14.sp, color = Color.Gray)'
)
content = content.replace(
    'BasicTextField(value = balance, onValueChange = { balance = it }, textStyle = TextStyle(fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.Black))',
    'Text("Balance: ₹----", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.Black)'
)

# Revert UpiIdRow
content = re.sub(r'@Composable\nfun UpiIdRow\(id: String, isActivate: Boolean\) \{\n    var upiId by remember \{ mutableStateOf\(id\) \}\n    Column \{',
                 '@Composable\nfun UpiIdRow(id: String, isActivate: Boolean) {\n    Column {',
                 content)

content = content.replace(
    'BasicTextField(value = upiId, onValueChange = { upiId = it }, textStyle = TextStyle(fontSize = 16.sp, color = Color.Black), modifier = Modifier.weight(1f))',
    'Text(id, fontSize = 16.sp, color = Color.Black, modifier = Modifier.weight(1f))'
)

# Add modifier to Text(id) since it's probably missing it in the replacement text but let's check what was replaced
# Originally it was Text(id, fontSize = 16.sp, color = Color.Black)
content = content.replace('Text(id, fontSize = 16.sp, color = Color.Black, modifier = Modifier.weight(1f))', 'Text(id, fontSize = 16.sp, color = Color.Black)')

with open('/app/applet/app/src/main/java/com/example/ui/screens/AccountDetailsScreen.kt', 'w') as f:
    f.write(content)
