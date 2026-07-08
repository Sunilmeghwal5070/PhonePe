with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

if 'import com.example.ui.screens.SendMoneyScreen' not in content:
    content = content.replace('import com.example.ui.screens.HomeScreen', 'import com.example.ui.screens.HomeScreen\nimport com.example.ui.screens.SendMoneyScreen\nimport com.example.ui.screens.SelectContactScreen\nimport com.example.ui.screens.ChatScreen')

old_home = '''            composable("home") {
                HomeScreen(
                    viewModel = prankViewModel,
                    onCreatePrank = { navController.navigate("create") },
                    onNavigateToCheckBalance = { navController.navigate("check_balance") },
                    onNavigateToHistory = { navController.navigate("history") },
                    onNavigateToProfile = { navController.navigate("profile") },
                    onNavigateToScanner = { navController.navigate("scanner") }
                )
            }'''
new_home = '''            composable("home") {
                HomeScreen(
                    viewModel = prankViewModel,
                    onCreatePrank = { navController.navigate("create") },
                    onNavigateToCheckBalance = { navController.navigate("check_balance") },
                    onNavigateToHistory = { navController.navigate("history") },
                    onNavigateToProfile = { navController.navigate("profile") },
                    onNavigateToScanner = { navController.navigate("scanner") },
                    onNavigateToContactList = { navController.navigate("contact_list") }
                )
            }'''

if old_home in content:
    content = content.replace(old_home, new_home)

new_routes = '''
            composable("contact_list") {
                SendMoneyScreen(
                    viewModel = prankViewModel,
                    onBack = { navController.popBackStack() },
                    onNewPayment = { navController.navigate("select_contact") },
                    onContactSelect = { contactName ->
                        navController.navigate("chat/$contactName")
                    }
                )
            }
            
            composable("select_contact") {
                SelectContactScreen(
                    onBack = { navController.popBackStack() },
                    onContactSelect = { contact ->
                        navController.navigate("chat/${contact.name}")
                    }
                )
            }
            
            composable(
                "chat/{contactName}",
                arguments = listOf(navArgument("contactName") { type = NavType.StringType })
            ) { backStackEntry ->
                val contactName = backStackEntry.arguments?.getString("contactName") ?: ""
                ChatScreen(
                    contactName = contactName,
                    viewModel = prankViewModel,
                    onBack = { navController.popBackStack() },
                    onPayAmount = { amount, name ->
                        // Navigate to pay flow with pre-filled name and amount
                        navController.navigate("pay_amount_prefilled/$amount/$name")
                    }
                )
            }
            
            composable(
                "pay_amount_prefilled/{amount}/{name}",
                arguments = listOf(
                    navArgument("amount") { type = NavType.StringType },
                    navArgument("name") { type = NavType.StringType }
                )
            ) { backStackEntry ->
                val amount = backStackEntry.arguments?.getString("amount") ?: ""
                val name = backStackEntry.arguments?.getString("name") ?: ""
                // Use PayAmountScreen but with prefilled data?
                // Wait, PayAmountScreen currently doesn't take amount/name as args. Let's fix that.
                // We'll modify PayAmountScreen to accept prefilled name
                PayAmountScreen(
                    viewModel = prankViewModel,
                    prefilledName = name,
                    prefilledAmount = amount,
                    onBack = { navController.popBackStack() },
                    onProceed = { amt, bankAccount -> 
                        navController.navigate("pay_pin/$amt/${bankAccount.id}")
                    }
                )
            }
'''

if 'composable("contact_list")' not in content:
    content = content.replace('composable("my_qr") {', new_routes + '\n            composable("my_qr") {')

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
