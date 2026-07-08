import re

with open('app/src/main/java/com/example/ui/screens/ReceiptScreen.kt', 'r') as f:
    content = f.read()

target = """    when (paymentState) {
        PaymentState.PROCESSING -> {"""

replacement = """    if (paymentState == PaymentState.RECEIPT_DETAILS && currentTx.type == "RECHARGE") {
        RechargeSuccessScreen(transactionId = transactionId, viewModel = viewModel, onDone = onDone)
        return
    }

    when (paymentState) {
        PaymentState.PROCESSING -> {"""

if target in content:
    content = content.replace(target, replacement)
    print("Replaced render logic!")

with open('app/src/main/java/com/example/ui/screens/ReceiptScreen.kt', 'w') as f:
    f.write(content)

