import re

with open("app/src/main/java/com/example/ui/screens/ReceiptScreen.kt", "r") as f:
    content = f.read()

# I need to add PrankViewModel to ReceiptScreen parameters
if "viewModel: PrankViewModel" not in content:
    content = content.replace("fun ReceiptScreen(", "fun ReceiptScreen(\n    viewModel: com.example.ui.PrankViewModel,")
    content = content.replace("    val context = LocalContext.current", "    val context = LocalContext.current\n    val userProfile by viewModel.userProfileManager.userProfile.androidx.compose.runtime.collectAsState()")

# Replace XXXXXX${currentTx.senderBankAccountLast4} with the user's profile name!
old_name = 'Text(if (currentTx.type == "PAID") "XXXXXXX${currentTx.senderBankAccountLast4}" else "XXXXXXX${currentTx.receiverPhone.takeLast(4)}", fontSize = 15.sp, color = Color.DarkGray)'
new_name = 'Text(if (currentTx.type == "PAID") userProfile.name else currentTx.receiverName, fontSize = 15.sp, color = Color.DarkGray)'
content = content.replace(old_name, new_name)

with open("app/src/main/java/com/example/ui/screens/ReceiptScreen.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    main = f.read()

main = main.replace("                        ReceiptScreen(", "                        ReceiptScreen(\n                            viewModel = viewModel,")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(main)
