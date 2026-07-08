import re

with open('/app/applet/app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt', 'r') as f:
    content = f.read()

# PinEntryScreen modifications
old_pin_entry_sig = "fun PinEntryScreen(pin: String, onPinChange: (String) -> Unit, onSubmit: () -> Unit) {"
new_pin_entry_sig = "fun PinEntryScreen(bankName: String, actionText: String, pin: String, onPinChange: (String) -> Unit, onSubmit: () -> Unit) {"
content = content.replace(old_pin_entry_sig, new_pin_entry_sig)

content = content.replace(
'''            Column {
                Text("Canara Bank", fontSize = 18.sp, color = Color.Black)
                Text("XXXXXXXX0513", fontSize = 16.sp, color = Color.Black)
            }''',
'''            Column {
                Text(bankName, fontSize = 18.sp, color = Color.Black)
            }'''
)

content = content.replace(
'''        // Gray Check Balance Bar
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .background(Color(0xFFEEEEEE))
                .padding(horizontal = 16.dp, vertical = 8.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text("Check Balance", fontSize = 16.sp, color = Color.Gray)
            Icon(Icons.Default.KeyboardArrowDown, contentDescription = null, tint = Color.Black)
        }''',
'''        // Action Text Bar
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .background(Color(0xFFEEEEEE))
                .padding(horizontal = 16.dp, vertical = 8.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(actionText, fontSize = 16.sp, color = Color.Gray)
            Icon(Icons.Default.KeyboardArrowDown, contentDescription = null, tint = Color.Black)
        }'''
)

# Update PinEntryScreen call in CheckBalanceScreen
old_pin_call = '''            CheckBalanceState.PIN -> {
                val context = LocalContext.current
                PinEntryScreen(
                    pin = enteredPin,
                    onPinChange = { newPin -> enteredPin = newPin },
                    onSubmit = { 
                        if (enteredPin == selectedAccount?.pin) {
                            currentState = CheckBalanceState.LOADING
                        } else {
                            Toast.makeText(context, "Incorrect UPI PIN", Toast.LENGTH_SHORT).show()
                            enteredPin = ""
                        }
                    }
                )
            }'''
new_pin_call = '''            CheckBalanceState.PIN -> {
                val context = LocalContext.current
                PinEntryScreen(
                    bankName = selectedAccount?.bankName ?: "Bank",
                    actionText = "Check Balance",
                    pin = enteredPin,
                    onPinChange = { newPin -> enteredPin = newPin },
                    onSubmit = { 
                        if (enteredPin == selectedAccount?.pin) {
                            currentState = CheckBalanceState.LOADING
                        } else {
                            Toast.makeText(context, "Incorrect UPI PIN", Toast.LENGTH_SHORT).show()
                            enteredPin = ""
                        }
                    }
                )
            }'''
content = content.replace(old_pin_call, new_pin_call)

with open('/app/applet/app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt', 'w') as f:
    f.write(content)
