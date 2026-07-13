import re

with open('app/src/main/java/com/example/ui/screens/ReceiptScreen.kt', 'r') as f:
    text = f.read()

target = """    LaunchedEffect(paymentState, tx) {
        val currentTx = tx
        if (paymentState == PaymentState.SUCCESS_ANIMATION && currentTx != null && currentTx.status == "SUCCESS") {
            val amountInt = currentTx.amount.toInt()
            val textToSpeak = "Received $amountInt rupees on PhonePe"
            tts?.speak(textToSpeak, TextToSpeech.QUEUE_FLUSH, null, "PhonePePrankTts")
        }
    }"""

replacement = """    LaunchedEffect(paymentState, tx) {
        val currentTx = tx
        if (paymentState == PaymentState.SUCCESS_ANIMATION && currentTx != null && currentTx.status == "SUCCESS") {
            if (currentTx.type != "PAID") {
                val amountInt = currentTx.amount.toInt()
                val textToSpeak = "Received $amountInt rupees on PhonePe"
                tts?.speak(textToSpeak, TextToSpeech.QUEUE_FLUSH, null, "PhonePePrankTts")
            }
        }
    }"""

text = text.replace(target, replacement)

with open('app/src/main/java/com/example/ui/screens/ReceiptScreen.kt', 'w') as f:
    f.write(text)
