import re

with open("app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt", "r") as f:
    content = f.read()

# Replace Toast with state transition
old_code = """                        if (enteredPin == selectedAccount?.pin) {
                            currentState = CheckBalanceState.LOADING
                        } else {
                            Toast.makeText(context, "Incorrect UPI PIN", Toast.LENGTH_SHORT).show()
                            enteredPin = ""
                        }"""
new_code = """                        if (enteredPin == selectedAccount?.pin) {
                            currentState = CheckBalanceState.LOADING
                        } else {
                            currentState = CheckBalanceState.WRONG_PIN
                        }"""

content = content.replace(old_code, new_code)

# Add CheckBalanceState.WRONG_PIN handler in the switch
wrong_pin_handler = """            CheckBalanceState.WRONG_PIN -> {
                WrongPinScreen(
                    bankName = selectedAccount?.bankName ?: "",
                    bankDesc = selectedAccount?.bankDesc ?: "",
                    onResetPin = { currentState = CheckBalanceState.PIN; enteredPin = "" },
                    onReEnterPin = { currentState = CheckBalanceState.PIN; enteredPin = "" },
                    onDone = { currentState = CheckBalanceState.LIST }
                )
            }
"""
content = content.replace('            CheckBalanceState.SUCCESS -> {', wrong_pin_handler + '            CheckBalanceState.SUCCESS -> {')

with open("app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt", "w") as f:
    f.write(content)
