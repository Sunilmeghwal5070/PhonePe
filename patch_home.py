with open('/app/applet/app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'label = "Mobile\\nRecharge",\n                            onClick = onCreatePrank',
    'label = "Mobile\\nRecharge",\n                            onClick = onNavigateToMobileRecharge'
)

# update HomeScreen signature
content = content.replace(
    'onNavigateToHistory: () -> Unit',
    'onNavigateToHistory: () -> Unit,\n    onNavigateToMobileRecharge: () -> Unit = {}'
)

with open('/app/applet/app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(content)
