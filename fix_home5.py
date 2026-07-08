with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

import re

# Remove the broken remainder of the dialog
content = re.sub(r"""            onRecharge = \{[\s\S]*?    \}""", "", content)

# Now, we need to insert the dialog block at the end of HomeScreen correctly.
# The end of HomeScreen is the first instance of "}\n}\n\n@Composable\nfun TransferButton"
# Wait, let's just find "fun TransferButton" and insert before its "@Composable"

dialog_block = """
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
}
"""

content = content.replace("    }\n}\n@Composable\nfun TransferButton", dialog_block + "\n@Composable\nfun TransferButton")

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
