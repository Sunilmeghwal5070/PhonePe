import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Update ScannerScreen call
old_scanner = """            composable("qr") {
                ScannerScreen(
                    onBack = { navController.popBackStack() },
                    onScanComplete = { navController.navigate("pay_amount") }
                )
            }"""
new_scanner = """            composable("qr") {
                ScannerScreen(
                    onBack = { navController.popBackStack() },
                    onScanSuccess = { name, upi ->
                        navController.navigate("pay_amount/${java.net.URLEncoder.encode(name, "UTF-8")}/${java.net.URLEncoder.encode(upi, "UTF-8")}")
                    }
                )
            }"""
content = content.replace(old_scanner, new_scanner)

# Update pay_amount route
old_pay_amount = """            composable("pay_amount") {
                PayAmountScreen(
                    viewModel = prankViewModel,
                    onBack = { navController.popBackStack() },
                    onProceed = { amount, bankAccount -> 
                        navController.navigate("pay_pin/$amount/${bankAccount.id}/Karishna%20Karishna")
                    }
                )
            }"""
new_pay_amount = """            composable(
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
content = content.replace(old_pay_amount, new_pay_amount)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
