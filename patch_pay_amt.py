with open('/app/applet/app/src/main/java/com/example/ui/screens/PayAmountScreen.kt', 'r') as f:
    content = f.read()

old_sig = '''fun PayAmountScreen(
    viewModel: PrankViewModel,
    prefilledName: String = "YASHWANT MEGHWAL",
    onBack: () -> Unit,
    onProceed: (String, BankAccount) -> Unit
) {
    var amount by remember { mutableStateOf("") }'''
new_sig = '''fun PayAmountScreen(
    viewModel: PrankViewModel,
    prefilledName: String = "YASHWANT MEGHWAL",
    prefilledAmount: String = "",
    onBack: () -> Unit,
    onProceed: (String, BankAccount) -> Unit
) {
    var amount by remember { mutableStateOf(prefilledAmount) }'''

content = content.replace(old_sig, new_sig)

with open('/app/applet/app/src/main/java/com/example/ui/screens/PayAmountScreen.kt', 'w') as f:
    f.write(content)
