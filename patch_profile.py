import re

with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'r') as f:
    text = f.read()

target = """                var shakeEnabled by remember { mutableStateOf(false) }
                Switch(
                    checked = shakeEnabled,
                    onCheckedChange = { shakeEnabled = it },"""
replacement = """                val shakeEnabled by viewModel.isShakeEnabled.collectAsState()
                Switch(
                    checked = shakeEnabled,
                    onCheckedChange = { viewModel.setShakeEnabled(it) },"""

text = text.replace(target, replacement)

with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'w') as f:
    f.write(text)
