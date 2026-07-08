package com.example.ui.screens

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.HelpOutline
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.DeleteOutline
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material3.*
import androidx.compose.runtime.*
import coil.compose.AsyncImage
import androidx.compose.ui.draw.clip
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

import com.example.ui.PrankViewModel
import com.example.ui.BankAccount

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AddBankAccountDetailsScreen(
    bankName: String,
    viewModel: PrankViewModel,
    onBack: () -> Unit,
    onSave: () -> Unit
) {
    var name by remember { mutableStateOf("Your Name") }
    var bankDesc by remember { mutableStateOf("$bankName - XXXX") }
    var accType by remember { mutableStateOf(":  Saving Account") }
    var branch by remember { mutableStateOf(":  BRANCH NAME") }
    var ifsc by remember { mutableStateOf(":  IFSC0000000") }
    var upiPinStatus by remember { mutableStateOf("4 digit UPI PIN exists") }
    var balance by remember { mutableStateOf("1297") }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Add Bank Details", fontWeight = FontWeight.Bold, fontSize = 20.sp) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    TextButton(onClick = {
                        viewModel.addBankAccount(
                            BankAccount(
                                bankName = bankName,
                                accountName = name,
                                bankDesc = bankDesc,
                                type = accType,
                                branch = branch,
                                ifsc = ifsc,
                                balance = balance.toDoubleOrNull() ?: 1297.0,
                                pin = "1234"
                            )
                        )
                        onSave()
                    }) {
                        Text("SAVE", color = Color(0xFF5f259f), fontWeight = FontWeight.Bold)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = Color.White
                )
            )
        },
        containerColor = Color(0xFFF5F5F5)
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .verticalScroll(rememberScrollState())
        ) {
            // Bank Info Card
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 8.dp),
                colors = CardDefaults.cardColors(containerColor = Color.White),
                shape = RoundedCornerShape(12.dp),
                elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        // Generic Bank Logo
                        Box(
                            modifier = Modifier
                                .size(40.dp)
                                .border(1.dp, Color(0xFFEEEEEE), RoundedCornerShape(8.dp))
                                .background(Color(0xFFF5F5F5), RoundedCornerShape(8.dp)),
                            contentAlignment = Alignment.Center
                        ) {
                            coil.compose.AsyncImage(model = getBankLogoUrl(bankName), contentDescription = bankName, modifier = Modifier.size(32.dp).clip(RoundedCornerShape(8.dp)), contentScale = androidx.compose.ui.layout.ContentScale.Fit)
                        }
                        
                        Spacer(modifier = Modifier.width(16.dp))
                        
                        Column {
                            BasicTextField(value = name, onValueChange = { name = it }, textStyle = TextStyle(fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color.Black))
                            Spacer(modifier = Modifier.height(4.dp))
                            BasicTextField(value = bankDesc, onValueChange = { bankDesc = it }, textStyle = TextStyle(fontSize = 14.sp, color = Color.Gray))
                        }
                    }
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    HorizontalDivider(color = Color(0xFFF0F0F0))
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text("Set as Primary", fontSize = 16.sp, color = Color.Black)
                        Icon(Icons.Default.CheckCircle, contentDescription = "Primary", tint = Color(0xFF388E3C))
                    }
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    HorizontalDivider(color = Color(0xFFF0F0F0))
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Column {
                            Text("Type", fontSize = 14.sp, color = Color.Gray)
                            Spacer(modifier = Modifier.height(8.dp))
                            Text("Branch", fontSize = 14.sp, color = Color.Gray)
                            Spacer(modifier = Modifier.height(8.dp))
                            Text("IFSC", fontSize = 14.sp, color = Color.Gray)
                        }
                        Column {
                            BasicTextField(value = accType, onValueChange = { accType = it }, textStyle = TextStyle(fontSize = 14.sp, color = Color.Gray))
                            Spacer(modifier = Modifier.height(8.dp))
                            BasicTextField(value = branch, onValueChange = { branch = it }, textStyle = TextStyle(fontSize = 14.sp, color = Color.Gray))
                            Spacer(modifier = Modifier.height(8.dp))
                            BasicTextField(value = ifsc, onValueChange = { ifsc = it }, textStyle = TextStyle(fontSize = 14.sp, color = Color.Gray))
                        }
                    }
                }
            }
            
            // UPI PIN
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 4.dp),
                colors = CardDefaults.cardColors(containerColor = Color.White),
                shape = RoundedCornerShape(12.dp)
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column {
                        Text("UPI PIN", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.Black)
                        BasicTextField(value = upiPinStatus, onValueChange = { upiPinStatus = it }, textStyle = TextStyle(fontSize = 14.sp, color = Color.Gray))
                    }
                    Row {
                        Text("RESET", color = Color(0xFF5f259f), fontWeight = FontWeight.Bold, fontSize = 14.sp, modifier = Modifier.clickable { })
                        Spacer(modifier = Modifier.width(16.dp))
                        Text("CHANGE", color = Color(0xFF5f259f), fontWeight = FontWeight.Bold, fontSize = 14.sp, modifier = Modifier.clickable { })
                    }
                }
            }
            
            // Balance
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 4.dp),
                colors = CardDefaults.cardColors(containerColor = Color.White),
                shape = RoundedCornerShape(12.dp)
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    BasicTextField(value = balance, onValueChange = { balance = it }, textStyle = TextStyle(fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.Black))
                    Text("CHECK BALANCE", color = Color(0xFF5f259f), fontWeight = FontWeight.Bold, fontSize = 14.sp, modifier = Modifier.clickable { })
                }
            }
            
            // International UPI
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 4.dp),
                colors = CardDefaults.cardColors(containerColor = Color.White),
                shape = RoundedCornerShape(12.dp)
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text("International UPI is here", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.Black)
                        Text("Scan and pay at select merchant\nstores abroad now", fontSize = 14.sp, color = Color.Gray)
                    }
                    Text("ACTIVATE", color = Color(0xFF5f259f), fontWeight = FontWeight.Bold, fontSize = 14.sp, modifier = Modifier.clickable { })
                }
            }
            
            // UPI IDs
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 4.dp),
                colors = CardDefaults.cardColors(containerColor = Color.White),
                shape = RoundedCornerShape(12.dp)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text("UPI IDs", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.Black)
                    Text("Below UPI IDs can only be used with this account", fontSize = 14.sp, color = Color.Gray)
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    EditableUpiIdRow("9876543210-2@axl", true)
                    EditableUpiIdRow("9876543210-2@ybl", true)
                    EditableUpiIdRow("9876543210-2@ibl", false)
                    EditableUpiIdRow("johndoe123@ibl", true)
                    EditableUpiIdRow("johndoe123@axl", false)
                    EditableUpiIdRow("johndoe123@ybl", false)
                }
            }
            

            Spacer(modifier = Modifier.height(16.dp))
            Button(
                onClick = {
                    val newAccount = BankAccount(
                        bankName = bankName,
                        accountName = name,
                        bankDesc = bankDesc,
                        type = accType,
                        branch = branch,
                        ifsc = ifsc,
                        balance = balance.toDoubleOrNull() ?: 0.0
                    )
                    viewModel.addBankAccount(newAccount)
                    onBack()
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp)
                    .height(52.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF5f259f)),
                shape = RoundedCornerShape(26.dp)
            ) {
                Text("SAVE ACCOUNT", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.White)
            }
            Spacer(modifier = Modifier.height(24.dp))
        }
    }
}


@Composable
fun EditableUpiIdRow(id: String, isActivate: Boolean) {
    var upiId by remember { mutableStateOf(id) }
    Column {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(vertical = 12.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            BasicTextField(value = upiId, onValueChange = { upiId = it }, textStyle = TextStyle(fontSize = 16.sp, color = Color.Black), modifier = Modifier.weight(1f))
            if (isActivate) {
                Text("ACTIVATE", color = Color(0xFF5f259f), fontWeight = FontWeight.Bold, fontSize = 14.sp, modifier = Modifier.clickable { })
            } else {
                Icon(Icons.Default.DeleteOutline, contentDescription = "Delete", tint = Color.Gray, modifier = Modifier.clickable { })
            }
        }
        HorizontalDivider(color = Color(0xFFF0F0F0))
    }
}
