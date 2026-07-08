with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Update pay_pin to take name
old_pay_pin = '''            composable(
                "pay_pin/{amount}/{bankId}",
                arguments = listOf(
                    navArgument("amount") { type = NavType.StringType },
                    navArgument("bankId") { type = NavType.StringType }
                )
            ) { backStackEntry ->
                val amount = backStackEntry.arguments?.getString("amount") ?: "0"
                val bankId = backStackEntry.arguments?.getString("bankId") ?: ""'''

new_pay_pin = '''            composable(
                "pay_pin/{amount}/{bankId}/{name}",
                arguments = listOf(
                    navArgument("amount") { type = NavType.StringType },
                    navArgument("bankId") { type = NavType.StringType },
                    navArgument("name") { type = NavType.StringType }
                )
            ) { backStackEntry ->
                val amount = backStackEntry.arguments?.getString("amount") ?: "0"
                val bankId = backStackEntry.arguments?.getString("bankId") ?: ""
                val name = backStackEntry.arguments?.getString("name") ?: "Karishna Karishna"'''
content = content.replace(old_pay_pin, new_pay_pin)

# Update nav to pay_processing
content = content.replace('navController.navigate("pay_processing/$amount/$bankId")', 'navController.navigate("pay_processing/$amount/$bankId/$name")')

# Update pay_processing to take name
old_pay_processing = '''            composable(
                "pay_processing/{amount}/{bankId}",
                arguments = listOf(
                    navArgument("amount") { type = NavType.StringType },
                    navArgument("bankId") { type = NavType.StringType }
                )
            ) { backStackEntry ->
                val amount = backStackEntry.arguments?.getString("amount") ?: "0"
                val bankId = backStackEntry.arguments?.getString("bankId") ?: ""'''
new_pay_processing = '''            composable(
                "pay_processing/{amount}/{bankId}/{name}",
                arguments = listOf(
                    navArgument("amount") { type = NavType.StringType },
                    navArgument("bankId") { type = NavType.StringType },
                    navArgument("name") { type = NavType.StringType }
                )
            ) { backStackEntry ->
                val amount = backStackEntry.arguments?.getString("amount") ?: "0"
                val bankId = backStackEntry.arguments?.getString("bankId") ?: ""
                val name = backStackEntry.arguments?.getString("name") ?: "Karishna Karishna"'''
content = content.replace(old_pay_processing, new_pay_processing)

# Update insertTransaction to use the passed name
content = content.replace('name = "Karishna Karishna",', 'name = name,')

# Update nav to pay_success to take name
content = content.replace('navController.navigate("pay_success/$amount/$insertedId")', 'navController.navigate("pay_success/$amount/$insertedId/$name")')

# Update pay_success to take name
old_pay_success = '''            composable(
                "pay_success/{amount}/{transactionId}",
                arguments = listOf(
                    navArgument("amount") { type = NavType.StringType },
                    navArgument("transactionId") { type = NavType.IntType }
                )
            ) { backStackEntry ->
                val amount = backStackEntry.arguments?.getString("amount") ?: "0"
                val txId = backStackEntry.arguments?.getInt("transactionId") ?: 0

                PaymentSuccessScreen(
                    amount = amount,'''
new_pay_success = '''            composable(
                "pay_success/{amount}/{transactionId}/{name}",
                arguments = listOf(
                    navArgument("amount") { type = NavType.StringType },
                    navArgument("transactionId") { type = NavType.IntType },
                    navArgument("name") { type = NavType.StringType }
                )
            ) { backStackEntry ->
                val amount = backStackEntry.arguments?.getString("amount") ?: "0"
                val txId = backStackEntry.arguments?.getInt("transactionId") ?: 0
                val name = backStackEntry.arguments?.getString("name") ?: "Karishna Karishna"

                PaymentSuccessScreen(
                    amount = amount,
                    payeeName = name,'''
content = content.replace(old_pay_success, new_pay_success)

# Update the onProceed calls to pass name
content = content.replace('navController.navigate("pay_pin/$amount/${bankAccount.id}")', 'navController.navigate("pay_pin/$amount/${bankAccount.id}/Karishna Karishna")')
content = content.replace('navController.navigate("pay_pin/$amt/${bankAccount.id}")', 'navController.navigate("pay_pin/$amt/${bankAccount.id}/$name")')

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
