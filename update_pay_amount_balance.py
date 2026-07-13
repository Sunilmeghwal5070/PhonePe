import re

with open('app/src/main/java/com/example/ui/screens/PayAmountScreen.kt', 'r') as f:
    text = f.read()

target = """                Button(
                    onClick = { 
                        showBottomSheet = false
                        onProceed(amount, currentSelectedBank)
                    },"""

replacement = """                val context = androidx.compose.ui.platform.LocalContext.current
                Button(
                    onClick = { 
                        val payAmount = amount.toDoubleOrNull() ?: 0.0
                        if (payAmount > currentSelectedBank.balance) {
                            android.widget.Toast.makeText(context, "Insufficient balance", android.widget.Toast.LENGTH_SHORT).show()
                        } else {
                            showBottomSheet = false
                            onProceed(amount, currentSelectedBank)
                        }
                    },"""

text = text.replace(target, replacement)

with open('app/src/main/java/com/example/ui/screens/PayAmountScreen.kt', 'w') as f:
    f.write(text)
