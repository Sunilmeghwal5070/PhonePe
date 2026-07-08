with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    lines = f.readlines()

insert_index = 0
for i, line in enumerate(lines):
    if "@Composable" in line and "fun TransferButton" in lines[i+1]:
        insert_index = i
        break

dialog_code = """
    if (showRechargeReminder) {
        RechargeReminderDialog(
            phoneNumber = "887596642",
            onDismiss = {
                showRechargeReminder = false
                viewModel.hasShownRechargeReminder = true
            },
            onRecharge = {
                showRechargeReminder = false
                viewModel.hasShownRechargeReminder = true
                onNavigateToMobileRecharge()
            }
        )
    }
"""

# The closing brace for HomeScreen is at insert_index - 1
lines.insert(insert_index - 1, dialog_code)

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.writelines(lines)
