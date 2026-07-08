import re

with open('/app/applet/app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'fun ListItemWithAction(icon: ImageVector, title: String, subtitle: String, actionText: String, tint: Color) {',
    'fun ListItemWithAction(icon: ImageVector, title: String, subtitle: String, actionText: String, tint: Color, onClick: () -> Unit = {}) {'
)

with open('/app/applet/app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'w') as f:
    f.write(content)
