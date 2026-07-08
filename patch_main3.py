import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'ProfileScreen(onBack = { navController.popBackStack() })',
    'ProfileScreen(\n                    onBack = { navController.popBackStack() },\n                    onNavigateToEditDetails = { navController.navigate("edit_details") },\n                    onNavigateToAccountDetails = { navController.navigate("account_details") }\n                )'
)

content = content.replace(
    '            composable("profile") {\n                ProfileScreen(',
    '            composable("profile") {\n                ProfileScreen('
)

# Insert the new composables before the closing braces.
content = content.replace(
    '            composable("profile") {',
    '            composable("edit_details") {\n                EditDetailsScreen(onBack = { navController.popBackStack() })\n            }\n            composable("account_details") {\n                AccountDetailsScreen(\n                    onBack = { navController.popBackStack() },\n                    onNavigateToCheckBalance = { navController.navigate("check_balance") }\n                )\n            }\n            composable("profile") {'
)

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
