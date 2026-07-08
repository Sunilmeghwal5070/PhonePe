import re

with open("app/src/main/java/com/example/ui/screens/CreatePrankScreen.kt", "r") as f:
    content = f.read()

# I need to find the onPinComplete handler
pattern = r"""val correctPin = selectedBank\?\.pin \?: "1234"\s*if \(enteredPin == correctPin\) \{"""

replacement = """val correctPin = selectedBank?.pin ?: "1234"
                if (enteredPin == correctPin) {
                    val finalAmount = amount.toDoubleOrNull() ?: 100.0
                    if (selectedBank != null && finalAmount > selectedBank!!.balance) {
                        showWrongPinScreen = true
                        // use a trick to pass the title, wait, I can just add a state for errorTitle
                        return@PinEntryScreen
                    }"""

content = re.sub(pattern, replacement, content)

with open("app/src/main/java/com/example/ui/screens/CreatePrankScreen.kt", "w") as f:
    f.write(content)
