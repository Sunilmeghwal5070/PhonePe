import re

with open('app/src/main/java/com/example/ui/screens/RechargeFlowScreens.kt', 'r') as f:
    content = f.read()

target = """fun RechargeProcessingScreen(
    name: String,
    amount: String,
    onSuccess: (Int) -> Unit
) {
    var step by remember { mutableStateOf(0) }

    LaunchedEffect(Unit) {
        delay(1500)
        step = 1
        delay(1500)
        onSuccess((1000000000..Int.MAX_VALUE).random()) // Random Transaction ID
    }"""

replacement = """fun RechargeProcessingScreen(
    name: String,
    amount: String,
    onSuccess: () -> Unit
) {
    var step by remember { mutableStateOf(0) }

    LaunchedEffect(Unit) {
        delay(1500)
        step = 1
        delay(1500)
        onSuccess()
    }"""

if target in content:
    content = content.replace(target, replacement)
    print("Replaced proc")
else:
    print("Not found")

with open('app/src/main/java/com/example/ui/screens/RechargeFlowScreens.kt', 'w') as f:
    f.write(content)

