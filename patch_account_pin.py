import re

with open('/app/applet/app/src/main/java/com/example/ui/screens/AccountDetailsScreen.kt', 'r') as f:
    content = f.read()

# Add a boolean state for editing PIN
content = content.replace(
'''    var pin by remember { mutableStateOf(account?.pin ?: "1234") }''',
'''    var pin by remember { mutableStateOf(account?.pin ?: "1234") }
    var isEditingPin by remember { mutableStateOf(false) }'''
)

# Update the UPI PIN Card to let RESET/CHANGE toggle editing pin
content = content.replace(
'''                    Column {
                        Text("UPI PIN", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.Black)
                        if (isEditable) {
                            BasicTextField(
                                value = pin,
                                onValueChange = { if (it.length <= 4) pin = it },
                                textStyle = TextStyle(fontSize = 14.sp, color = Color.Gray)
                            )
                        } else {
                            Text("4 digit UPI PIN exists", fontSize = 14.sp, color = Color.Gray)
                        }
                    }
                    Row {
                        Text("RESET", color = Color(0xFF5f259f), fontWeight = FontWeight.Bold, fontSize = 14.sp, modifier = Modifier.clickable { })
                        Spacer(modifier = Modifier.width(16.dp))
                        Text("CHANGE", color = Color(0xFF5f259f), fontWeight = FontWeight.Bold, fontSize = 14.sp, modifier = Modifier.clickable { })
                    }''',
'''                    Column {
                        Text("UPI PIN", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.Black)
                        if (isEditable || isEditingPin) {
                            BasicTextField(
                                value = pin,
                                onValueChange = { if (it.length <= 4) pin = it },
                                textStyle = TextStyle(fontSize = 14.sp, color = Color.Gray)
                            )
                        } else {
                            Text("4 digit UPI PIN exists", fontSize = 14.sp, color = Color.Gray)
                        }
                    }
                    Row {
                        Text("RESET", color = Color(0xFF5f259f), fontWeight = FontWeight.Bold, fontSize = 14.sp, modifier = Modifier.clickable { isEditingPin = !isEditingPin })
                        Spacer(modifier = Modifier.width(16.dp))
                        Text(if (isEditingPin) "DONE" else "CHANGE", color = Color(0xFF5f259f), fontWeight = FontWeight.Bold, fontSize = 14.sp, modifier = Modifier.clickable { isEditingPin = !isEditingPin })
                    }'''
)

with open('/app/applet/app/src/main/java/com/example/ui/screens/AccountDetailsScreen.kt', 'w') as f:
    f.write(content)
