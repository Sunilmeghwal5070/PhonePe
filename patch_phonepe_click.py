with open('/app/applet/app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    content = f.read()

target = """                        Column(
                            horizontalAlignment = Alignment.CenterHorizontally,
                            modifier = Modifier
                                .width(80.dp)
                                .clickable {
                                    showDialogTitle = "PhonePe Wallet 💳"
                                    showDialogText = "You have a fictional ₹15,000 in your wallet which increases when you shop! 😎"
                                }
                        ) {"""

replacement = """                        Column(
                            horizontalAlignment = Alignment.CenterHorizontally,
                            modifier = Modifier
                                .width(80.dp)
                        ) {"""

content = content.replace(target, replacement)

with open('/app/applet/app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(content)
