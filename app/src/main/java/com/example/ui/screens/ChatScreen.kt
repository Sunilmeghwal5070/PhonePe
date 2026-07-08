package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.HelpOutline
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Alarm
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.Dialpad
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material.icons.filled.ArrowCircleRight
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.collectAsState
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.ui.PrankViewModel
import java.text.SimpleDateFormat
import java.util.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ChatScreen(
    contactName: String,
    viewModel: PrankViewModel,
    onBack: () -> Unit,
    onPayAmount: (String, String) -> Unit
) {
    var inputText by remember { mutableStateOf("") }
    val transactions by viewModel.allTransactions.collectAsState()
    
    // Filter transactions by this contact
    val contactTransactions = transactions.filter { 
        it.receiverName.equals(contactName, ignoreCase = true) 
    }.sortedBy { it.timestamp }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { 
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Box(
                            modifier = Modifier
                                .size(40.dp)
                                .background(Color.Gray, CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(contactName.take(1).uppercase(), color = Color.White, fontWeight = FontWeight.Bold)
                        }
                        Spacer(modifier = Modifier.width(12.dp))
                        Column {
                            Text(contactName, fontWeight = FontWeight.Bold, fontSize = 18.sp)
                            Text("+91XXXXX", color = Color.Gray, fontSize = 12.sp)
                        }
                    }
                },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    IconButton(onClick = { }) { Icon(Icons.Default.Alarm, contentDescription = "History") }
                    IconButton(onClick = { }) { Icon(Icons.AutoMirrored.Filled.HelpOutline, contentDescription = "Help") }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.White)
            )
        },
        containerColor = Color.White
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
            LazyColumn(
                modifier = Modifier
                    .weight(1f)
                    .padding(horizontal = 16.dp)
            ) {
                // Group by date
                val grouped = contactTransactions.groupBy { 
                    SimpleDateFormat("MMMM dd, yyyy", Locale.getDefault()).format(Date(it.timestamp))
                }
                
                grouped.forEach { (date, txs) ->
                    item {
                        Text(
                            text = date,
                            color = Color.Gray,
                            fontSize = 12.sp,
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(vertical = 16.dp),
                            textAlign = TextAlign.Center
                        )
                    }
                    items(txs) { tx ->
                        val isPaid = tx.type == "PAID"
                        val timeStr = SimpleDateFormat("h:mm a", Locale.getDefault()).format(Date(tx.timestamp))
                        
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = if (isPaid) Arrangement.End else Arrangement.Start
                        ) {
                            if (!isPaid) {
                                Box(modifier = Modifier.size(32.dp).background(Color(0xFF00897B), CircleShape), contentAlignment = Alignment.Center) {
                                    Text(contactName.take(1).uppercase(), color = Color.White, fontSize = 14.sp)
                                }
                                Spacer(modifier = Modifier.width(8.dp))
                            }
                            
                            Card(
                                modifier = Modifier.width(240.dp).padding(bottom = 16.dp),
                                shape = RoundedCornerShape(
                                    topStart = 16.dp, topEnd = 16.dp,
                                    bottomStart = if (isPaid) 16.dp else 0.dp,
                                    bottomEnd = if (isPaid) 0.dp else 16.dp
                                ),
                                colors = CardDefaults.cardColors(
                                    containerColor = if (isPaid) Color(0xFFF3E5F5) else Color(0xFFF5F5F5)
                                )
                            ) {
                                Column(modifier = Modifier.padding(16.dp)) {
                                    Row(
                                        modifier = Modifier.fillMaxWidth(),
                                        horizontalArrangement = Arrangement.SpaceBetween,
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Text("₹${tx.amount.toInt()}", fontSize = 28.sp, fontWeight = FontWeight.Bold, color = Color.Black)
                                        Icon(Icons.Default.ArrowCircleRight, contentDescription = null, tint = Color.LightGray, modifier = Modifier.size(32.dp))
                                    }
                                    Spacer(modifier = Modifier.height(8.dp))
                                    Row(
                                        modifier = Modifier.fillMaxWidth(),
                                        horizontalArrangement = Arrangement.SpaceBetween,
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Row(verticalAlignment = Alignment.CenterVertically) {
                                            Icon(Icons.Default.CheckCircle, contentDescription = null, tint = Color(0xFF388E3C), modifier = Modifier.size(16.dp))
                                            Spacer(modifier = Modifier.width(4.dp))
                                            Text(if (isPaid) "PAID" else "RECEIVED", color = Color.Gray, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                                        }
                                        Text(timeStr, color = Color.Gray, fontSize = 12.sp)
                                    }
                                }
                            }
                            
                            if (isPaid) {
                                Spacer(modifier = Modifier.width(8.dp))
                                Box(modifier = Modifier.size(32.dp).background(Color(0xFF607D8B), CircleShape), contentAlignment = Alignment.Center) {
                                    Text("YM", color = Color.White, fontSize = 14.sp)
                                }
                            }
                        }
                    }
                }
            }
            
            // Suggestions
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 8.dp),
                horizontalArrangement = Arrangement.Center
            ) {
                SuggestionChip("Hi", onClick = {})
                Spacer(modifier = Modifier.width(8.dp))
                SuggestionChip("👋", onClick = {})
                Spacer(modifier = Modifier.width(8.dp))
                SuggestionChip("Send ₹1", onClick = { onPayAmount("1", contactName) })
            }
            
            HorizontalDivider(color = Color(0xFFEEEEEE), thickness = 1.dp)
            
            // Input Area
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 12.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                TextField(
                    value = inputText,
                    onValueChange = { inputText = it },
                    placeholder = { Text("Enter amount or chat", color = Color.Gray) },
                    modifier = Modifier.weight(1f),
                    colors = TextFieldDefaults.colors(
                        focusedContainerColor = Color.Transparent,
                        unfocusedContainerColor = Color.Transparent,
                        focusedIndicatorColor = Color.Transparent,
                        unfocusedIndicatorColor = Color.Transparent
                    ),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Text)
                )
                
                IconButton(onClick = {}) { Icon(Icons.Default.Dialpad, contentDescription = "Dialpad") }
                IconButton(onClick = {}) { Icon(Icons.Default.Add, contentDescription = "Add") }
                IconButton(onClick = { 
                    if (inputText.isNotEmpty()) {
                        if (inputText.all { it.isDigit() }) {
                            onPayAmount(inputText, contactName)
                        }
                        inputText = ""
                    }
                }) { 
                    Icon(Icons.AutoMirrored.Filled.Send, contentDescription = "Send", tint = Color.Gray) 
                }
            }
        }
    }
}

@Composable
fun SuggestionChip(text: String, onClick: () -> Unit) {
    Box(
        modifier = Modifier
            .border(1.dp, Color.LightGray, RoundedCornerShape(16.dp))
            .clickable(onClick = onClick)
            .padding(horizontal = 16.dp, vertical = 8.dp)
    ) {
        Text(text, fontSize = 14.sp, color = Color.Black)
    }
}
