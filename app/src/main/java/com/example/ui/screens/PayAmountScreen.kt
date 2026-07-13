package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.HelpOutline
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.Close
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.ui.BankAccount
import com.example.ui.PrankViewModel
import com.example.ui.theme.PhonePePurple

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PayAmountScreen(
    viewModel: PrankViewModel,
    payeeName: String = "YASHWANT MEGHWAL",
    upiId: String = "yashwant@ybl",
    prefilledAmount: String = "",
    onBack: () -> Unit,
    onProceed: (String, BankAccount) -> Unit
) {
    var amount by remember { mutableStateOf(prefilledAmount) }
    var message by remember { mutableStateOf("") }
    var showBottomSheet by remember { mutableStateOf(false) }
    
    val bankAccounts by viewModel.bankAccounts.collectAsState()
    val selectedBank = bankAccounts.firstOrNull()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Pay", fontWeight = FontWeight.Bold, fontSize = 20.sp) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    IconButton(onClick = { }) {
                        Icon(Icons.AutoMirrored.Filled.HelpOutline, contentDescription = "Help")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.White)
            )
        },
        containerColor = Color(0xFFF5F5F5),
        bottomBar = {
            Button(
                onClick = { if (amount.isNotEmpty()) showBottomSheet = true },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(80.dp)
                    .padding(16.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = if (amount.isNotEmpty()) PhonePePurple else Color.LightGray
                ),
                shape = RoundedCornerShape(8.dp),
                enabled = amount.isNotEmpty()
            ) {
                Text("Proceed To Pay", fontSize = 16.sp, fontWeight = FontWeight.Bold)
            }
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp)
        ) {
            Card(
                colors = CardDefaults.cardColors(containerColor = Color.White),
                shape = RoundedCornerShape(12.dp),
                elevation = CardDefaults.cardElevation(0.dp)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Box(
                            modifier = Modifier
                                .size(48.dp)
                                .background(Color(0xFF607D8B), CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(payeeName.replace("+", "").replace("%20", "").take(2).uppercase(), color = Color.White, fontSize = 18.sp)
                        }
                        Spacer(modifier = Modifier.width(12.dp))
                        Column {
                            Text(payeeName.replace("+", " ").replace("%20", " "), fontWeight = FontWeight.Bold, fontSize = 16.sp)
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Text(upiId, color = Color.Gray, fontSize = 14.sp)
                            }
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Text("Banking name: ${payeeName.replace("+", " ").replace("%20", " ")}", color = Color.Gray, fontSize = 12.sp)
                                Spacer(modifier = Modifier.width(4.dp))
                                Icon(Icons.Default.CheckCircle, contentDescription = null, tint = Color(0xFF388E3C), modifier = Modifier.size(14.dp))
                            }
                        }
                    }
                    
                    Spacer(modifier = Modifier.height(24.dp))
                    
                    // Amount Input
                    OutlinedTextField(
                        value = amount,
                        onValueChange = { amount = it },
                        textStyle = TextStyle(fontSize = 24.sp, fontWeight = FontWeight.Bold),
                        placeholder = { Text("₹ Enter amount", fontSize = 24.sp, fontWeight = FontWeight.Bold, color = Color.Gray) },
                        leadingIcon = {
                            if (amount.isNotEmpty()) {
                                Text("₹", fontSize = 24.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(start = 12.dp))
                            }
                        },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        modifier = Modifier.fillMaxWidth(),
                        singleLine = true,
                        shape = RoundedCornerShape(8.dp)
                    )
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    OutlinedTextField(
                        value = message,
                        onValueChange = { message = it },
                        placeholder = { Text("Add a message (optional)") },
                        modifier = Modifier.fillMaxWidth(),
                        singleLine = true,
                        shape = RoundedCornerShape(8.dp)
                    )
                }
            }
        }
    }

    if (showBottomSheet && selectedBank != null) {
        ModalBottomSheet(
            onDismissRequest = { showBottomSheet = false },
            containerColor = Color.White
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("Total Payable", fontWeight = FontWeight.Bold, fontSize = 18.sp)
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text("₹$amount", fontWeight = FontWeight.Bold, fontSize = 24.sp)
                        Spacer(modifier = Modifier.width(8.dp))
                        Icon(Icons.Default.Close, contentDescription = "Close", modifier = Modifier.clickable { showBottomSheet = false })
                    }
                }
                
                Spacer(modifier = Modifier.height(16.dp))
                
                var currentSelectedBank by remember { mutableStateOf(selectedBank) }
                
                Card(
                    colors = CardDefaults.cardColors(containerColor = Color(0xFFF5F5F5)),
                    shape = RoundedCornerShape(12.dp)
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("Accounts", color = Color.Gray, fontSize = 12.sp)
                        Spacer(modifier = Modifier.height(8.dp))
                        
                        bankAccounts.forEach { bank ->
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .clickable { currentSelectedBank = bank }
                                    .padding(vertical = 8.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Box(modifier = Modifier.size(32.dp).border(1.dp, Color(0xFFE0E0E0), RoundedCornerShape(8.dp)), contentAlignment = Alignment.Center) { com.example.ui.components.BankLogo(bankName = bank.bankName, size = 24.dp) }
                                Spacer(modifier = Modifier.width(12.dp))
                                Column(modifier = Modifier.weight(1f)) {
                                    Text(bank.accountName, fontSize = 16.sp)
                                    Text("•• ${bank.bankDesc.takeLast(4)} UPI", color = Color.Gray, fontSize = 14.sp)
                                }
                                Text("₹$amount", fontWeight = FontWeight.Bold, fontSize = 16.sp)
                                Spacer(modifier = Modifier.width(8.dp))
                                if (currentSelectedBank?.id == bank.id) {
                                    Icon(Icons.Default.CheckCircle, contentDescription = null, tint = Color(0xFF388E3C))
                                } else {
                                    Box(modifier = Modifier.size(24.dp))
                                }
                            }
                        }
                    }
                }
                
                Spacer(modifier = Modifier.height(24.dp))
                
                val context = androidx.compose.ui.platform.LocalContext.current
                var showInsufficientBalanceDialog by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf(false) }
                
                if (showInsufficientBalanceDialog) {
                    androidx.compose.material3.AlertDialog(
                        onDismissRequest = { showInsufficientBalanceDialog = false },
                        title = { Text("Payment Failed") },
                        text = { Text("Your account balance is insufficient for this transaction.") },
                        confirmButton = {
                            androidx.compose.material3.TextButton(onClick = { showInsufficientBalanceDialog = false }) {
                                Text("OK", color = PhonePePurple)
                            }
                        }
                    )
                }

                Button(
                    onClick = { 
                        val payAmount = amount.toDoubleOrNull() ?: 0.0
                        if (payAmount > currentSelectedBank.balance) {
                            showInsufficientBalanceDialog = true
                        } else {
                            showBottomSheet = false
                            onProceed(amount, currentSelectedBank)
                        }
                    },
                    modifier = Modifier.fillMaxWidth().height(52.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = PhonePePurple),
                    shape = RoundedCornerShape(8.dp)
                ) {
                    Text("Pay ₹$amount", fontSize = 16.sp, fontWeight = FontWeight.Bold)
                }
                Spacer(modifier = Modifier.height(24.dp))
            }
        }
    }
}
