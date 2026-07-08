with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

old_success = '''            composable(
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
                    onDone = {'''

new_success = '''            composable(
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
                    payeeName = name,
                    onDone = {'''

content = content.replace(old_success, new_success)

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
