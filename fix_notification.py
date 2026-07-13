import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    text = f.read()

target = """                        // Insert transaction
                        prankViewModel.insertTransaction(
                            name = name,
                            phone = "9876543210",
                            upiId = "krishna88750@axl",
                            amount = amount.toDoubleOrNull() ?: 100.0,
                            status = "SUCCESS",
                            bankName = selectedBank?.bankName ?: "State Bank of India",
                            bankLast4 = selectedBank?.bankDesc?.takeLast(4) ?: "0365",
                            customTxId = "",
                            customUtr = "",
                            timestamp = System.currentTimeMillis(),
                            onSuccess = { insertedId ->
                                navController.navigate("pay_success/$amount/$insertedId/${Uri.encode(name)}") {"""

replacement = """                        // Insert transaction
                        val parsedAmount = amount.toDoubleOrNull() ?: 100.0
                        val resolvedBankName = selectedBank?.bankName ?: "State Bank of India"
                        val resolvedBankLast4 = selectedBank?.bankDesc?.takeLast(4) ?: "0365"
                        
                        com.example.ui.NotificationHelper.showBankSmsNotification(
                            context = context,
                            amount = parsedAmount,
                            bankLast4 = resolvedBankLast4,
                            payeeName = name,
                            bankName = resolvedBankName
                        )
                        
                        prankViewModel.insertTransaction(
                            name = name,
                            phone = "9876543210",
                            upiId = "krishna88750@axl",
                            amount = parsedAmount,
                            status = "SUCCESS",
                            bankName = resolvedBankName,
                            bankLast4 = resolvedBankLast4,
                            customTxId = "",
                            customUtr = "",
                            timestamp = System.currentTimeMillis(),
                            onSuccess = { insertedId ->
                                navController.navigate("pay_success/$amount/$insertedId/${Uri.encode(name)}") {"""

text = text.replace(target, replacement)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(text)
