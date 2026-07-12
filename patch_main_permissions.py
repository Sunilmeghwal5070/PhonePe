import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    text = f.read()

onCreate_pattern = r'override fun onCreate\(savedInstanceState: Bundle\?\) \{\n\s*super\.onCreate\(savedInstanceState\)'
onCreate_replacement = """override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        com.example.ui.NotificationHelper.createNotificationChannel(this)
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.TIRAMISU) {
            if (androidx.core.content.ContextCompat.checkSelfPermission(this, android.Manifest.permission.POST_NOTIFICATIONS) != android.content.pm.PackageManager.PERMISSION_GRANTED) {
                androidx.core.app.ActivityCompat.requestPermissions(this, arrayOf(android.Manifest.permission.POST_NOTIFICATIONS), 101)
            }
        }"""

text = re.sub(onCreate_pattern, onCreate_replacement, text)

# Find insertTransaction in PaymentProcessingScreen callback
tx_pattern = r'prankViewModel\.insertTransaction\(\s*name = name,\s*phone = "9876543210",\s*upiId = "krishna88750@axl",\s*amount = amount\.toDoubleOrNull\(\) \?: 100\.0,\s*status = "SUCCESS",\s*bankName = selectedBank\?\.bankName \?: "State Bank of India",\s*bankLast4 = selectedBank\?\.bankDesc\?\.takeLast\(4\) \?: "0365",\s*customTxId = "",\s*customUtr = "",\s*timestamp = System\.currentTimeMillis\(\),\s*isRecharge = false\s*\)'
tx_replacement = """val amt = amount.toDoubleOrNull() ?: 100.0
                        val bName = selectedBank?.bankName ?: "State Bank of India"
                        val bLast4 = selectedBank?.bankDesc?.takeLast(4) ?: "0365"
                        prankViewModel.insertTransaction(
                            name = name,
                            phone = "9876543210",
                            upiId = "krishna88750@axl",
                            amount = amt,
                            status = "SUCCESS",
                            bankName = bName,
                            bankLast4 = bLast4,
                            customTxId = "",
                            customUtr = "",
                            timestamp = System.currentTimeMillis(),
                            isRecharge = false
                        )
                        com.example.ui.NotificationHelper.showBankSmsNotification(this@MainActivity, amt, bLast4, name, bName)"""

text = re.sub(tx_pattern, tx_replacement, text)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(text)

