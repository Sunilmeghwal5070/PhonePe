import re

with open('app/src/main/java/com/example/ui/screens/ReceiptScreen.kt', 'r') as f:
    content = f.read()

# Replace the broken lines
content = re.sub(
    r'ReceiptActionButton\(icon = Icons.AutoMirrored.Filled.CallMade, label = "Send\\nMoney"',
    r'ReceiptActionButton(icon = Icons.AutoMirrored.Filled.CallMade, label = "Send\\nMoney", onClick = { onDone() })',
    content
)
content = re.sub(
    r'ReceiptActionButton\(icon = Icons.Default.AccountBalance, label = "Check\\nBalance"',
    r'ReceiptActionButton(icon = Icons.Default.AccountBalance, label = "Check\\nBalance", onClick = {})',
    content
)
content = re.sub(
    r'ReceiptActionButton\(icon = Icons.Default.Schedule, label = "View\\nHistory"',
    r'ReceiptActionButton(icon = Icons.Default.Schedule, label = "View\\nHistory", onClick = { onDone() })',
    content
)
content = re.sub(
    r'ReceiptActionButton\(icon = Icons.Default.Share, label = "Share\\nReceipt"',
    r'ReceiptActionButton(icon = Icons.Default.Share, label = "Share\\nReceipt", onClick = { shareTransaction() })',
    content
)

with open('app/src/main/java/com/example/ui/screens/ReceiptScreen.kt', 'w') as f:
    f.write(content)
