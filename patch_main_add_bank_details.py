import re

with open('/app/applet/app/src/main/java/com/example/ui/screens/AddBankAccountDetailsScreen.kt', 'r') as f:
    content = f.read()

content = content.replace('fun AddBankAccountDetailsScreen(\n    bankName: String,\n    onBack: () -> Unit,\n    onSave: () -> Unit\n) {',
'''import com.example.ui.PrankViewModel
import com.example.ui.BankAccount

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AddBankAccountDetailsScreen(
    bankName: String,
    viewModel: PrankViewModel,
    onBack: () -> Unit,
    onSave: () -> Unit
) {''')

content = content.replace('TextButton(onClick = onSave) {',
'''TextButton(onClick = {
                        viewModel.addBankAccount(
                            BankAccount(
                                bankName = bankName,
                                accountName = name,
                                bankDesc = bankDesc,
                                type = accType,
                                branch = branch,
                                ifsc = ifsc,
                                balance = balance
                            )
                        )
                        onSave()
                    }) {''')

content = content.replace('@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nimport', 'import')

with open('/app/applet/app/src/main/java/com/example/ui/screens/AddBankAccountDetailsScreen.kt', 'w') as f:
    f.write(content)


with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    main_content = f.read()

main_content = main_content.replace('''composable("bank_accounts") {
                BankAccountsScreen(
                    onBack = { navController.popBackStack() },
                    onNavigateToAccountDetails = { navController.navigate("account_details") },
                    onNavigateToAddBankAccount = { navController.navigate("add_bank_account") }
                )
            }''', '''composable("bank_accounts") {
                BankAccountsScreen(
                    viewModel = prankViewModel,
                    onBack = { navController.popBackStack() },
                    onNavigateToAccountDetails = { id, isEditMode -> 
                        navController.navigate("account_details/$id/$isEditMode") 
                    },
                    onNavigateToAddBankAccount = { navController.navigate("add_bank_account") }
                )
            }''')

main_content = main_content.replace('''composable(
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
            }''', '''composable(
                "add_bank_account_details/{bankName}",
                arguments = listOf(navArgument("bankName") { type = NavType.StringType })
            ) { backStackEntry ->
                val bankName = backStackEntry.arguments?.getString("bankName") ?: "Bank"
                AddBankAccountDetailsScreen(
                    bankName = bankName,
                    viewModel = prankViewModel,
                    onBack = { navController.popBackStack() },
                    onSave = {
                        navController.navigate("bank_accounts") {
                            popUpTo("bank_accounts") { inclusive = false }
                        }
                    }
                )
            }''')

main_content = main_content.replace('''composable("account_details") {
                AccountDetailsScreen(
                    onBack = { navController.popBackStack() },
                    onNavigateToCheckBalance = { navController.navigate("check_balance") }
                )
            }''', '''composable(
                "account_details/{id}/{isEditMode}",
                arguments = listOf(
                    navArgument("id") { type = NavType.StringType },
                    navArgument("isEditMode") { type = NavType.BoolType }
                )
            ) { backStackEntry ->
                val id = backStackEntry.arguments?.getString("id") ?: ""
                val isEditMode = backStackEntry.arguments?.getBoolean("isEditMode") ?: false
                AccountDetailsScreen(
                    accountId = id,
                    isEditable = isEditMode,
                    viewModel = prankViewModel,
                    onBack = { navController.popBackStack() },
                    onNavigateToCheckBalance = { navController.navigate("check_balance") }
                )
            }''')

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(main_content)

