with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

target = """                com.example.ui.screens.RechargeSuccessScreen(
                    amount = amount,
                    name = name,
                    transactionId = transactionId,
                    onDone = {
                        navController.navigate("home") {
                            popUpTo("home") { inclusive = true }
                        }
                    }
                )"""

replacement = """                com.example.ui.screens.RechargeSuccessScreen(
                    transactionId = transactionId,
                    viewModel = prankViewModel,
                    onDone = {
                        navController.navigate("home") {
                            popUpTo("home") { inclusive = true }
                        }
                    }
                )"""

if target in content:
    content = content.replace(target, replacement)
    print("Replaced main success screen call")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

