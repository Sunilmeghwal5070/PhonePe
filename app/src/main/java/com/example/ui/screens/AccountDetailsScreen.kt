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
import androidx.compose.material.icons.filled.Add
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import coil.compose.AsyncImage
import androidx.compose.ui.draw.clip
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.ui.text.TextStyle
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

import com.example.ui.PrankViewModel
import androidx.compose.runtime.collectAsState

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AccountDetailsScreen(
    accountId: String,
    isEditable: Boolean,
    viewModel: PrankViewModel,
    onBack: () -> Unit,
    onNavigateToCheckBalance: () -> Unit
) {
    val bankAccounts by viewModel.bankAccounts.collectAsState()
    val account = bankAccounts.find { it.id == accountId }
    var isEditableState by remember { mutableStateOf(isEditable) }
    
    var name by remember { mutableStateOf(account?.accountName ?: "John Doe") }
    var bankDesc by remember { mutableStateOf(account?.bankDesc ?: "Bank") }
    var accType by remember { mutableStateOf(account?.type ?: ": Saving Account") }
    var branch by remember { mutableStateOf(account?.branch ?: ": MAIN") }
    var ifsc by remember { mutableStateOf(account?.ifsc ?: ": IFSC") }
    var pin by remember { mutableStateOf(account?.pin ?: "1234") }
    var isEditingPin by remember { mutableStateOf(false) }
    var upiIds by remember { mutableStateOf(account?.upiIds ?: listOf()) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Account Details", fontWeight = FontWeight.Bold, fontSize = 20.sp) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    if (isEditableState) {
                        TextButton(onClick = {
                            account?.let {
                                viewModel.updateBankAccount(it.copy(
                                    accountName = name,
                                    bankDesc = bankDesc,
                                    type = accType,
                                    branch = branch,
                                    ifsc = ifsc,
                                    pin = pin,
                                    upiIds = upiIds
                                ))
                            }
                            onBack()
                        }) {
                            Text("SAVE", color = Color(0xFF5f259f), fontWeight = FontWeight.Bold)
                        }
                    } else {
                        IconButton(onClick = { isEditableState = true }) {
                            Icon(Icons.AutoMirrored.Filled.HelpOutline, contentDescription = "Edit")
                        }
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
                        // Bank Logo
                        com.example.ui.components.BankLogo(bankName = account?.bankName ?: "Bank", size = 40.dp)
                        
                        Spacer(modifier = Modifier.width(16.dp))
                        
                        Column {
                            BasicTextField(value = name, onValueChange = { name = it }, textStyle = TextStyle(fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color.Black), enabled = isEditableState)
                            BasicTextField(value = bankDesc, onValueChange = { bankDesc = it }, textStyle = TextStyle(fontSize = 14.sp, color = Color.Gray), enabled = isEditableState)
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
                    
                    Column {
                        Row(verticalAlignment = Alignment.Top, modifier = Modifier.fillMaxWidth()) {
                            Text("Type", fontSize = 14.sp, color = Color.Gray, modifier = Modifier.width(80.dp))
                            BasicTextField(value = accType, onValueChange = { accType = it }, textStyle = TextStyle(fontSize = 14.sp, color = Color.Gray), modifier = Modifier.weight(1f), enabled = isEditableState)
                        }
                        Spacer(modifier = Modifier.height(12.dp))
                        Row(verticalAlignment = Alignment.Top, modifier = Modifier.fillMaxWidth()) {
                            Text("Branch", fontSize = 14.sp, color = Color.Gray, modifier = Modifier.width(80.dp))
                            BasicTextField(value = branch, onValueChange = { branch = it }, textStyle = TextStyle(fontSize = 14.sp, color = Color.Gray), modifier = Modifier.weight(1f), enabled = isEditableState)
                        }
                        Spacer(modifier = Modifier.height(12.dp))
                        Row(verticalAlignment = Alignment.Top, modifier = Modifier.fillMaxWidth()) {
                            Text("IFSC", fontSize = 14.sp, color = Color.Gray, modifier = Modifier.width(80.dp))
                            BasicTextField(value = ifsc, onValueChange = { ifsc = it }, textStyle = TextStyle(fontSize = 14.sp, color = Color.Gray), modifier = Modifier.weight(1f), enabled = isEditableState)
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
                        if (isEditable || isEditingPin) {
                            BasicTextField(
                                value = pin,
                                onValueChange = { if (it.length <= 4) pin = it },
                                textStyle = TextStyle(fontSize = 14.sp, color = Color.Gray)
                            )
                        } else {
                            Text("4 digit UPI PIN exists", fontSize = 14.sp, color = Color.Gray)
                        }
                    }
                    Row {
                        Text("RESET", color = Color(0xFF5f259f), fontWeight = FontWeight.Bold, fontSize = 14.sp, modifier = Modifier.clickable { isEditingPin = !isEditingPin })
                        Spacer(modifier = Modifier.width(16.dp))
                        Text(if (isEditingPin) "DONE" else "CHANGE", color = Color(0xFF5f259f), fontWeight = FontWeight.Bold, fontSize = 14.sp, modifier = Modifier.clickable { 
                            if (isEditingPin) {
                                if (account != null) {
                                    viewModel.updateBankAccount(account.copy(pin = pin))
                                }
                            }
                            isEditingPin = !isEditingPin 
                        })
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
                    Text("CHECK BALANCE", color = Color(0xFF5f259f), fontWeight = FontWeight.Bold, fontSize = 14.sp, modifier = Modifier.clickable { onNavigateToCheckBalance() })
                    Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(16.dp))
                }
            }
            
            // Add Balance Card (Unity Ads)
            val context = androidx.compose.ui.platform.LocalContext.current
            val activity = context as? android.app.Activity
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
                        .clickable { 
                            if (activity != null) {
                                com.example.ui.UnityAdsManager.showRewardedAd(activity) {
                                    if (account != null) {
                                        viewModel.updateBankAccount(account.copy(balance = account.balance + 500))
                                        android.widget.Toast.makeText(context, "₹500 added to your account!", android.widget.Toast.LENGTH_SHORT).show()
                                    }
                                }
                            }
                        }
                        .padding(16.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("ADD ₹500 BALANCE (WATCH AD)", color = Color(0xFF388E3C), fontWeight = FontWeight.Bold, fontSize = 14.sp)
                    Icon(Icons.Default.Add, contentDescription = null, tint = Color(0xFF388E3C), modifier = Modifier.size(16.dp))
                }
            }
            

            

            if (isEditableState && account != null) {
                Spacer(modifier = Modifier.height(16.dp))
                Button(
                    onClick = {
                        val updated = account.copy(
                            accountName = name,
                            bankDesc = bankDesc,
                            type = accType,
                            branch = branch,
                            ifsc = ifsc,
                            pin = pin,
                            upiIds = upiIds
                        )
                        viewModel.updateBankAccount(updated)
                        onBack()
                    },
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp)
                        .height(52.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF5f259f)),
                    shape = RoundedCornerShape(26.dp)
                ) {
                    Text("SAVE CHANGES", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.White)
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
                    
                    upiIds.forEachIndexed { index, upiId ->
                        var isEditingUpi by remember { mutableStateOf(false) }
                        var editedUpi by remember { mutableStateOf(upiId) }
                        
                        Column {
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(vertical = 12.dp),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                if (isEditingUpi || isEditableState) {
                                    BasicTextField(
                                        value = editedUpi,
                                        onValueChange = { editedUpi = it },
                                        textStyle = TextStyle(fontSize = 16.sp, color = Color.Black),
                                        modifier = Modifier
                                            .weight(1f)
                                            .border(1.dp, Color.LightGray, RoundedCornerShape(4.dp))
                                            .padding(8.dp)
                                    )
                                    Spacer(modifier = Modifier.width(8.dp))
                                    Icon(Icons.Default.CheckCircle, contentDescription = "Save", tint = Color(0xFF388E3C), modifier = Modifier.clickable {
                                        val newList = upiIds.toMutableList()
                                        newList[index] = editedUpi
                                        upiIds = newList
                                        isEditingUpi = false
                                    })
                                } else {
                                    Text(upiId, fontSize = 16.sp, color = Color.Black, modifier = Modifier.weight(1f))
                                    if (index % 2 == 0) {
                                        Text("ACTIVATE", color = Color(0xFF5f259f), fontWeight = FontWeight.Bold, fontSize = 14.sp, modifier = Modifier.clickable { })
                                    } else {
                                        Icon(Icons.Default.DeleteOutline, contentDescription = "Delete", tint = Color.Gray, modifier = Modifier.clickable { })
                                    }
                                    Spacer(modifier = Modifier.width(8.dp))
                                    Icon(Icons.Default.Edit, contentDescription = "Edit", tint = Color.Gray, modifier = Modifier.clickable { isEditingUpi = true })
                                }
                            }
                            HorizontalDivider(color = Color(0xFFF0F0F0))
                        }
                    }
                }
            }
            
            // Edit Nickname
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
                        .clickable { }
                        .padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(Icons.Default.Edit, contentDescription = null, tint = Color.Black)
                    Spacer(modifier = Modifier.width(16.dp))
                    Text("Edit Nickname", fontSize = 16.sp, color = Color.Black)
                }
            }
            
            // Unlink Bank Account
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
                        .clickable { viewModel.deleteBankAccount(accountId); onBack() }
                        .padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(Icons.Default.DeleteOutline, contentDescription = null, tint = Color(0xFFD32F2F))
                    Spacer(modifier = Modifier.width(16.dp))
                    Text("Unlink Bank Account", fontSize = 16.sp, color = Color(0xFFD32F2F))
                }
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            
            // Powered by UPI
            Box(modifier = Modifier.fillMaxWidth(), contentAlignment = Alignment.Center) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Text("POWERED BY", fontSize = 10.sp, color = Color.Gray, fontWeight = FontWeight.Bold)
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        coil.compose.AsyncImage(
                            model = coil.request.ImageRequest.Builder(androidx.compose.ui.platform.LocalContext.current)
                                .data("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/UPI-Logo-vector.svg/1024px-UPI-Logo-vector.svg.png")
                                .crossfade(true)
                                .build(),
                            contentDescription = "UPI",
                            modifier = Modifier.height(24.dp),
                            contentScale = androidx.compose.ui.layout.ContentScale.Fit
                        )
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(32.dp))
        }
    }
}


