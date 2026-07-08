import re

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

# First, fix the var showRechargeReminder
if "var showRechargeReminder" not in content:
    content = content.replace("var showDialogTitle by remember { mutableStateOf<String?>(null) }", "var showDialogTitle by remember { mutableStateOf<String?>(null) }\n    var showRechargeReminder by remember { mutableStateOf(!viewModel.hasShownRechargeReminder) }")

# Now, find the end of the HomeScreen function (right before @Composable fun TransferButton)
# Let's remove any garbage between "Paid successfully! ✅" block and "@Composable fun TransferButton"
pattern = r"""Text\("Paid successfully! ✅", color = Color\.White\)\s*\}\s*\}\s*\)\s*\}\s*\}.*?@Composable\s*fun TransferButton"""

replacement = """Text("Paid successfully! ✅", color = Color.White)
                }
            }
        )
    }

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

@Composable
fun TransferButton"""

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
