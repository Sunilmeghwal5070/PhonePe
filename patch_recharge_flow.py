import re

with open("app/src/main/java/com/example/ui/screens/RechargeFlowScreens.kt", "r") as f:
    content = f.read()

# Add showWrongPinScreen
content = content.replace('var enteredPin by remember { mutableStateOf("") }',
                          'var enteredPin by remember { mutableStateOf("") }\n    var showWrongPinScreen by remember { mutableStateOf(false) }')

# Replace Toast with state
old_toast = """            } else {
                Toast.makeText(context, "Incorrect UPI PIN", Toast.LENGTH_SHORT).show()
                enteredPin = ""
            }"""
new_wrong_pin = """            } else {
                showWrongPinScreen = true
            }"""
content = content.replace(old_toast, new_wrong_pin)

wrong_pin_ui = """
    if (showWrongPinScreen) {
        WrongPinScreen(
            bankName = bankName,
            bankDesc = "$bankName - 0365",
            errorTitle = "Payment failed",
            onResetPin = { showWrongPinScreen = false; enteredPin = "" },
            onReEnterPin = { showWrongPinScreen = false; enteredPin = "" },
            onDone = { showWrongPinScreen = false }
        )
        return
    }
"""
content = content.replace('    PinEntryScreen(', wrong_pin_ui + '\n    PinEntryScreen(')

with open("app/src/main/java/com/example/ui/screens/RechargeFlowScreens.kt", "w") as f:
    f.write(content)
