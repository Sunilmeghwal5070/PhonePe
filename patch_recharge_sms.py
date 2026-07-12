import re

with open('app/src/main/java/com/example/ui/screens/RechargeFlowScreens.kt', 'r') as f:
    text = f.read()

target = """                        type = "RECHARGE",
                        bankName = it.bankName,
                        bankLast4 = it.bankDesc.takeLast(4),
                        customTxId = "NX26061723274381818502541",
                        customUtr = "201104189977",
                        timestamp = System.currentTimeMillis(),
                        isRecharge = true
                    )
                    onRechargeSuccess()"""

replacement = """                        type = "RECHARGE",
                        bankName = it.bankName,
                        bankLast4 = it.bankDesc.takeLast(4),
                        customTxId = "NX26061723274381818502541",
                        customUtr = "201104189977",
                        timestamp = System.currentTimeMillis(),
                        isRecharge = true
                    )
                    com.example.ui.NotificationHelper.showBankSmsNotification(context, amt, it.bankDesc.takeLast(4), name, it.bankName)
                    onRechargeSuccess()"""

text = text.replace(target, replacement)

# We need to ensure `val context = LocalContext.current` is defined
if "val context = LocalContext.current" not in text:
    text = text.replace("fun RechargePinScreen(", "fun RechargePinScreen(\n    val context = androidx.compose.ui.platform.LocalContext.current\n")
else:
    # let's be more specific
    func_pattern = r'fun RechargePinScreen\(.*?\) \{'
    new_func = """fun RechargePinScreen(
    viewModel: com.example.ui.PrankViewModel,
    name: String,
    amount: String,
    accountId: String,
    onBack: () -> Unit,
    onRechargeSuccess: () -> Unit
) {
    val context = androidx.compose.ui.platform.LocalContext.current"""
    text = re.sub(func_pattern, new_func, text, count=1, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/RechargeFlowScreens.kt', 'w') as f:
    f.write(text)

