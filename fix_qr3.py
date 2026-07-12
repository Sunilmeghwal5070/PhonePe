import re

with open('app/src/main/java/com/example/ui/screens/QrScreen.kt', 'r') as f:
    text = f.read()

# Remove the incorrectly placed import
text = text.replace("import com.example.ui.PrankViewModel\nfun QrScreen", "fun QrScreen")
# And put it at the top
text = text.replace("package com.example.ui.screens\n\n", "package com.example.ui.screens\n\nimport com.example.ui.PrankViewModel\n")

# Wait, the other errors:
# @Composable invocations can only happen from the context of a @Composable function
# This means I replaced the `val upiId = "sunilmeghwal6367@ybl"` with the block, but I didn't verify the structure.
