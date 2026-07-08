with open('/app/applet/app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'onNavigateToContactList: () -> Unit = {}',
    'onNavigateToContactList: () -> Unit = {},\n    onNavigateToMobileRecharge: () -> Unit = {}'
)

with open('/app/applet/app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(content)

with open('/app/applet/app/src/main/java/com/example/ui/screens/RechargeFlowScreens.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'val currentBal = it.balance.toDoubleOrNull() ?: 1297.0',
    'val currentBal = it.balance'
)

with open('/app/applet/app/src/main/java/com/example/ui/screens/RechargeFlowScreens.kt', 'w') as f:
    f.write(content)
