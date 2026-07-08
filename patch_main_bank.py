import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'onNavigateToAccountDetails = { navController.navigate("account_details") }',
    'onNavigateToAccountDetails = { navController.navigate("bank_accounts") }'
)

new_composables = """            composable("bank_accounts") {
                BankAccountsScreen(
                    onBack = { navController.popBackStack() },
                    onNavigateToAccountDetails = { navController.navigate("account_details") },
                    onNavigateToAddBankAccount = { navController.navigate("add_bank_account") }
                )
            }
            composable("add_bank_account") {
                AddBankAccountScreen(onBack = { navController.popBackStack() })
            }
            composable("account_details") {"""

content = content.replace('            composable("account_details") {', new_composables)

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
