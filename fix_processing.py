import re

with open('app/src/main/java/com/example/ui/screens/RechargeFlowScreens.kt', 'r') as f:
    text = f.read()

target = """fun RechargeProcessingScreen(
    name: String,
    amount: String,
    onSuccess: (Int) -> Unit
)"""
replacement = """fun RechargeProcessingScreen(
    name: String,
    amount: String,
    onSuccess: () -> Unit
)"""

text = text.replace(target, replacement)

with open('app/src/main/java/com/example/ui/screens/RechargeFlowScreens.kt', 'w') as f:
    f.write(text)

