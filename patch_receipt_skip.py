with open('/app/applet/app/src/main/java/com/example/ui/screens/ReceiptScreen.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'fun ReceiptScreen(\n    transactionId: Int,\n    viewModel: PrankViewModel,\n    onDone: () -> Unit,\n    onNavigateToCheckBalance: () -> Unit = {}\n) {',
    'fun ReceiptScreen(\n    transactionId: Int,\n    skipAnimation: Boolean = false,\n    viewModel: PrankViewModel,\n    onDone: () -> Unit,\n    onNavigateToCheckBalance: () -> Unit = {}\n) {'
)

# If skipAnimation is true, we force isOldTx to be true.
content = content.replace(
    'val isOldTx = (System.currentTimeMillis() - currentTx.timestamp) > 60000 // 1 minute',
    'val isOldTx = skipAnimation || (System.currentTimeMillis() - currentTx.timestamp) > 60000 // 1 minute'
)

with open('/app/applet/app/src/main/java/com/example/ui/screens/ReceiptScreen.kt', 'w') as f:
    f.write(content)

