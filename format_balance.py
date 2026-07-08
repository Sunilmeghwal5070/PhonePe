with open('/app/applet/app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt', 'r') as f:
    content = f.read()

# Replace the formatting logic
content = content.replace(
    'Text(\n                "₹${account?.balance ?: "1297.0"}",',
    'val displayBalance = account?.balance?.let { if (it % 1.0 == 0.0) it.toInt().toString() else it.toString() } ?: "1297"\n            Text(\n                "₹$displayBalance",'
)

with open('/app/applet/app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt', 'w') as f:
    f.write(content)

with open('/app/applet/app/src/main/java/com/example/ui/screens/AccountDetailsScreen.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'account?.balance?.toString() ?: "1297.0"',
    'account?.balance?.let { if (it % 1.0 == 0.0) it.toInt().toString() else it.toString() } ?: "1297"'
)

with open('/app/applet/app/src/main/java/com/example/ui/screens/AccountDetailsScreen.kt', 'w') as f:
    f.write(content)

with open('/app/applet/app/src/main/java/com/example/ui/screens/AddBankAccountDetailsScreen.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'mutableStateOf("1297.0")',
    'mutableStateOf("1297")'
)
with open('/app/applet/app/src/main/java/com/example/ui/screens/AddBankAccountDetailsScreen.kt', 'w') as f:
    f.write(content)
