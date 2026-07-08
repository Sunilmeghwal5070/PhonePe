import re

with open('/app/applet/app/src/main/java/com/example/ui/screens/CreatePrankScreen.kt', 'r') as f:
    content = f.read()

# Add collectAsState
content = content.replace(
'''import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue''',
'''import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.runtime.collectAsState
import android.widget.Toast
import androidx.compose.ui.platform.LocalContext''')

# Use bankAccounts in CreatePrankScreen
content = content.replace(
'''    var senderBankName by remember { mutableStateOf("State Bank of India") }
    var senderBankLast4 by remember { mutableStateOf((1000..9999).random().toString()) }''',
'''    val bankAccounts by viewModel.bankAccounts.collectAsState()
    var selectedBank by remember { mutableStateOf(bankAccounts.firstOrNull()) }
    var senderBankName by remember(selectedBank) { mutableStateOf(selectedBank?.bankName ?: "State Bank of India") }
    var senderBankLast4 by remember { mutableStateOf((1000..9999).random().toString()) }
    
    var showPinScreen by remember { mutableStateOf(false) }
    var enteredPin by remember { mutableStateOf("") }
    val context = LocalContext.current
    
    // We only use the bankAccounts list for the dropdown now.''')

# Replace the banks list with the viewModel banks
content = content.replace(
'''    val banks = listOf(
        "State Bank of India",
        "HDFC Bank",
        "ICICI Bank",
        "Punjab National Bank",
        "Bank of Baroda",
        "Axis Bank",
        "Paytm Payments Bank"
    )''',
'''    val banks = bankAccounts.map { it.bankName }''')

# Now in the DropdownMenuItem:
content = content.replace(
'''                            banks.forEach { bank ->
                                DropdownMenuItem(
                                    text = { Text(bank) },
                                    onClick = { 
                                        senderBankName = bank
                                        showBankDropdown = false
                                    }
                                )
                            }''',
'''                            banks.forEach { bank ->
                                DropdownMenuItem(
                                    text = { Text(bank) },
                                    onClick = { 
                                        senderBankName = bank
                                        selectedBank = bankAccounts.find { it.bankName == bank }
                                        showBankDropdown = false
                                    }
                                )
                            }''')

# Intercept the PAY button
old_button = '''            Button(
                onClick = {
                    val finalAmount = amount.toDoubleOrNull() ?: 100.0
                    var timestamp = System.currentTimeMillis()
                    
                    if (!useCurrentTime && customDateString.isNotBlank()) {
                        try {
                            val sdf = SimpleDateFormat("dd-MM-yyyy HH:mm", Locale.getDefault())
                            val date = sdf.parse(customDateString)
                            if (date != null) {
                                timestamp = date.time
                            }
                        } catch (e: Exception) {
                            // Keep current time if parsing fails
                        }
                    }

                    viewModel.insertTransaction(
                        name = receiverName,
                        phone = receiverPhone,
                        upiId = receiverUpiId,
                        amount = finalAmount,
                        status = status,
                        bankName = senderBankName,
                        bankLast4 = senderBankLast4,
                        customTxId = customTxId,
                        customUtr = customUtr,
                        timestamp = timestamp,
                        onSuccess = { insertedId ->
                            onNavigateToReceipt(insertedId)
                        }
                    )
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(52.dp)
                    .testTag("create_prank_button"),
                colors = ButtonDefaults.buttonColors(containerColor = PhonePePurple),
                shape = RoundedCornerShape(26.dp)
            ) {
                Text(
                    text = "View successful payment screen! 🚀",
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.White
                )
            }'''

new_button = '''            Button(
                onClick = {
                    showPinScreen = true
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(52.dp)
                    .testTag("create_prank_button"),
                colors = ButtonDefaults.buttonColors(containerColor = PhonePePurple),
                shape = RoundedCornerShape(26.dp)
            ) {
                Text(
                    text = "PAY",
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.White
                )
            }'''

content = content.replace(old_button, new_button)

# Wrap the main Scaffold in a conditional to show PIN screen
content = content.replace(
'''    Scaffold(
        topBar = {''',
'''    if (showPinScreen) {
        PinEntryScreen(
            bankName = senderBankName,
            actionText = "Sending: ₹$amount",
            pin = enteredPin,
            onPinChange = { enteredPin = it },
            onSubmit = {
                val correctPin = selectedBank?.pin ?: "1234"
                if (enteredPin == correctPin) {
                    val finalAmount = amount.toDoubleOrNull() ?: 100.0
                    var timestamp = System.currentTimeMillis()
                    
                    if (!useCurrentTime && customDateString.isNotBlank()) {
                        try {
                            val sdf = SimpleDateFormat("dd-MM-yyyy HH:mm", java.util.Locale.getDefault())
                            val date = sdf.parse(customDateString)
                            if (date != null) {
                                timestamp = date.time
                            }
                        } catch (e: Exception) {
                            // Keep current time if parsing fails
                        }
                    }

                    viewModel.insertTransaction(
                        name = receiverName,
                        phone = receiverPhone,
                        upiId = receiverUpiId,
                        amount = finalAmount,
                        status = status,
                        bankName = senderBankName,
                        bankLast4 = senderBankLast4,
                        customTxId = customTxId,
                        customUtr = customUtr,
                        timestamp = timestamp,
                        onSuccess = { insertedId ->
                            onNavigateToReceipt(insertedId)
                        }
                    )
                } else {
                    Toast.makeText(context, "Incorrect UPI PIN", Toast.LENGTH_SHORT).show()
                    enteredPin = ""
                }
            }
        )
    } else {
    Scaffold(
        topBar = {'''
)

# And close the else block at the end
content = content.replace(
'''        }
    }
}''',
'''        }
    }
    }
}''')

with open('/app/applet/app/src/main/java/com/example/ui/screens/CreatePrankScreen.kt', 'w') as f:
    f.write(content)

