with open('/app/applet/app/src/main/java/com/example/ui/screens/AccountDetailsScreen.kt', 'r') as f:
    content = f.read()

old_pin_toggle = '''Text(if (isEditingPin) "DONE" else "CHANGE", color = Color(0xFF5f259f), fontWeight = FontWeight.Bold, fontSize = 14.sp, modifier = Modifier.clickable { isEditingPin = !isEditingPin })'''
new_pin_toggle = '''Text(if (isEditingPin) "DONE" else "CHANGE", color = Color(0xFF5f259f), fontWeight = FontWeight.Bold, fontSize = 14.sp, modifier = Modifier.clickable { 
                            if (isEditingPin) {
                                if (account != null) {
                                    viewModel.updateBankAccount(account.copy(pin = pin))
                                }
                            }
                            isEditingPin = !isEditingPin 
                        })'''

if old_pin_toggle in content:
    content = content.replace(old_pin_toggle, new_pin_toggle)

with open('/app/applet/app/src/main/java/com/example/ui/screens/AccountDetailsScreen.kt', 'w') as f:
    f.write(content)
