import re

with open('app/src/main/java/com/example/ui/screens/RechargeFlowScreens.kt', 'r') as f:
    text = f.read()

text = text.replace("    onSuccess: () -> Unit", "    onSuccess: (Int) -> Unit")

with open('app/src/main/java/com/example/ui/screens/RechargeFlowScreens.kt', 'w') as f:
    f.write(text)

