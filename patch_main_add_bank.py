import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

new_composables = """            composable("add_bank_account") {
                AddBankAccountScreen(
                    onBack = { navController.popBackStack() },
                    onNavigateToAddBankAccountDetails = { bankName ->
                        navController.navigate("add_bank_account_details/$bankName")
                    }
                )
            }
            composable(
                "add_bank_account_details/{bankName}",
                arguments = listOf(navArgument("bankName") { type = NavType.StringType })
            ) { backStackEntry ->
                val bankName = backStackEntry.arguments?.getString("bankName") ?: "Bank"
                AddBankAccountDetailsScreen(
                    bankName = bankName,
                    onBack = { navController.popBackStack() },
                    onSave = {
                        navController.navigate("bank_accounts") {
                            popUpTo("bank_accounts") { inclusive = false }
                        }
                    }
                )
            }
            composable("account_details") {"""

content = content.replace("""            composable("add_bank_account") {
                AddBankAccountScreen(onBack = { navController.popBackStack() })
            }
            composable("account_details") {""", new_composables)

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
