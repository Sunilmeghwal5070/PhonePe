import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    text = f.read()

text = text.replace('composable("my_qr") {\n                QrScreen()\n            }', 'composable("my_qr") {\n                QrScreen(viewModel = prankViewModel, onBack = { navController.popBackStack() })\n            }')

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(text)

