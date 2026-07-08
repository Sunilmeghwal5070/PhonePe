package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import android.widget.Toast
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.ui.PrankViewModel
import com.example.ui.theme.*
import java.text.SimpleDateFormat
import java.util.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CreatePrankScreen(
    viewModel: PrankViewModel,
    onBack: () -> Unit,
    onNavigateToReceipt: (Int) -> Unit
) {
    var receiverName by remember { mutableStateOf("") }
    var receiverPhone by remember { mutableStateOf("") }
    var receiverUpiId by remember { mutableStateOf("") }
    var amount by remember { mutableStateOf("") }
    var status by remember { mutableStateOf("SUCCESS") }
    val bankAccounts by viewModel.bankAccounts.collectAsState()
    var selectedBank by remember { mutableStateOf(bankAccounts.firstOrNull()) }
    var senderBankName by remember(selectedBank) { mutableStateOf(selectedBank?.bankName ?: "State Bank of India") }
    var senderBankLast4 by remember { mutableStateOf((1000..9999).random().toString()) }
    
    var showPinScreen by remember { mutableStateOf(false) }
    var showWrongPinScreen by remember { mutableStateOf(false) }
    var pinErrorTitle by remember { mutableStateOf("Payment failed") }
    var enteredPin by remember { mutableStateOf("") }
    val context = LocalContext.current
    
    // We only use the bankAccounts list for the dropdown now.
    
    var customTxId by remember { mutableStateOf(viewModel.generateTransactionId()) }
    var customUtr by remember { mutableStateOf(viewModel.generateUtr()) }
    
    var useCurrentTime by remember { mutableStateOf(true) }
    var customDateString by remember { mutableStateOf("") }

    val banks = bankAccounts.map { it.bankName }
    
    var showBankDropdown by remember { mutableStateOf(false) }


    if (showWrongPinScreen) {
        WrongPinScreen(
            bankName = senderBankName,
            bankDesc = "$senderBankName - $senderBankLast4",
            errorTitle = pinErrorTitle,
            onResetPin = { showWrongPinScreen = false; enteredPin = "" },
            onReEnterPin = { showWrongPinScreen = false; enteredPin = "" },
            onDone = { showWrongPinScreen = false; showPinScreen = false; enteredPin = "" }
        )
        return
    }

    if (showPinScreen) {
        PinEntryScreen(
            bankName = senderBankName,
            actionText = "Sending: ₹$amount",
            pin = enteredPin,
            onPinChange = { enteredPin = it },
            onSubmit = {
                val correctPin = selectedBank?.pin ?: "1234"
                if (enteredPin == correctPin) {
                    val finalAmount = amount.toDoubleOrNull() ?: 100.0
                    if (selectedBank != null && finalAmount > selectedBank!!.balance) {
                        pinErrorTitle = "Insufficient Balance"
                        showWrongPinScreen = true
                        return@PinEntryScreen
                    }
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
                            enteredPin = ""; onNavigateToReceipt(insertedId)
                        }
                    )
                } else {
                    showWrongPinScreen = true; pinErrorTitle = "Payment failed"
                        return@PinEntryScreen
                }
            }
        )
    } else {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("New Payment", fontWeight = FontWeight.Bold, color = Color.White) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                            contentDescription = "Back",
                            tint = Color.White
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = PhonePePurple
                )
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .background(PhonePeBgGray)
                .verticalScroll(rememberScrollState())
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // Payee Info Card
            Card(
                colors = CardDefaults.cardColors(containerColor = Color.White),
                shape = RoundedCornerShape(12.dp),
                elevation = CardDefaults.cardElevation(2.dp)
            ) {
                Column(
                    modifier = Modifier.padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    Text(
                        text = "Payee Details",
                        fontWeight = FontWeight.Bold,
                        color = PhonePePurple,
                        fontSize = 16.sp
                    )
                    
                    OutlinedTextField(
                        value = receiverName,
                        onValueChange = { receiverName = it },
                        label = { Text("Full Name") },
                        leadingIcon = { Icon(Icons.Default.Person, contentDescription = null, tint = PhonePePurple) },
                        modifier = Modifier.fillMaxWidth().testTag("receiver_name_input"),
                        singleLine = true
                    )
                    
                    OutlinedTextField(
                        value = receiverPhone,
                        onValueChange = { receiverPhone = it },
                        label = { Text("Mobile Number") },
                        leadingIcon = { Icon(Icons.Default.Phone, contentDescription = null, tint = PhonePePurple) },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Phone),
                        modifier = Modifier.fillMaxWidth().testTag("receiver_phone_input"),
                        singleLine = true
                    )
                    
                    OutlinedTextField(
                        value = receiverUpiId,
                        onValueChange = { receiverUpiId = it },
                        label = { Text("UPI ID (Leave blank to generate)") },
                        leadingIcon = { Icon(Icons.Default.AlternateEmail, contentDescription = null, tint = PhonePePurple) },
                        modifier = Modifier.fillMaxWidth().testTag("receiver_upi_input"),
                        singleLine = true
                    )
                }
            }

            // Payment Amount & Bank Card
            Card(
                colors = CardDefaults.cardColors(containerColor = Color.White),
                shape = RoundedCornerShape(12.dp),
                elevation = CardDefaults.cardElevation(2.dp)
            ) {
                Column(
                    modifier = Modifier.padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    Text(
                        text = "Payment and Bank Info",
                        fontWeight = FontWeight.Bold,
                        color = PhonePePurple,
                        fontSize = 16.sp
                    )
                    
                    OutlinedTextField(
                        value = amount,
                        onValueChange = { amount = it },
                        label = { Text("Amount (in ₹)") },
                        leadingIcon = { Icon(Icons.Default.CurrencyRupee, contentDescription = null, tint = PhonePePurple) },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        modifier = Modifier.fillMaxWidth().testTag("amount_input"),
                        singleLine = true
                    )

                    // Bank selection dropdown
                    Box(modifier = Modifier.fillMaxWidth()) {
                        OutlinedTextField(
                            value = senderBankName,
                            onValueChange = {},
                            readOnly = true,
                            label = { Text("Debit Bank") },
                            leadingIcon = { Icon(Icons.Default.AccountBalance, contentDescription = null, tint = PhonePePurple) },
                            trailingIcon = { 
                                Icon(
                                    Icons.Default.ArrowDropDown, 
                                    contentDescription = null,
                                    modifier = Modifier.clickable { showBankDropdown = true }
                                ) 
                            },
                            modifier = Modifier.fillMaxWidth().clickable { showBankDropdown = true }
                        )
                        DropdownMenu(
                            expanded = showBankDropdown,
                            onDismissRequest = { showBankDropdown = false },
                            modifier = Modifier.fillMaxWidth(0.9f)
                        ) {
                            banks.forEach { bank ->
                                DropdownMenuItem(
                                    text = { Text(bank) },
                                    onClick = {
                                        senderBankName = bank
                                        showBankDropdown = false
                                    }
                                )
                            }
                        }
                    }

                    OutlinedTextField(
                        value = senderBankLast4,
                        onValueChange = { senderBankLast4 = it.take(4) },
                        label = { Text("Bank Account Last 4 Digits") },
                        leadingIcon = { Icon(Icons.Default.Lock, contentDescription = null, tint = PhonePePurple) },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        modifier = Modifier.fillMaxWidth(),
                        singleLine = true
                    )
                }
            }

            // Advanced Card (Tx ID, UTR, Date)
            Card(
                colors = CardDefaults.cardColors(containerColor = Color.White),
                shape = RoundedCornerShape(12.dp),
                elevation = CardDefaults.cardElevation(2.dp)
            ) {
                Column(
                    modifier = Modifier.padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    Text(
                        text = "Advanced Settings",
                        fontWeight = FontWeight.Bold,
                        color = PhonePePurple,
                        fontSize = 16.sp
                    )
                    
                    OutlinedTextField(
                        value = customTxId,
                        onValueChange = { customTxId = it },
                        label = { Text("Transaction ID") },
                        trailingIcon = {
                            IconButton(onClick = { customTxId = viewModel.generateTransactionId() }) {
                                Icon(Icons.Default.Refresh, contentDescription = "Regenerate")
                            }
                        },
                        modifier = Modifier.fillMaxWidth(),
                        singleLine = true
                    )
                    
                    OutlinedTextField(
                        value = customUtr,
                        onValueChange = { customUtr = it },
                        label = { Text("UTR Number (12 digit)") },
                        trailingIcon = {
                            IconButton(onClick = { customUtr = viewModel.generateUtr() }) {
                                Icon(Icons.Default.Refresh, contentDescription = "Regenerate")
                            }
                        },
                        modifier = Modifier.fillMaxWidth(),
                        singleLine = true
                    )
                    
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Checkbox(
                            checked = useCurrentTime,
                            onCheckedChange = { useCurrentTime = it }
                        )
                        Text("Use Current Time")
                    }

                    if (!useCurrentTime) {
                        OutlinedTextField(
                            value = customDateString,
                            onValueChange = { customDateString = it },
                            label = { Text("Custom Date (Format: dd-MM-yyyy HH:mm)") },
                            placeholder = { Text("e.g. 06-07-2026 14:30") },
                            modifier = Modifier.fillMaxWidth()
                        )
                    }

                    // Status selection
                    Text("Transaction Status:", fontWeight = FontWeight.Medium)
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(16.dp)
                    ) {
                        FilterChip(
                            selected = status == "SUCCESS",
                            onClick = { status = "SUCCESS" },
                            label = { Text("SUCCESS") },
                            colors = FilterChipDefaults.filterChipColors(
                                selectedContainerColor = PhonePeSuccessGreen.copy(alpha = 0.2f),
                                selectedLabelColor = PhonePeSuccessGreen
                            )
                        )
                        FilterChip(
                            selected = status == "PENDING",
                            onClick = { status = "PENDING" },
                            label = { Text("PENDING") },
                            colors = FilterChipDefaults.filterChipColors(
                                selectedContainerColor = PhonePePendingOrange.copy(alpha = 0.2f),
                                selectedLabelColor = PhonePePendingOrange
                            )
                        )
                        FilterChip(
                            selected = status == "FAILED",
                            onClick = { status = "FAILED" },
                            label = { Text("FAILED") },
                            colors = FilterChipDefaults.filterChipColors(
                                selectedContainerColor = PhonePeFailedRed.copy(alpha = 0.2f),
                                selectedLabelColor = PhonePeFailedRed
                            )
                        )
                    }
                }
            }

            // Create Prank Button
            Button(
                onClick = {
                    viewModel.selectedPayeeUpi = receiverUpiId
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
            }
            
            Spacer(modifier = Modifier.height(16.dp))
        }
    }
    }
}
