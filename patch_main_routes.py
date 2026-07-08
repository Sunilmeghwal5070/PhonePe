import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# I will update ScannerScreen to just save it to viewModel
old_scanner = """            composable("qr") {
                ScannerScreen(
                    onBack = { navController.popBackStack() },
                    onScanSuccess = { name, upi ->
                        navController.navigate("pay_amount/${java.net.URLEncoder.encode(name, "UTF-8")}/${java.net.URLEncoder.encode(upi, "UTF-8")}")
                    }
                )
            }"""
new_scanner = """            composable("qr") {
                ScannerScreen(
                    onBack = { navController.popBackStack() },
                    onScanSuccess = { name, upi ->
                        prankViewModel.selectedPayeeUpi = upi
                        navController.navigate("pay_amount/${java.net.URLEncoder.encode(name, "UTF-8")}")
                    }
                )
            }"""
content = content.replace(old_scanner, new_scanner)

# And revert pay_amount route back to single param
old_pay_amount = """            composable(
                "pay_amount/{name}/{upi}",
                arguments = listOf(
                    androidx.navigation.navArgument("name") { type = androidx.navigation.NavType.StringType },
                    androidx.navigation.navArgument("upi") { type = androidx.navigation.NavType.StringType }
                )
            ) { backStackEntry ->
                val name = java.net.URLDecoder.decode(backStackEntry.arguments?.getString("name") ?: "Karishna Karishna", "UTF-8")
                val upi = java.net.URLDecoder.decode(backStackEntry.arguments?.getString("upi") ?: "unknown@upi", "UTF-8")
                
                PayAmountScreen(
                    viewModel = prankViewModel,
                    payeeName = name,
                    upiId = upi,
                    onBack = { navController.popBackStack() },
                    onProceed = { amount, bankAccount -> 
                        navController.navigate("pay_pin/$amount/${bankAccount.id}/${java.net.URLEncoder.encode(name, "UTF-8")}")
                    }
                )
            }"""
new_pay_amount = """            composable(
                "pay_amount/{name}",
                arguments = listOf(
                    androidx.navigation.navArgument("name") { type = androidx.navigation.NavType.StringType }
                )
            ) { backStackEntry ->
                val name = java.net.URLDecoder.decode(backStackEntry.arguments?.getString("name") ?: "Karishna Karishna", "UTF-8")
                
                PayAmountScreen(
                    viewModel = prankViewModel,
                    payeeName = name,
                    upiId = prankViewModel.selectedPayeeUpi,
                    onBack = { navController.popBackStack() },
                    onProceed = { amount, bankAccount -> 
                        navController.navigate("pay_pin/$amount/${bankAccount.id}/${java.net.URLEncoder.encode(name, "UTF-8")}")
                    }
                )
            }"""
content = content.replace(old_pay_amount, new_pay_amount)

# Update the generic "pay_amount" no-param route which might still be there for manual clicks
old_pay_amount_noparam = """            composable("pay_amount") {
                PayAmountScreen(
                    viewModel = prankViewModel,
                    onBack = { navController.popBackStack() },
                    onProceed = { amount, bankAccount -> 
                        navController.navigate("pay_pin/$amount/${bankAccount.id}/Karishna%20Karishna")
                    }
                )
            }"""
content = content.replace(old_pay_amount_noparam, "")

# And in payment success, inject upiId
old_pay_success = """                PaymentSuccessScreen(
                    amount = amount,
                    payeeName = name,
                    onDone = {"""
new_pay_success = """                PaymentSuccessScreen(
                    amount = amount,
                    payeeName = name,
                    upiId = prankViewModel.selectedPayeeUpi,
                    onDone = {"""
content = content.replace(old_pay_success, new_pay_success)

# And in CreatePrankScreen, when we hit pay, we can update selectedPayeeUpi
# Actually, I'll update it inside CreatePrankScreen if needed, or it's fine.

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
