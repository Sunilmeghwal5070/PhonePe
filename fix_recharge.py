import re

with open('app/src/main/java/com/example/ui/screens/RechargeFlowScreens.kt', 'r') as f:
    content = f.read()

target_pin = """@Composable
fun RechargePinScreen(
    amount: String,
    bankId: String,
    viewModel: PrankViewModel,
    onBack: () -> Unit,
    onSuccess: () -> Unit
) {"""

replacement_pin = """@Composable
fun RechargePinScreen(
    amount: String,
    bankId: String,
    name: String,
    viewModel: PrankViewModel,
    onBack: () -> Unit,
    onSuccess: (Int) -> Unit
) {"""

if target_pin in content:
    content = content.replace(target_pin, replacement_pin)

target_submit = """                // Deduct balance
                account?.let { 
                    val currentBal = it.balance
                    val amt = amount.toDoubleOrNull() ?: 0.0
                    // viewModel.updateBankAccount(it.copy(balance = (currentBal - amt)))
                }
                onSuccess()"""

replacement_submit = """                // Deduct balance
                account?.let { 
                    // Let insertTransaction handle balance deduction
                    val amt = amount.toDoubleOrNull() ?: 0.0
                    viewModel.insertTransaction(
                        name = name,
                        phone = name, // using name as phone for now
                        upiId = "",
                        amount = amt,
                        status = "SUCCESS",
                        type = "RECHARGE",
                        bankName = it.bankName,
                        bankLast4 = it.bankDesc.takeLast(4),
                        customTxId = "NX26061723274381818502541",
                        customUtr = "201104189977",
                        timestamp = System.currentTimeMillis()
                    ) { txId ->
                        onSuccess(txId)
                    }
                } ?: run {
                    onSuccess(0)
                }"""

# Actually, wait! In existing RechargeFlowScreens, the original code is:
#                 // Deduct balance
#                 account?.let { 
#                     val currentBal = it.balance
#                     val amt = amount.toDoubleOrNull() ?: 0.0
#                     viewModel.updateBankAccount(it.copy(balance = (currentBal - amt)))
#                 }
#                 onSuccess()

content = content.replace("""                // Deduct balance
                account?.let { 
                    val currentBal = it.balance
                    val amt = amount.toDoubleOrNull() ?: 0.0
                    viewModel.updateBankAccount(it.copy(balance = (currentBal - amt)))
                }
                onSuccess()""", replacement_submit)

with open('app/src/main/java/com/example/ui/screens/RechargeFlowScreens.kt', 'w') as f:
    f.write(content)

