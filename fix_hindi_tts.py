import re

with open('app/src/main/java/com/example/ui/screens/ReceiptScreen.kt', 'r') as f:
    text = f.read()

target = """                val amountInt = currentTx.amount.toInt()
                val textToSpeak = "Received $amountInt rupees on PhonePe"
                tts?.speak(textToSpeak, TextToSpeech.QUEUE_FLUSH, null, "PhonePePrankTts")"""

replacement = """                val amountInt = currentTx.amount.toInt()
                val textToSpeak = "PhonePe par, $amountInt rupaye, praapt hue."
                tts?.speak(textToSpeak, TextToSpeech.QUEUE_FLUSH, null, "PhonePePrankTts")"""

text = text.replace(target, replacement)

with open('app/src/main/java/com/example/ui/screens/ReceiptScreen.kt', 'w') as f:
    f.write(text)
