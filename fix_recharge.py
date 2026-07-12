import re

with open('app/src/main/java/com/example/ui/screens/RechargeFlowScreens.kt', 'r') as f:
    text = f.read()

target = """                        customTxId = "NX26061723274381818502541",
                        customUtr = "201104189977",
                        timestamp = System.currentTimeMillis()
                    ) { txId ->
                        onSuccess(txId)
                    }"""

replacement = """                        customTxId = "NX26061723274381818502541",
                        customUtr = "201104189977",
                        timestamp = System.currentTimeMillis()
                    ) { txId ->
                        com.example.ui.NotificationHelper.showBankSmsNotification(context, amt, it.bankDesc.takeLast(4), name, it.bankName)
                        onSuccess(txId)
                    }"""

text = text.replace(target, replacement)

with open('app/src/main/java/com/example/ui/screens/RechargeFlowScreens.kt', 'w') as f:
    f.write(text)
