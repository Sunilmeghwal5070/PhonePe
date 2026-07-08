import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

replacement = """
                var showWrongPinScreen by remember { mutableStateOf(false) }
                var pinErrorTitle by remember { mutableStateOf("Payment failed") }
                
                if (showWrongPinScreen) {
                    com.example.ui.screens.WrongPinScreen(
                        bankName = selectedBank?.bankName ?: "Bank",
                        bankDesc = "${selectedBank?.bankName ?: "Bank"} - ${selectedBank?.bankDesc?.takeLast(4) ?: "XXXX"}",
                        errorTitle = pinErrorTitle,
                        onResetPin = { showWrongPinScreen = false; enteredPin = "" },
                        onReEnterPin = { showWrongPinScreen = false; enteredPin = "" },
                        onDone = { navController.popBackStack() }
                    )
                } else {
                    PinEntryScreen(
                        bankName = selectedBank?.bankName ?: "Bank",
                        actionText = "Sending: ₹$amount",
                        pin = enteredPin,
                        onPinChange = { enteredPin = it },
                        onSubmit = {
                            val correctPin = selectedBank?.pin ?: "1234"
                            val paymentAmount = amount.toDoubleOrNull() ?: 0.0
                            if (enteredPin == correctPin) {
                                if (selectedBank != null && paymentAmount > selectedBank.balance) {
                                    pinErrorTitle = "Insufficient Balance"
                                    showWrongPinScreen = true
                                } else {
                                    navController.navigate("pay_processing/$amount/$bankId/${java.net.URLEncoder.encode(name, "UTF-8")}") {
                                        popUpTo("pay_amount") { inclusive = true }
                                    }
                                }
                            } else {
                                pinErrorTitle = "Payment failed"
                                showWrongPinScreen = true
                            }
                        }
                    )
                }
"""

# replace from `PinEntryScreen(` to `Toast.makeText...` to `}`
pattern = r"PinEntryScreen\([\s\S]*?Toast\.makeText[^\n]*\n[^\n]*\}\n[^\n]*\)"
content = re.sub(pattern, replacement.strip(), content)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
