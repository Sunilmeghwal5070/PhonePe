with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'onNavigateToHistory = { navController.navigate("history") }',
    'onNavigateToHistory = { navController.navigate("history") },\n                    onNavigateToMobileRecharge = { navController.navigate("mobile_recharge") }'
)

routes = """
            composable("mobile_recharge") {
                com.example.ui.screens.MobileRechargeScreen(
                    onBack = { navController.popBackStack() },
                    onContactSelect = { contact ->
                        navController.navigate("recharge_plan/${java.net.URLEncoder.encode(contact.name, "UTF-8")}/${contact.number}")
                    }
                )
            }
            
            composable(
                "recharge_plan/{name}/{number}",
                arguments = listOf(
                    androidx.navigation.navArgument("name") { type = androidx.navigation.NavType.StringType },
                    androidx.navigation.navArgument("number") { type = androidx.navigation.NavType.StringType }
                )
            ) { backStackEntry ->
                val name = backStackEntry.arguments?.getString("name") ?: ""
                val number = backStackEntry.arguments?.getString("number") ?: ""
                com.example.ui.screens.RechargePlanScreen(
                    name = name,
                    number = number,
                    viewModel = prankViewModel,
                    onBack = { navController.popBackStack() },
                    onProceedToPay = { amount ->
                        navController.navigate("recharge_pay_pin/$amount/1/$name")
                    }
                )
            }
            
            composable(
                "recharge_pay_pin/{amount}/{bankId}/{name}",
                arguments = listOf(
                    androidx.navigation.navArgument("amount") { type = androidx.navigation.NavType.StringType },
                    androidx.navigation.navArgument("bankId") { type = androidx.navigation.NavType.StringType },
                    androidx.navigation.navArgument("name") { type = androidx.navigation.NavType.StringType }
                )
            ) { backStackEntry ->
                val amount = backStackEntry.arguments?.getString("amount") ?: "0"
                val bankId = backStackEntry.arguments?.getString("bankId") ?: "1"
                val name = backStackEntry.arguments?.getString("name") ?: ""
                com.example.ui.screens.RechargePinScreen(
                    amount = amount,
                    bankId = bankId,
                    viewModel = prankViewModel,
                    onBack = { navController.popBackStack() },
                    onSuccess = { 
                        navController.navigate("recharge_processing/$amount/$bankId/${java.net.URLEncoder.encode(name, "UTF-8")}") {
                            popUpTo("recharge_plan") { inclusive = false }
                        }
                    }
                )
            }
            
            composable(
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
            }
            
            composable(
                "recharge_success/{amount}/{transactionId}/{name}",
                arguments = listOf(
                    androidx.navigation.navArgument("amount") { type = androidx.navigation.NavType.StringType },
                    androidx.navigation.navArgument("transactionId") { type = androidx.navigation.NavType.IntType },
                    androidx.navigation.navArgument("name") { type = androidx.navigation.NavType.StringType }
                )
            ) { backStackEntry ->
                val amount = backStackEntry.arguments?.getString("amount") ?: "0"
                val name = backStackEntry.arguments?.getString("name") ?: ""
                val transactionId = backStackEntry.arguments?.getInt("transactionId") ?: 0
                com.example.ui.screens.RechargeSuccessScreen(
                    amount = amount,
                    name = name,
                    transactionId = transactionId,
                    onDone = {
                        navController.navigate("home") {
                            popUpTo("home") { inclusive = true }
                        }
                    }
                )
            }
            
            composable("contact_list") {
"""

content = content.replace('composable("contact_list") {', routes)

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
