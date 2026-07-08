package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.HelpOutline
import androidx.compose.material.icons.automirrored.filled.CallMade
import androidx.compose.material.icons.automirrored.filled.CallReceived
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Tune
import androidx.compose.material.icons.filled.Error
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.ui.PrankViewModel
import com.example.data.PrankTransaction
import java.text.SimpleDateFormat
import java.util.*
import androidx.compose.ui.text.style.TextOverflow

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HistoryScreen(
    viewModel: PrankViewModel,
    onNavigateToReceipt: (Int) -> Unit
) {
    val transactions by viewModel.allTransactions.collectAsState()
    var searchQuery by remember { mutableStateOf("") }
    
    val filteredTransactions = remember(transactions, searchQuery) {
        if (searchQuery.isBlank()) {
            transactions.sortedByDescending { it.timestamp }
        } else {
            transactions.filter {
                it.receiverName.contains(searchQuery, ignoreCase = true) ||
                it.receiverPhone.contains(searchQuery) ||
                it.receiverUpiId.contains(searchQuery, ignoreCase = true)
            }.sortedByDescending { it.timestamp }
        }
    }

    val groupedTransactions = remember(filteredTransactions) {
        val sdfMonthYear = SimpleDateFormat("MMMM yyyy", Locale.getDefault())
        filteredTransactions.groupBy { tx ->
            sdfMonthYear.format(Date(tx.timestamp))
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("History", fontWeight = FontWeight.Bold, color = Color.Black, fontSize = 22.sp) },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = Color.White
                ),
                actions = {
                    IconButton(onClick = { }) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.HelpOutline, 
                            contentDescription = "Help", 
                            tint = Color.Black
                        )
                    }
                }
            )
        },
        containerColor = Color.White
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .background(Color.White)
        ) {
            // Search Bar
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 8.dp)
                    .background(Color(0xFFF3F4F6), RoundedCornerShape(24.dp))
                    .padding(horizontal = 16.dp, vertical = 2.dp)
            ) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Icon(
                        imageVector = Icons.Default.Search,
                        contentDescription = "Search",
                        tint = Color.Gray,
                        modifier = Modifier.size(24.dp)
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    
                    androidx.compose.foundation.text.BasicTextField(
                        value = searchQuery,
                        onValueChange = { searchQuery = it },
                        modifier = Modifier
                            .weight(1f)
                            .padding(vertical = 14.dp),
                        singleLine = true,
                        textStyle = androidx.compose.ui.text.TextStyle(
                            fontSize = 16.sp,
                            color = Color.Black
                        ),
                        decorationBox = { innerTextField ->
                            if (searchQuery.isEmpty()) {
                                Text(
                                    text = "Search",
                                    color = Color.Gray,
                                    fontSize = 16.sp
                                )
                            }
                            innerTextField()
                        }
                    )
                    
                    Icon(
                        imageVector = Icons.Default.Tune,
                        contentDescription = "Filter",
                        tint = Color.Black,
                        modifier = Modifier.size(24.dp)
                    )
                }
            }
            
            Spacer(modifier = Modifier.height(8.dp))

            if (filteredTransactions.isEmpty()) {
                // Empty State
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = if (searchQuery.isNotBlank()) "No matches found" else "History is empty",
                        color = Color.Gray
                    )
                }
            } else {
                LazyColumn(
                    modifier = Modifier.fillMaxWidth(),
                    contentPadding = PaddingValues(bottom = 80.dp)
                ) {
                    groupedTransactions.forEach { (monthYear, txs) ->
                        // Month Header
                        item {
                            val totalAmount = txs.sumOf { 
                                if (it.type == "RECEIVED" && it.status != "FAILED") it.amount else 0.0 
                            }
                            val isPositive = totalAmount > 0
                            
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .background(Color(0xFFF9F9FB))
                                    .padding(horizontal = 16.dp, vertical = 12.dp),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Text(
                                    text = monthYear,
                                    color = Color.Gray,
                                    fontSize = 14.sp,
                                    fontWeight = FontWeight.Medium
                                )
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    if (isPositive) {
                                        Text(
                                            text = "+ ₹${totalAmount.toInt()}",
                                            color = Color(0xFF2E7D32),
                                            fontSize = 14.sp,
                                            fontWeight = FontWeight.Medium
                                        )
                                    } else {
                                        val debited = txs.sumOf { if (it.type == "PAID" && it.status != "FAILED") it.amount else 0.0 }
                                        Text(
                                            text = "₹${debited.toInt()}",
                                            color = Color.Black,
                                            fontSize = 14.sp,
                                            fontWeight = FontWeight.Medium
                                        )
                                    }
                                    Spacer(modifier = Modifier.width(4.dp))
                                    Icon(
                                        imageVector = Icons.AutoMirrored.Filled.KeyboardArrowRight,
                                        contentDescription = null,
                                        tint = Color.Gray,
                                        modifier = Modifier.size(16.dp)
                                    )
                                }
                            }
                        }
                        
                        // Transaction Items
                        items(txs.size) { index ->
                            val tx = txs[index]
                            HistoryItemRow(tx = tx, onClick = { onNavigateToReceipt(tx.id) })
                            if (index < txs.size - 1) {
                                HorizontalDivider(
                                    modifier = Modifier.padding(start = 76.dp),
                                    thickness = 1.dp,
                                    color = Color(0xFFF0F0F0)
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun HistoryItemRow(tx: PrankTransaction, onClick: () -> Unit) {
    val sdfDayMonth = remember { SimpleDateFormat("dd MMM", Locale.getDefault()) }
    val isReceived = tx.type == "RECEIVED"
    val isFailed = tx.status == "FAILED"
    
    val dateStr = remember(tx.timestamp) { 
        val now = System.currentTimeMillis()
        val diff = now - tx.timestamp
        if (diff < 24 * 60 * 60 * 1000) {
            val hours = diff / (60 * 60 * 1000)
            if (hours > 0) "$hours hours ago" else "Just now"
        } else {
            sdfDayMonth.format(Date(tx.timestamp))
        }
    }

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .background(Color.White)
            .clickable { onClick() }
            .padding(horizontal = 16.dp, vertical = 16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        // Icon Box
        Box(
            modifier = Modifier
                .size(44.dp)
                .background(Color(0xFFF3F4F6), RoundedCornerShape(12.dp)),
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = if (isReceived) Icons.AutoMirrored.Filled.CallReceived else Icons.AutoMirrored.Filled.CallMade,
                contentDescription = null,
                tint = Color.Black,
                modifier = Modifier.size(24.dp)
            )
        }
        
        Spacer(modifier = Modifier.width(16.dp))
        
        // Middle Column
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = if (isReceived) "Received from" else "Paid to",
                color = Color.Gray,
                fontSize = 12.sp
            )
            Text(
                text = tx.receiverName,
                color = Color.Black,
                fontSize = 16.sp,
                fontWeight = FontWeight.Medium,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
            Spacer(modifier = Modifier.height(2.dp))
            Text(
                text = dateStr,
                color = Color.Gray,
                fontSize = 12.sp
            )
        }
        
        Spacer(modifier = Modifier.width(8.dp))
        
        // Right Column
        Column(horizontalAlignment = Alignment.End) {
            Text(
                text = if (isReceived) "+ ₹${tx.amount.toInt()}" else "₹${tx.amount.toInt()}",
                color = if (isReceived) Color(0xFF2E7D32) else Color.Black,
                fontSize = 16.sp,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(4.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
                if (isFailed) {
                    Text("Failed", color = Color.Gray, fontSize = 12.sp)
                    Spacer(modifier = Modifier.width(4.dp))
                    Icon(
                        imageVector = Icons.Default.Error, // Red exclamation
                        contentDescription = "Failed",
                        tint = Color(0xFFD32F2F),
                        modifier = Modifier.size(14.dp)
                    )
                } else {
                    Text(
                        text = if (isReceived) "Credited to" else "Debited from",
                        color = Color.Gray,
                        fontSize = 12.sp
                    )
                    Spacer(modifier = Modifier.width(4.dp))
                    // PhonePe Icon Placeholder (S logo)
                    Box(
                        modifier = Modifier
                            .size(14.dp)
                            .background(Color.Transparent),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = "S", 
                            color = Color(0xFF5f259f), 
                            fontSize = 10.sp, 
                            fontWeight = FontWeight.ExtraBold, 
                            fontStyle = androidx.compose.ui.text.font.FontStyle.Italic
                        )
                    }
                }
            }
        }
    }
}
