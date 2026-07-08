with open('/app/applet/app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    content = f.read()

old_sig = '''fun HomeScreen(
    viewModel: PrankViewModel,
    onCreatePrank: () -> Unit,
    onNavigateToReceipt: (Int) -> Unit,
    onNavigateToQr: () -> Unit = {},
    onNavigateToCheckBalance: () -> Unit = {},
    onNavigateToProfile: () -> Unit = {}
) {'''
new_sig = '''fun HomeScreen(
    viewModel: PrankViewModel,
    onCreatePrank: () -> Unit,
    onNavigateToReceipt: (Int) -> Unit,
    onNavigateToQr: () -> Unit = {},
    onNavigateToCheckBalance: () -> Unit = {},
    onNavigateToProfile: () -> Unit = {},
    onNavigateToContactList: () -> Unit = {}
) {'''

content = content.replace(old_sig, new_sig)

old_mobile = '''                        TransferButton(
                            icon = Icons.Default.PhoneAndroid,
                            label = "To Mobile\\nNumber",
                            onClick = onCreatePrank
                        )'''
new_mobile = '''                        TransferButton(
                            icon = Icons.Default.PhoneAndroid,
                            label = "To Mobile\\nNumber",
                            onClick = onNavigateToContactList
                        )'''
content = content.replace(old_mobile, new_mobile)

with open('/app/applet/app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(content)
