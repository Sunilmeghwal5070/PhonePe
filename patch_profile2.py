import re

with open('/app/applet/app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'fun ProfileScreen(\n    onBack: () -> Unit\n) {',
    'fun ProfileScreen(\n    onBack: () -> Unit,\n    onNavigateToEditDetails: () -> Unit = {},\n    onNavigateToAccountDetails: () -> Unit = {}\n) {'
)

content = content.replace(
    'modifier = Modifier.clickable { }',
    'modifier = Modifier.clickable { onNavigateToEditDetails() }',
    1 # Only the first occurrence which is 'Manage'
)

content = content.replace(
    'ListItemWithIcon(Icons.Default.AccountBalance, "Bank Accounts", "Set UPI PIN, Add Accounts & more", tint = Color(0xFF1976D2))',
    'ListItemWithIcon(Icons.Default.AccountBalance, "Bank Accounts", "Set UPI PIN, Add Accounts & more", tint = Color(0xFF1976D2), onClick = onNavigateToAccountDetails)'
)

content = content.replace(
    'fun ListItemWithIcon(icon: ImageVector, title: String, subtitle: String?, tint: Color) {',
    'fun ListItemWithIcon(icon: ImageVector, title: String, subtitle: String?, tint: Color, onClick: () -> Unit = {}) {'
)

content = content.replace(
    '.clickable { }\n            .padding(horizontal = 16.dp, vertical = 16.dp),',
    '.clickable { onClick() }\n            .padding(horizontal = 16.dp, vertical = 16.dp),'
)


with open('/app/applet/app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'w') as f:
    f.write(content)
