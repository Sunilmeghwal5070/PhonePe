with open('/app/applet/app/src/main/java/com/example/ui/screens/PayAmountScreen.kt', 'r') as f:
    content = f.read()

old_pay_sig = '''fun PayAmountScreen(
    viewModel: PrankViewModel,
    onBack: () -> Unit,
    onProceed: (String, BankAccount) -> Unit
) {
    var amount by remember { mutableStateOf("") }'''
new_pay_sig = '''fun PayAmountScreen(
    viewModel: PrankViewModel,
    prefilledName: String = "Karishna Karishna",
    prefilledAmount: String = "",
    onBack: () -> Unit,
    onProceed: (String, BankAccount) -> Unit
) {
    var amount by remember { mutableStateOf(prefilledAmount) }'''

content = content.replace(old_pay_sig, new_pay_sig)

# We also need to change payeeName to prefilledName if it's hardcoded
if 'payeeName' in content and 'prefilledName' not in content:
    content = content.replace('payeeName = "Karishna Karishna"', '')
    content = content.replace('val payeeName = "Karishna Karishna"', '')
    content = content.replace('payeeName', 'prefilledName')
elif 'val payeeName' in content:
    content = content.replace('val payeeName = "Karishna Karishna"\n', '')
    content = content.replace('payeeName', 'prefilledName')

with open('/app/applet/app/src/main/java/com/example/ui/screens/PayAmountScreen.kt', 'w') as f:
    f.write(content)
