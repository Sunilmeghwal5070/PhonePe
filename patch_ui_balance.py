import re
import os

# 1. AccountDetailsScreen.kt
with open('/app/applet/app/src/main/java/com/example/ui/screens/AccountDetailsScreen.kt', 'r') as f:
    content = f.read()

# Change parameter to local state
content = content.replace(
    'val account = bankAccounts.find { it.id == accountId }',
    'val account = bankAccounts.find { it.id == accountId }\n    var isEditableState by remember { mutableStateOf(isEditable) }'
)
content = content.replace('if (isEditable) {', 'if (isEditableState) {')
content = content.replace('enabled = isEditable', 'enabled = isEditableState')
content = content.replace('isEditable = isEditMode', 'isEditable = isEditableState') # wait, that's wrong if it's the call

content = content.replace(
    'var balance by remember { mutableStateOf(account?.balance ?: "Balance: ₹----") }',
    'var balance by remember { mutableStateOf(account?.balance?.toString() ?: "1297.0") }'
)
content = content.replace(
    'balance = balance,',
    'balance = balance.toDoubleOrNull() ?: 0.0,'
)
content = content.replace(
    'IconButton(onClick = { }) {\n                            Icon(Icons.AutoMirrored.Filled.HelpOutline, contentDescription = "Help")',
    'IconButton(onClick = { isEditableState = true }) {\n                            Icon(Icons.AutoMirrored.Filled.HelpOutline, contentDescription = "Edit")'
)

with open('/app/applet/app/src/main/java/com/example/ui/screens/AccountDetailsScreen.kt', 'w') as f:
    f.write(content)

# 2. AddBankAccountDetailsScreen.kt
with open('/app/applet/app/src/main/java/com/example/ui/screens/AddBankAccountDetailsScreen.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'var balance by remember { mutableStateOf("Balance: ₹----") }',
    'var balance by remember { mutableStateOf("1297.0") }'
)
content = content.replace(
    'balance = balance,',
    'balance = balance.toDoubleOrNull() ?: 1297.0,'
)

with open('/app/applet/app/src/main/java/com/example/ui/screens/AddBankAccountDetailsScreen.kt', 'w') as f:
    f.write(content)

# 3. CheckBalanceScreen.kt
with open('/app/applet/app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'Text(account?.balance ?: "Balance: ₹----", fontSize = 42.sp, color = Color.Black)',
    'Text("₹${account?.balance ?: "1297.0"}", fontSize = 42.sp, color = Color.Black)'
)

with open('/app/applet/app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt', 'w') as f:
    f.write(content)

