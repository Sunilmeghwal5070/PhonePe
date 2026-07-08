import re

with open('/app/applet/app/src/main/java/com/example/ui/screens/AccountDetailsScreen.kt', 'r') as f:
    content = f.read()

# 1. Add `pin` variable
content = content.replace(
'''    var balance by remember { mutableStateOf(account?.balance ?: "Balance: ₹----") }''',
'''    var balance by remember { mutableStateOf(account?.balance ?: "Balance: ₹----") }
    var pin by remember { mutableStateOf(account?.pin ?: "1234") }''')

# 2. Add `pin = pin` to the save block
content = content.replace(
'''                                    type = accType,
                                    branch = branch,
                                    ifsc = ifsc,
                                    balance = balance
                                ))''',
'''                                    type = accType,
                                    branch = branch,
                                    ifsc = ifsc,
                                    balance = balance,
                                    pin = pin
                                ))''')

# 3. Add a visual field for editing PIN where the static text is
content = content.replace(
'''Text("UPI PIN", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.Black)
                        Text("4 digit UPI PIN exists", fontSize = 14.sp, color = Color.Gray)''',
'''Text("UPI PIN", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.Black)
                        if (isEditable) {
                            BasicTextField(
                                value = pin,
                                onValueChange = { if (it.length <= 4) pin = it },
                                textStyle = TextStyle(fontSize = 14.sp, color = Color.Gray)
                            )
                        } else {
                            Text("4 digit UPI PIN exists", fontSize = 14.sp, color = Color.Gray)
                        }'''
)

with open('/app/applet/app/src/main/java/com/example/ui/screens/AccountDetailsScreen.kt', 'w') as f:
    f.write(content)

