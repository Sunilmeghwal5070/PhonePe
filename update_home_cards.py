import re

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    text = f.read()

target = """                // Left Capsule Card
                Card(
                    modifier = Modifier
                        .weight(1f)
                        .clickable {
                            Toast.makeText(context, "Silver Savings opening...", Toast.LENGTH_SHORT).show()
                        },"""
replacement = """                // Left Capsule Card
                Card(
                    modifier = Modifier
                        .weight(1f)
                        .height(52.dp)
                        .clickable {
                            Toast.makeText(context, "Silver Savings opening...", Toast.LENGTH_SHORT).show()
                        },"""

text = text.replace(target, replacement)

target2 = """                // Right Capsule Card
                Card(
                    modifier = Modifier
                        .weight(1f)
                        .clickable {
                            Toast.makeText(context, "Opening share.market...", Toast.LENGTH_SHORT).show()
                        },"""
replacement2 = """                // Right Capsule Card
                Card(
                    modifier = Modifier
                        .weight(1f)
                        .height(52.dp)
                        .clickable {
                            Toast.makeText(context, "Opening share.market...", Toast.LENGTH_SHORT).show()
                        },"""

text = text.replace(target2, replacement2)

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(text)
