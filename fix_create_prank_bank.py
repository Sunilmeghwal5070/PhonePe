import re

with open('app/src/main/java/com/example/ui/screens/CreatePrankScreen.kt', 'r') as f:
    text = f.read()

target = """    val bankAccounts by viewModel.bankAccounts.collectAsState()
    var selectedBank by remember(bankAccounts) { mutableStateOf(bankAccounts.firstOrNull()) }
    var senderBankName by remember(selectedBank) { mutableStateOf(selectedBank?.bankName ?: "State Bank of India") }
    var senderBankLast4 by remember(selectedBank) { mutableStateOf(selectedBank?.bankDesc?.takeLast(4) ?: (1000..9999).random().toString()) }"""

replacement = """    val bankAccounts by viewModel.bankAccounts.collectAsState()
    var selectedBank by remember { mutableStateOf(bankAccounts.firstOrNull()) }
    var senderBankName by remember { mutableStateOf(selectedBank?.bankName ?: "State Bank of India") }
    var senderBankLast4 by remember { mutableStateOf(selectedBank?.bankDesc?.takeLast(4) ?: (1000..9999).random().toString()) }

    LaunchedEffect(bankAccounts) {
        if (selectedBank == null && bankAccounts.isNotEmpty()) {
            selectedBank = bankAccounts.first()
            senderBankName = bankAccounts.first().bankName
            senderBankLast4 = bankAccounts.first().bankDesc.takeLast(4)
        }
    }"""

text = text.replace(target, replacement)

# Update dropdown to correctly set all three when a bank is manually selected
target_dropdown = """                                    onClick = {
                                        senderBankName = bank
                                        selectedBank = bankAccounts.find { it.bankName == bank }
                                        showBankDropdown = false
                                    }"""

replacement_dropdown = """                                    onClick = {
                                        val newBank = bankAccounts.find { it.bankName == bank }
                                        if (newBank != null) {
                                            selectedBank = newBank
                                            senderBankName = newBank.bankName
                                            senderBankLast4 = newBank.bankDesc.takeLast(4)
                                        }
                                        showBankDropdown = false
                                    }"""
text = text.replace(target_dropdown, replacement_dropdown)

with open('app/src/main/java/com/example/ui/screens/CreatePrankScreen.kt', 'w') as f:
    f.write(text)
