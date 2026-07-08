import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Make sure imports are present
if "import com.example.ui.screens.PayAmountScreen" not in content:
    content = content.replace("import com.example.ui.screens.HomeScreen", 
'''import com.example.ui.screens.HomeScreen
import com.example.ui.screens.PayAmountScreen
import com.example.ui.screens.PaymentProcessingScreen
import com.example.ui.screens.PaymentSuccessScreen
import com.example.ui.screens.PinEntryScreen
import com.example.ui.BankAccount''')

# Update QR navigation in ScannerScreen
scanner_route_old = '''            composable("qr") {
                ScannerScreen(onBack = { navController.popBackStack() })
            }'''
scanner_route_new = '''            composable("qr") {
                ScannerScreen(
                    onBack = { navController.popBackStack() },
                    onScanComplete = { navController.navigate("pay_amount") }
                )
            }'''
content = content.replace(scanner_route_old, scanner_route_new)

# Add new routes
if 'composable("pay_amount")' not in content:
    routes = '''
            composable("pay_amount") {
                PayAmountScreen(
                    viewModel = prankViewModel,
                    onBack = { navController.popBackStack() },
                    onProceed = { amount, bankAccount -> 
                        navController.navigate("pay_pin/$amount/${bankAccount.id}")
                    }
                )
            }
            
            composable(
                "pay_pin/{amount}/{bankId}",
                arguments = listOf(
                    navArgument("amount") { type = NavType.StringType },
                    navArgument("bankId") { type = NavType.StringType }
                )
            ) { backStackEntry ->
                val amount = backStackEntry.arguments?.getString("amount") ?: "0"
                val bankId = backStackEntry.arguments?.getString("bankId") ?: ""
                val bankAccounts by prankViewModel.bankAccounts.collectAsState()
                val selectedBank = bankAccounts.find { it.id == bankId }
                
                var enteredPin by remember { mutableStateOf("") }
                val context = LocalContext.current
                
                PinEntryScreen(
                    bankName = selectedBank?.bankName ?: "Bank",
                    actionText = "Sending: ₹$amount",
                    pin = enteredPin,
                    onPinChange = { enteredPin = it },
                    onSubmit = {
                        val correctPin = selectedBank?.pin ?: "1234"
                        if (enteredPin == correctPin) {
                            navController.navigate("pay_processing/$amount/$bankId") {
                                popUpTo("pay_amount") { inclusive = true }
                            }
                        } else {
                            Toast.makeText(context, "Incorrect UPI PIN", Toast.LENGTH_SHORT).show()
                            enteredPin = ""
                        }
                    }
                )
            }
            
            composable(
                "pay_processing/{amount}/{bankId}",
                arguments = listOf(
                    navArgument("amount") { type = NavType.StringType },
                    navArgument("bankId") { type = NavType.StringType }
                )
            ) { backStackEntry ->
                val amount = backStackEntry.arguments?.getString("amount") ?: "0"
                val bankId = backStackEntry.arguments?.getString("bankId") ?: ""
                val bankAccounts by prankViewModel.bankAccounts.collectAsState()
                val selectedBank = bankAccounts.find { it.id == bankId }
                
                PaymentProcessingScreen(
                    onProcessingComplete = {
                        // Insert transaction
                        prankViewModel.insertTransaction(
                            name = "Karishna Karishna",
                            phone = "9876543210",
                            upiId = "krishna88750@axl",
                            amount = amount.toDoubleOrNull() ?: 100.0,
                            status = "SUCCESS",
                            bankName = selectedBank?.bankName ?: "State Bank of India",
                            bankLast4 = selectedBank?.bankDesc?.takeLast(4) ?: "0365",
                            customTxId = "",
                            customUtr = "",
                            timestamp = System.currentTimeMillis(),
                            onSuccess = { insertedId ->
                                navController.navigate("pay_success/$amount/$insertedId") {
                                    popUpTo("home")
                                }
                            }
                        )
                    }
                )
            }
            
            composable(
                "pay_success/{amount}/{transactionId}",
                arguments = listOf(
                    navArgument("amount") { type = NavType.StringType },
                    navArgument("transactionId") { type = NavType.IntType }
                )
            ) { backStackEntry ->
                val amount = backStackEntry.arguments?.getString("amount") ?: "0"
                val txId = backStackEntry.arguments?.getInt("transactionId") ?: 0
                
                PaymentSuccessScreen(
                    amount = amount,
                    onDone = {
                        navController.navigate("home") {
                            popUpTo("home") { inclusive = true }
                        }
                    },
                    onViewDetails = {
                        navController.navigate("receipt/$txId") {
                            popUpTo("home")
                        }
                    }
                )
            }
'''
    content = content.replace('composable("create") {', routes + '\n            composable("create") {')

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

