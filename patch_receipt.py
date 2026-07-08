with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

bad_receipt = '''            composable(
                route = "receipt/{transactionId}",
                    navArgument("transactionId") { type = NavType.IntType },
                    navArgument("name") { type = NavType.StringType }
            ) { backStackEntry ->
                val transactionId = backStackEntry.arguments?.getInt("transactionId") ?: 0
                val name = backStackEntry.arguments?.getString("name") ?: "Karishna Karishna"
                ReceiptScreen('''

bad_receipt_2 = '''            composable(
                route = "receipt/{transactionId}",
                    navArgument("transactionId") { type = NavType.IntType },
                    navArgument("name") { type = NavType.StringType }
            ) { backStackEntry ->
                val transactionId = backStackEntry.arguments?.getInt("transactionId") ?: 0
                ReceiptScreen('''

good_receipt = '''            composable(
                route = "receipt/{transactionId}",
                arguments = listOf(navArgument("transactionId") { type = NavType.IntType })
            ) { backStackEntry ->
                val transactionId = backStackEntry.arguments?.getInt("transactionId") ?: 0
                ReceiptScreen('''

if bad_receipt in content:
    content = content.replace(bad_receipt, good_receipt)
elif bad_receipt_2 in content:
    content = content.replace(bad_receipt_2, good_receipt)
else:
    # Use regex
    import re
    content = re.sub(
        r'composable\(\s*route = "receipt/\{transactionId\}",\s*navArgument\("transactionId"\) \{ type = NavType.IntType \},\s*navArgument\("name"\) \{ type = NavType.StringType \}\s*\) \{ backStackEntry ->\s*val transactionId = backStackEntry.arguments\?\.getInt\("transactionId"\) \?: 0(?:(?:.|\n)*?val name = backStackEntry.arguments\?\.getString\("name"\) \?: "Karishna Karishna"(.|\n)*?)?\s*ReceiptScreen\(',
        '''            composable(
                route = "receipt/{transactionId}",
                arguments = listOf(navArgument("transactionId") { type = NavType.IntType })
            ) { backStackEntry ->
                val transactionId = backStackEntry.arguments?.getInt("transactionId") ?: 0
                ReceiptScreen(''',
        content
    )

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
