import re

with open('app/src/main/java/com/example/ui/screens/ReceiptScreen.kt', 'r') as f:
    text = f.read()

target = """    fun shareTransaction() {
        val shareMsg = ""\"
            *PhonePe Transaction Receipt*
            ----------------------------------
            Status: ${currentTx.status}
            Received From: ${currentTx.receiverName}
            Phone: ${currentTx.receiverPhone}
            Amount: ₹${currentTx.amount.toInt()}
            Date: $formattedDate
            Txn ID: ${currentTx.transactionId}
            UTR: ${currentTx.utr}
            ----------------------------------
            Shared via PhonePe
        ""\".trimIndent()"""

replacement = """    fun shareTransaction() {
        val direction = if (currentTx.type == "PAID") "Paid To" else "Received From"
        val shareMsg = ""\"
            *PhonePe Transaction Receipt*
            ----------------------------------
            Status: ${currentTx.status}
            $direction: ${currentTx.receiverName}
            UPI ID / Phone: ${currentTx.receiverPhone}
            Amount: ₹${currentTx.amount.toInt()}
            Date: $formattedDate
            Txn ID: ${currentTx.transactionId}
            UTR: ${currentTx.utr}
            ----------------------------------
            Shared via PhonePe
        ""\".trimIndent()"""

text = text.replace(target, replacement)

with open('app/src/main/java/com/example/ui/screens/ReceiptScreen.kt', 'w') as f:
    f.write(text)
