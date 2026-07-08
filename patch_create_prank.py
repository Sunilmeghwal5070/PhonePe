import re

with open("app/src/main/java/com/example/ui/screens/CreatePrankScreen.kt", "r") as f:
    content = f.read()

# Add showWrongPinScreen
content = content.replace('var showPinScreen by remember { mutableStateOf(false) }',
                          'var showPinScreen by remember { mutableStateOf(false) }\n    var showWrongPinScreen by remember { mutableStateOf(false) }')

# Replace Toast with state
old_toast = """                } else {
                    Toast.makeText(context, "Incorrect UPI PIN", Toast.LENGTH_SHORT).show()
                    enteredPin = ""
                }"""
new_wrong_pin = """                } else {
                    showWrongPinScreen = true
                }"""
content = content.replace(old_toast, new_wrong_pin)

# Show WrongPinScreen if true
wrong_pin_ui = """
    if (showWrongPinScreen) {
        WrongPinScreen(
            bankName = senderBankName,
            bankDesc = "$senderBankName - $senderBankLast4",
            errorTitle = "Payment failed",
            onResetPin = { showWrongPinScreen = false; enteredPin = "" },
            onReEnterPin = { showWrongPinScreen = false; enteredPin = "" },
            onDone = { showWrongPinScreen = false; showPinScreen = false }
        )
        return
    }
"""
content = content.replace('    if (showPinScreen) {', wrong_pin_ui + '\n    if (showPinScreen) {')

with open("app/src/main/java/com/example/ui/screens/CreatePrankScreen.kt", "w") as f:
    f.write(content)
