import re

with open('app/src/main/java/com/example/ui/screens/RechargeFlowScreens.kt', 'r') as f:
    text = f.read()

target = """                        Row(modifier = Modifier.fillMaxWidth().padding(horizontal = 48.dp, vertical = 8.dp), horizontalArrangement = Arrangement.SpaceBetween) {
                            Column {
                                val details = getPlanDetails(currentTx.amount)"""

replacement = """                        Row(modifier = Modifier.fillMaxWidth().padding(horizontal = 48.dp, vertical = 8.dp), horizontalArrangement = Arrangement.SpaceBetween) {
                            val details = getPlanDetails(currentTx.amount)
                            Column {"""

text = text.replace(target, replacement)

with open('app/src/main/java/com/example/ui/screens/RechargeFlowScreens.kt', 'w') as f:
    f.write(text)
