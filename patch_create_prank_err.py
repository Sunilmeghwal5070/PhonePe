import re

with open("app/src/main/java/com/example/ui/screens/CreatePrankScreen.kt", "r") as f:
    content = f.read()

content = content.replace("var showWrongPinScreen by remember { mutableStateOf(false) }", "var showWrongPinScreen by remember { mutableStateOf(false) }\n    var pinErrorTitle by remember { mutableStateOf(\"Payment failed\") }")

content = content.replace("showWrongPinScreen = true", "showWrongPinScreen = true; pinErrorTitle = \"Payment failed\"")
content = content.replace('errorTitle = "Payment failed"', 'errorTitle = pinErrorTitle')
content = content.replace('if (selectedBank != null && finalAmount > selectedBank!!.balance) {\n                        showWrongPinScreen = true; pinErrorTitle = "Payment failed"\n                        // use a trick to pass the title, wait, I can just add a state for errorTitle\n                        return@PinEntryScreen\n                    }', 'if (selectedBank != null && finalAmount > selectedBank!!.balance) {\n                        pinErrorTitle = "Insufficient Balance"\n                        showWrongPinScreen = true\n                        return@PinEntryScreen\n                    }')

with open("app/src/main/java/com/example/ui/screens/CreatePrankScreen.kt", "w") as f:
    f.write(content)
