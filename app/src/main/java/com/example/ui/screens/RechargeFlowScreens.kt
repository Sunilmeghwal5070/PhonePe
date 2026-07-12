package com.example.ui.screens


import androidx.compose.foundation.border

import androidx.compose.foundation.clickable

import androidx.compose.animation.AnimatedVisibility

import androidx.compose.animation.AnimatedContent

import androidx.compose.animation.ExperimentalAnimationApi

import androidx.compose.foundation.Canvas

import androidx.compose.foundation.background

import androidx.compose.foundation.layout.*

import androidx.compose.foundation.shape.CircleShape

import androidx.compose.foundation.shape.RoundedCornerShape

import androidx.compose.material.icons.Icons

import androidx.compose.material.icons.filled.Check

import androidx.compose.material.icons.filled.KeyboardArrowDown

import androidx.compose.material3.*

import androidx.compose.runtime.*

import androidx.compose.animation.core.*

import androidx.compose.ui.draw.scale

import androidx.compose.ui.Alignment

import androidx.compose.ui.Modifier

import androidx.compose.ui.graphics.Color

import androidx.compose.ui.text.font.FontWeight

import androidx.compose.ui.unit.dp

import androidx.compose.ui.unit.sp

import java.text.SimpleDateFormat

import java.util.*

import androidx.compose.foundation.rememberScrollState

import androidx.compose.foundation.verticalScroll

import androidx.compose.material.icons.automirrored.filled.*

import androidx.compose.material.icons.filled.*


import kotlinx.coroutines.delay

import com.example.ui.PrankViewModel

import androidx.compose.ui.text.style.TextAlign

import android.widget.Toast

import androidx.compose.ui.platform.LocalContext

@Composable
fun RechargePinScreen(
    viewModel: com.example.ui.PrankViewModel,
    name: String,
    amount: String,
    bankId: String,
    onBack: () -> Unit,
    onSuccess: (Int) -> Unit
) {
    val bankAccounts by viewModel.bankAccounts.collectAsState()
    val account = bankAccounts.find { it.id == bankId } ?: bankAccounts.firstOrNull()
    
    var enteredPin by remember { mutableStateOf("") }
    var showWrongPinScreen by remember { mutableStateOf(false) }
    val context = androidx.compose.ui.platform.LocalContext.current


    if (showWrongPinScreen) {
        WrongPinScreen(
            bankName = account?.bankName ?: "State Bank of India",
            bankDesc = "${account?.bankName ?: "Bank"} - ${account?.bankDesc?.takeLast(4) ?: "0365"}",
            errorTitle = "Payment failed",
            onResetPin = { showWrongPinScreen = false; enteredPin = "" },
            onReEnterPin = { showWrongPinScreen = false; enteredPin = "" },
            onDone = { showWrongPinScreen = false }
        )
        return
    }

    PinEntryScreen(
        bankName = account?.bankName ?: "Bank",
        actionText = "Recharge Mobile",
        pin = enteredPin,
        onPinChange = { enteredPin = it },
        onSubmit = {
            if (enteredPin == account?.pin) {
                enteredPin = ""
                // Deduct balance
                account?.let { 
                    // Let insertTransaction handle balance deduction
                    val amt = amount.toDoubleOrNull() ?: 0.0
                    viewModel.insertTransaction(
                        name = name,
                        phone = name, // using name as phone for now
                        upiId = "",
                        amount = amt,
                        status = "SUCCESS",
                        type = "RECHARGE",
                        bankName = it.bankName,
                        bankLast4 = it.bankDesc.takeLast(4),
                        customTxId = "NX26061723274381818502541",
                        customUtr = "201104189977",
                        timestamp = System.currentTimeMillis()
                    ) { txId ->
                        com.example.ui.NotificationHelper.showBankSmsNotification(context, amt, it.bankDesc.takeLast(4), name, it.bankName)
                        onSuccess(txId)
                    }
                } ?: run {
                    onSuccess(0)
                }
            } else {
                showWrongPinScreen = true
            }
        }
    )
}

@Composable
fun RechargeProcessingScreen(
    name: String,
    amount: String,
    onSuccess: () -> Unit
) {
    var step by remember { mutableStateOf(0) }

    LaunchedEffect(Unit) {
        delay(1500)
        step = 1
        delay(1500)
        onSuccess()
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.White),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        CircularProgressIndicator(color = Color(0xFF5f259f), modifier = Modifier.size(64.dp))
        Spacer(modifier = Modifier.height(24.dp))
        Text(
            if (step == 0) "Connecting securely..." else "Processing Recharge of ₹$amount to $name",
            fontSize = 16.sp,
            fontWeight = FontWeight.Medium,
            color = Color.Black
        )
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RechargeSuccessScreen(
    transactionId: Int,
    viewModel: PrankViewModel,
    onDone: () -> Unit
) {
    val tx by viewModel.allTransactions.collectAsState()
    val currentTx = tx.find { it.id == transactionId }

    if (currentTx == null) {
        // Fallback or loading
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            CircularProgressIndicator()
        }
        return
    }

    val sdf = SimpleDateFormat("hh:mm a 'on' dd MMM yyyy", Locale.getDefault())
    val formattedDate = sdf.format(Date(currentTx.timestamp))

    var planExpanded by remember { mutableStateOf(false) }
    var paymentExpanded by remember { mutableStateOf(false) }

    Scaffold(
        containerColor = Color(0xFFF9F9FB),
        topBar = {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(Color(0xFF2E7D32)) // Green
                    .padding(top = 16.dp, bottom = 12.dp, start = 8.dp, end = 16.dp)
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    IconButton(onClick = onDone) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                            contentDescription = "Back",
                            tint = Color.White
                        )
                    }
                    Spacer(modifier = Modifier.width(4.dp))
                    Column {
                        Text(
                            text = "Recharge successful",
                            color = Color.White,
                            fontSize = 18.sp,
                            fontWeight = FontWeight.Bold
                        )
                        Text(
                            text = formattedDate,
                            color = Color.White.copy(alpha = 0.9f),
                            fontSize = 13.sp
                        )
                    }
                }
            }
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .verticalScroll(rememberScrollState())
        ) {
            Spacer(modifier = Modifier.height(16.dp))

            // Main Card
            Card(
                colors = CardDefaults.cardColors(containerColor = Color.White),
                shape = RoundedCornerShape(12.dp),
                elevation = CardDefaults.cardElevation(defaultElevation = 0.dp),
                border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFEEEEEE)),
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp)
            ) {
                Column {
                    // Header
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        // Icon
                        Box(
                            modifier = Modifier
                                .size(48.dp)
                                .border(1.dp, Color.LightGray, RoundedCornerShape(8.dp)),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Default.PhoneIphone, contentDescription = null, tint = Color.Black, modifier = Modifier.size(28.dp))
                            Icon(Icons.Default.Bolt, contentDescription = null, tint = Color.Black, modifier = Modifier.size(16.dp))
                        }
                        
                        Spacer(modifier = Modifier.width(16.dp))
                        
                        Column(modifier = Modifier.weight(1f)) {
                            Text("Mobile recharged", color = Color.DarkGray, fontSize = 14.sp)
                            Text("Jio Prepaid", fontWeight = FontWeight.Bold, fontSize = 16.sp, color = Color.Black)
                            Text(currentTx.receiverPhone, color = Color.Gray, fontSize = 14.sp)
                        }
                        
                        Text("₹${currentTx.amount.toInt()}", fontWeight = FontWeight.Bold, fontSize = 20.sp, color = Color.Black)
                    }

                    HorizontalDivider(color = Color(0xFFEEEEEE))

                    // Plan details
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable { planExpanded = !planExpanded }
                            .padding(16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(Icons.Default.ListAlt, contentDescription = null, tint = Color.DarkGray)
                        Spacer(modifier = Modifier.width(12.dp))
                        Text("Plan details", fontSize = 16.sp, color = Color.Black, modifier = Modifier.weight(1f))
                        Icon(if(planExpanded) Icons.Default.KeyboardArrowUp else Icons.Default.KeyboardArrowDown, contentDescription = null)
                    }

                    AnimatedVisibility(visible = planExpanded) {
                        Row(modifier = Modifier.fillMaxWidth().padding(horizontal = 48.dp, vertical = 8.dp), horizontalArrangement = Arrangement.SpaceBetween) {
                            val details = getPlanDetails(currentTx.amount)
                            Column {
                                Text("Validity", color = Color.Gray, fontSize = 13.sp)
                                Text(details.first, color = Color.Black, fontSize = 14.sp)
                            }
                            Column(horizontalAlignment = Alignment.End) {
                                Text("Data", color = Color.Gray, fontSize = 13.sp)
                                Text(details.second, color = Color.Black, fontSize = 14.sp)
                            }
                        }
                    }

                    HorizontalDivider(color = Color(0xFFEEEEEE))

                    // Payment details
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable { paymentExpanded = !paymentExpanded }
                            .padding(16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(Icons.Default.Receipt, contentDescription = null, tint = Color.DarkGray)
                        Spacer(modifier = Modifier.width(12.dp))
                        Text("Payment Details", fontSize = 16.sp, color = Color.Black, modifier = Modifier.weight(1f))
                        Icon(if(paymentExpanded) Icons.Default.KeyboardArrowUp else Icons.Default.KeyboardArrowDown, contentDescription = null)
                    }

                    AnimatedVisibility(visible = paymentExpanded) {
                        Column(modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp)) {
                            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                                Text("Recharge Amount", color = Color.Gray, fontSize = 14.sp)
                                Text("₹${currentTx.amount.toInt()}", color = Color.Gray, fontSize = 14.sp)
                            }
                            Spacer(modifier = Modifier.height(8.dp))
                            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                                Text("Platform fee(inclusive of GST)", color = Color.Gray, fontSize = 14.sp)
                                Text("+ ₹0", color = Color.Gray, fontSize = 14.sp)
                            }
                        }
                    }

                    HorizontalDivider(color = Color(0xFFEEEEEE))
                    
                    // Total Amount
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(16.dp),
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Text("Total Amount", fontWeight = FontWeight.Bold, fontSize = 16.sp, color = Color.Black)
                        Text("₹${currentTx.amount.toInt()}", fontWeight = FontWeight.Bold, fontSize = 18.sp, color = Color.Black)
                    }

                    HorizontalDivider(color = Color(0xFFEEEEEE), thickness = 8.dp)

                    // TX IDs
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("PhonePe Transaction ID", color = Color.Gray, fontSize = 13.sp)
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                            Text(currentTx.transactionId, color = Color.Black, fontSize = 14.sp)
                            Icon(Icons.Default.ContentCopy, contentDescription = null, tint = Color(0xFF5f259f), modifier = Modifier.size(18.dp))
                        }
                        
                        Spacer(modifier = Modifier.height(16.dp))
                        
                        Text("Jio Prepaid Reference ID", color = Color.Gray, fontSize = 13.sp)
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                            Text("26104453538", color = Color.Black, fontSize = 14.sp)
                            Icon(Icons.Default.ContentCopy, contentDescription = null, tint = Color(0xFF5f259f), modifier = Modifier.size(18.dp))
                        }
                        
                        Spacer(modifier = Modifier.height(16.dp))
                        
                        Text("Debited from", color = Color.Gray, fontSize = 13.sp)
                        Spacer(modifier = Modifier.height(8.dp))
                        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {
                            com.example.ui.components.BankLogo(bankName = currentTx.senderBankName, size = 24.dp)
                            Spacer(modifier = Modifier.width(12.dp))
                            Text("XXXXXX${currentTx.senderBankAccountLast4}", fontSize = 15.sp, color = Color.Black, modifier = Modifier.weight(1f))
                            Text("₹${currentTx.amount.toInt()}", fontSize = 15.sp, color = Color.Black)
                        }
                        
                        Spacer(modifier = Modifier.height(8.dp))
                        Row(modifier = Modifier.fillMaxWidth().padding(start = 36.dp), horizontalArrangement = Arrangement.SpaceBetween) {
                            Text("UTR: ${currentTx.utr}", color = Color.Gray, fontSize = 14.sp)
                            Icon(Icons.Default.ContentCopy, contentDescription = null, tint = Color(0xFF5f259f), modifier = Modifier.size(18.dp))
                        }
                    }

                    HorizontalDivider(color = Color(0xFFEEEEEE))

                    // Actions Row
                    Row(
                        modifier = Modifier.fillMaxWidth().padding(16.dp),
                        horizontalArrangement = Arrangement.SpaceEvenly
                    ) {
                        ActionItem(icon = Icons.Default.Schedule, text = "View\nHistory")
                        ActionItem(icon = Icons.AutoMirrored.Filled.CallMade, text = "Recharge\nAgain")
                        ActionItem(icon = Icons.Default.CallSplit, text = "Split\nExpense")
                        ActionItem(icon = Icons.Default.Share, text = "Share\nReceipt")
                    }
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            // Contact Support
            Card(
                colors = CardDefaults.cardColors(containerColor = Color.White),
                shape = RoundedCornerShape(12.dp),
                elevation = CardDefaults.cardElevation(defaultElevation = 0.dp),
                border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFEEEEEE)),
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth().padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(Icons.Default.HelpOutline, contentDescription = null, tint = Color.Black)
                    Spacer(modifier = Modifier.width(12.dp))
                    Text("Contact PhonePe Support", fontSize = 16.sp, color = Color.Black, modifier = Modifier.weight(1f))
                    Icon(Icons.Default.KeyboardArrowRight, contentDescription = null, tint = Color.Gray)
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            // Banner
            Card(
                colors = CardDefaults.cardColors(containerColor = Color.White),
                shape = RoundedCornerShape(12.dp),
                elevation = CardDefaults.cardElevation(defaultElevation = 0.dp),
                border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFEEEEEE)),
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth().padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text("Buy a prepaid Jio SIM!", fontWeight = FontWeight.Bold, fontSize = 16.sp, color = Color.Black)
                        Text("Follow a full online process and enjoy free home delivery.", color = Color.Gray, fontSize = 13.sp)
                        Spacer(modifier = Modifier.height(12.dp))
                        Button(
                            onClick = {},
                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF5f259f)),
                            shape = RoundedCornerShape(8.dp),
                            modifier = Modifier.height(36.dp),
                            contentPadding = PaddingValues(horizontal = 16.dp, vertical = 0.dp)
                        ) {
                            Text("Buy now", color = Color.White, fontSize = 14.sp)
                        }
                    }
                    Spacer(modifier = Modifier.width(8.dp))
                    // Simple Box as Jio logo for now
                    Box(modifier = Modifier.size(64.dp).background(Color(0xFF0033A0), CircleShape), contentAlignment = Alignment.Center) {
                        Text("Jio", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 24.sp)
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(32.dp))
        }
    }
}

@Composable
fun ActionItem(icon: androidx.compose.ui.graphics.vector.ImageVector, text: String) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Box(
            modifier = Modifier.size(48.dp).background(Color(0xFFF3E5F5), CircleShape).border(1.dp, Color(0xFFE1BEE7), CircleShape),
            contentAlignment = Alignment.Center
        ) {
            Icon(imageVector = icon, contentDescription = null, tint = Color(0xFF5f259f))
        }
        Spacer(modifier = Modifier.height(8.dp))
        Text(text, fontSize = 12.sp, color = Color.DarkGray, textAlign = androidx.compose.ui.text.style.TextAlign.Center, lineHeight = 16.sp)
    }
}

fun getPlanDetails(amount: Double): Pair<String, String> {
    val planAmt = amount.toInt()
    return when(planAmt) {
        299 -> "28 Days" to "1.5 GB/Day"
        479 -> "56 Days" to "1.5 GB/Day"
        719 -> "84 Days" to "1.5 GB/Day"
        29 -> "1 Day" to "2 GB"
        349 -> "28 Days" to "2.5 GB/Day"
        899 -> "90 Days" to "2.5 GB/Day"
        3599 -> "365 Days" to "2.5 GB/Day"
        26 -> "1 Day" to "1.5 GB"
        449 -> "28 Days" to "3 GB/Day"
        901 -> "84 Days" to "3 GB/Day"
        else -> "28 Days" to "1.5 GB/Day"
    }
}
