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
    var receiverPhoneOrUpi by remember { mutableStateOf("") }
    var amount by remember { mutableStateOf("") }
    
    val bankAccounts by viewModel.bankAccounts.collectAsState()
    var selectedBank by remember { mutableStateOf(bankAccounts.firstOrNull()) }
    var senderBankName by remember { mutableStateOf(selectedBank?.bankName ?: "State Bank of India") }
    var senderBankLast4 by remember { mutableStateOf(selectedBank?.bankDesc?.takeLast(4) ?: (1000..9999).random().toString()) }

    LaunchedEffect(bankAccounts) {
        if (selectedBank == null && bankAccounts.isNotEmpty()) {
            selectedBank = bankAccounts.first()
            senderBankName = bankAccounts.first().bankName
            senderBankLast4 = bankAccounts.first().bankDesc.takeLast(4)
        }
    }
    
    var showPinScreen by remember { mutableStateOf(false) }
    var showWrongPinScreen by remember { mutableStateOf(false) }
    var pinErrorTitle by remember { mutableStateOf("Payment failed") }
    var enteredPin by remember { mutableStateOf("") }
    val context = LocalContext.current
    
    var showBankDropdown by remember { mutableStateOf(false) }
    val banks = bankAccounts.map { it.bankName }

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
                    
                    val timestamp = System.currentTimeMillis()
                    
                    viewModel.insertTransaction(
                        name = receiverName,
                        phone = if (receiverPhoneOrUpi.all { it.isDigit() }) receiverPhoneOrUpi else "9876543210",
                        upiId = if (!receiverPhoneOrUpi.all { it.isDigit() }) receiverPhoneOrUpi else "$receiverPhoneOrUpi@ybl",
                        amount = finalAmount,
                        status = "SUCCESS",
                        bankName = senderBankName,
                        bankLast4 = senderBankLast4,
                        customTxId = viewModel.generateTransactionId(),
                        customUtr = viewModel.generateUtr(),
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
                title = { Text("Send Money", fontWeight = FontWeight.Bold, color = Color.White) },
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
            
            // Receiver Info Card
            Card(
                colors = CardDefaults.cardColors(containerColor = Color.White),
                shape = RoundedCornerShape(12.dp),
                elevation = CardDefaults.cardElevation(2.dp)
            ) {
                Column(
                    modifier = Modifier.padding(16.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    OutlinedTextField(
                        value = receiverName,
                        onValueChange = { receiverName = it },
                        label = { Text("Receiver Name (Optional)") },
                        modifier = Modifier.fillMaxWidth(),
                        singleLine = true
                    )
                    
                    OutlinedTextField(
                        value = receiverPhoneOrUpi,
                        onValueChange = { receiverPhoneOrUpi = it },
                        label = { Text("Bank Account Number or UPI ID") },
                        modifier = Modifier.fillMaxWidth(),
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
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    OutlinedTextField(
                        value = amount,
                        onValueChange = { amount = it },
                        label = { Text("Amount (in ₹)") },
                        leadingIcon = { Text("₹", modifier = Modifier.padding(start = 16.dp), fontSize = 18.sp, fontWeight = FontWeight.Bold, color = PhonePePurple) },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        modifier = Modifier.fillMaxWidth(),
                        singleLine = true
                    )

                    // Bank selection dropdown
                    Box(modifier = Modifier.fillMaxWidth()) {
                        OutlinedTextField(
                            value = senderBankName,
                            onValueChange = {},
                            readOnly = true,
                            label = { Text("Debit From") },
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
                                        val newBank = bankAccounts.find { it.bankName == bank }
                                        if (newBank != null) {
                                            selectedBank = newBank
                                            senderBankName = newBank.bankName
                                            senderBankLast4 = newBank.bankDesc.takeLast(4)
                                        }
                                        showBankDropdown = false
                                    }
                                )
                            }
                        }
                    }
                }
            }

            // Create Prank Button
            Button(
                onClick = {
                    viewModel.selectedPayeeUpi = receiverPhoneOrUpi
                    showPinScreen = true
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(52.dp)
                    .padding(top = 16.dp),
                colors = ButtonDefaults.buttonColors(containerColor = PhonePePurple),
                shape = RoundedCornerShape(26.dp)
            ) {
                Text(
                    text = "PROCEED TO PAY",
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.White,
                    letterSpacing = 1.sp
                )
            }
            
            Spacer(modifier = Modifier.height(16.dp))
        }
    }
    }
}
