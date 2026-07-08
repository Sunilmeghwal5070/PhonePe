import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

target = """                com.example.ui.screens.RechargePinScreen(
                    amount = amount,
                    bankId = bankId,
                    viewModel = prankViewModel,
                    onBack = { navController.popBackStack() },
                    onSuccess = { 
                        navController.navigate("recharge_processing/$amount/$bankId/${java.net.URLEncoder.encode(name, "UTF-8")}") {
                            popUpTo("recharge_plan") { inclusive = false }
                        }
                    }
                )"""

replacement = """                com.example.ui.screens.RechargePinScreen(
                    amount = amount,
                    bankId = bankId,
                    name = name,
                    viewModel = prankViewModel,
                    onBack = { navController.popBackStack() },
                    onSuccess = { txId ->
                        navController.navigate("recharge_processing/$amount/$txId/${java.net.URLEncoder.encode(name, "UTF-8")}") {
                            popUpTo("recharge_plan") { inclusive = false }
                        }
                    }
                )"""

content = content.replace(target, replacement)

# Change recharge_processing arguments in MainActivity:
# "recharge_processing/{amount}/{bankId}/{name}" -> "recharge_processing/{amount}/{transactionId}/{name}"
# Note: bankId was passed but not used except for URL?
# Wait! RechargeProcessingScreen takes name, amount, onSuccess.

target_proc = """            composable(
                "recharge_processing/{amount}/{bankId}/{name}",
                arguments = listOf(
                    androidx.navigation.navArgument("amount") { type = androidx.navigation.NavType.StringType },
                    androidx.navigation.navArgument("bankId") { type = androidx.navigation.NavType.StringType },
                    androidx.navigation.navArgument("name") { type = androidx.navigation.NavType.StringType }
                )
            ) { backStackEntry ->
                val amount = backStackEntry.arguments?.getString("amount") ?: "0"
                val bankId = backStackEntry.arguments?.getString("bankId") ?: "1"
                val name = backStackEntry.arguments?.getString("name") ?: ""
                com.example.ui.screens.RechargeProcessingScreen(
                    name = name,
                    amount = amount,
                    onSuccess = { transactionId ->
                        navController.navigate("recharge_success/$amount/$transactionId/${java.net.URLEncoder.encode(name, "UTF-8")}") {
                            popUpTo("mobile_recharge") { inclusive = false }
                        }
                    }
                )
            }"""

replacement_proc = """            composable(
                "recharge_processing/{amount}/{transactionId}/{name}",
                arguments = listOf(
                    androidx.navigation.navArgument("amount") { type = androidx.navigation.NavType.StringType },
                    androidx.navigation.navArgument("transactionId") { type = androidx.navigation.NavType.IntType },
                    androidx.navigation.navArgument("name") { type = androidx.navigation.NavType.StringType }
                )
            ) { backStackEntry ->
                val amount = backStackEntry.arguments?.getString("amount") ?: "0"
                val transactionId = backStackEntry.arguments?.getInt("transactionId") ?: 0
                val name = backStackEntry.arguments?.getString("name") ?: ""
                com.example.ui.screens.RechargeProcessingScreen(
                    name = name,
                    amount = amount,
                    onSuccess = { 
                        navController.navigate("recharge_success/$amount/$transactionId/${java.net.URLEncoder.encode(name, "UTF-8")}") {
                            popUpTo("mobile_recharge") { inclusive = false }
                        }
                    }
                )
            }"""

content = content.replace(target_proc, replacement_proc)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

