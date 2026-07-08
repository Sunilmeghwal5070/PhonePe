import re

# 1. Fix prefilledName -> payeeName in MainActivity.kt
with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()
content = content.replace("prefilledName = name,", "payeeName = name,")
with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

# 2. Fix receiverUpi -> receiverUpiId in CreatePrankScreen.kt
with open("app/src/main/java/com/example/ui/screens/CreatePrankScreen.kt", "r") as f:
    content = f.read()
content = content.replace("viewModel.selectedPayeeUpi = receiverUpi\n", "viewModel.selectedPayeeUpi = receiverUpiId\n")
with open("app/src/main/java/com/example/ui/screens/CreatePrankScreen.kt", "w") as f:
    f.write(content)

# 3. Add import for ArrowForward in ReceiptScreen.kt
with open("app/src/main/java/com/example/ui/screens/ReceiptScreen.kt", "r") as f:
    content = f.read()
if "import androidx.compose.material.icons.automirrored.filled.ArrowForward" not in content:
    content = content.replace("import androidx.compose.material.icons.automirrored.filled.ArrowBack", "import androidx.compose.material.icons.automirrored.filled.ArrowBack\nimport androidx.compose.material.icons.automirrored.filled.ArrowForward")
with open("app/src/main/java/com/example/ui/screens/ReceiptScreen.kt", "w") as f:
    f.write(content)

