import re

with open('app/src/main/java/com/example/ui/screens/ReceiptScreen.kt', 'r') as f:
    content = f.read()

target = """    LaunchedEffect(tx) {
        val currentTx = tx
        if (currentTx != null) {
            val isOldTx = skipAnimation || (System.currentTimeMillis() - currentTx.timestamp) > 60000 // 1 minute
            if (isOldTx) {
                paymentState = PaymentState.RECEIPT_DETAILS
            } else {
                paymentState = PaymentState.PROCESSING
                delay(1800) // Processing delay
                if (currentTx.status == "SUCCESS") {
                    paymentState = PaymentState.SUCCESS_ANIMATION
                    delay(2600) // Success screen celebration delay
                }
                paymentState = PaymentState.RECEIPT_DETAILS
            }
        }
    }"""

replacement = """    LaunchedEffect(tx) {
        val currentTx = tx
        if (currentTx != null) {
            val isOldTx = skipAnimation || (System.currentTimeMillis() - currentTx.timestamp) > 60000 // 1 minute
            if (isOldTx || currentTx.type == "RECHARGE") {
                paymentState = PaymentState.RECEIPT_DETAILS
            } else {
                paymentState = PaymentState.PROCESSING
                delay(1800) // Processing delay
                if (currentTx.status == "SUCCESS") {
                    paymentState = PaymentState.SUCCESS_ANIMATION
                    delay(2600) // Success screen celebration delay
                }
                paymentState = PaymentState.RECEIPT_DETAILS
            }
        }
    }"""

content = content.replace(target, replacement)

target_render = """    val currentTx = tx
    if (currentTx == null) {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            CircularProgressIndicator()
        }
        return
    }

    val sdf = SimpleDateFormat("hh:mm a 'on' dd MMM yyyy", Locale.getDefault())
    val formattedDate = sdf.format(Date(currentTx.timestamp))

    when (paymentState) {"""

# Wait, `val currentTx = tx` is inside the `Box` or `Column`? Let's check `ReceiptScreen.kt`.
