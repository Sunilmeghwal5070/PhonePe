with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Pass skipAnimation=true when coming from PaymentSuccessScreen
content = content.replace(
    'navController.navigate("receipt/$txId") {',
    'navController.navigate("receipt/$txId?skipAnimation=true") {'
)

# Also update HistoryScreen navigation to pass skipAnimation=true just in case it's recent
# Wait, HistoryScreen already goes to receipt/$transactionId. But the route in MainActivity must be updated.

# Update route declaration to accept skipAnimation
content = content.replace(
    'route = "receipt/{transactionId}",\n                arguments = listOf(navArgument("transactionId") { type = NavType.IntType })',
    'route = "receipt/{transactionId}?skipAnimation={skipAnimation}",\n                arguments = listOf(\n                    navArgument("transactionId") { type = NavType.IntType },\n                    navArgument("skipAnimation") { type = NavType.BoolType; defaultValue = false }\n                )'
)

# Extract skipAnimation
content = content.replace(
    'val transactionId = backStackEntry.arguments?.getInt("transactionId") ?: 0\n                ReceiptScreen(\n                    transactionId = transactionId,',
    'val transactionId = backStackEntry.arguments?.getInt("transactionId") ?: 0\n                val skipAnimation = backStackEntry.arguments?.getBoolean("skipAnimation") ?: false\n                ReceiptScreen(\n                    transactionId = transactionId,\n                    skipAnimation = skipAnimation,'
)

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

