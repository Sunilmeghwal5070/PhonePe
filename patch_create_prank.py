import re

with open("app/src/main/java/com/example/ui/screens/CreatePrankScreen.kt", "r") as f:
    content = f.read()

content = content.replace("showPinScreen = true", "viewModel.selectedPayeeUpi = receiverUpi\n                    showPinScreen = true")

with open("app/src/main/java/com/example/ui/screens/CreatePrankScreen.kt", "w") as f:
    f.write(content)
