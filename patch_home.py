import re

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

pattern_vars = r"""    var showDialogText by remember \{ mutableStateOf<String\?>\(null\) \}
    var showDialogTitle by remember \{ mutableStateOf<String\?>\(null\) \}"""
replacement_vars = """    var showDialogText by remember { mutableStateOf<String?>(null) }
    var showDialogTitle by remember { mutableStateOf<String?>(null) }
    
    var showRechargeReminder by remember { mutableStateOf(!viewModel.hasShownRechargeReminder) }"""
content = re.sub(pattern_vars, replacement_vars, content)

pattern_end = r"""            \}
        \}
    \}
\}"""
replacement_end = """            }
        }
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
}"""
# Wait, let's just append at the very end of HomeScreen
content = content[:content.rfind("}")].strip() + """
    
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
}"""

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
