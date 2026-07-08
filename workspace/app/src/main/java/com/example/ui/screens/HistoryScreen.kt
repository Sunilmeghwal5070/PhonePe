package com.example.ui.screens

import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.HelpOutline
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Tune
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.data.PrankTransaction
import com.example.ui.PrankViewModel
import com.example.ui.theme.*
import java.text.SimpleDateFormat
import java.util.*

@OptIn(ExperimentalMaterial3Api::class, ExperimentalFoundationApi::class)
@Composable
fun HistoryScreen(
    viewModel: PrankViewModel,
    onNavigateToReceipt: (Int) -> Unit
) {
    val transactions by viewModel.allTransactions.collectAsState()
    var searchQuery by remember { mutableStateOf("") }

    val filteredTransactions = remember(transactions, searchQuery) {
        if (searchQuery.isBlank()) {
            transactions
        } else {
            transactions.filter {
                it.receiverName.contains(searchQuery, ignoreCase = true) ||
                it.receiverPhone.contains(searchQuery) ||
                it.receiverUpiId.contains(searchQuery, ignoreCase = true)
            }
        }
    }

    // Group transactions by Month-Year
    val groupedTransactions = remember(filteredTransactions) {
        val format = SimpleDateFormat("MMMM yyyy", Locale.US)
        filteredTransactions
            .sortedByDescending { it.timestamp }
            .groupBy { format.format(Date(it.timestamp)) }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { 
                    Text(
                        text = "History", 
                        fontWeight = FontWeight.Bold, 
                        fontSize = 22.sp, 
                        color = Color.Black
                    ) 
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = Color.White
                ),
                actions = {
                    IconButton(onClick = { /* Help */ }) {
                        Icon(
                            imageVector = Icons.Default.HelpOutline, 
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
        ) {
            // Search Bar
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 8.dp)
            ) {
                OutlinedTextField(
                    value = searchQuery,
                    onValueChange = { searchQuery = it },
                    placeholder = { Text("Search", color = Color.Gray, fontSize = 16.sp) },
                    leadingIcon = { 
                        Icon(
                            imageVector = Icons.Default.Search, 
                            contentDescription = "Search", 
                            tint = Color.Gray,
                            modifier = Modifier.size(28.dp)
                        ) 
                    },
                    trailingIcon = {
                        Icon(
                            imageVector = Icons.Default.Tune,
                            contentDescription = "Filter",
                            tint = Color.Black,
                            modifier = Modifier.padding(end = 8.dp).size(24.dp)
                        )
                    },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(56.dp),
                    shape = RoundedCornerShape(32.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = Color.Transparent,
                        unfocusedBorderColor = Color.Transparent,
                        focusedContainerColor = Color(0xFFF3F4F6),
                        unfocusedContainerColor = Color(0xFFF3F4F6)
                    ),
                    singleLine = true
                )
            }

            Spacer(modifier = Modifier.height(16.dp))

            LazyColumn(
                modifier = Modifier.fillMaxWidth()
            ) {
                groupedTransactions.forEach { (monthYear, txList) ->
                    stickyHeader {
                        // Calculate month total (just summing up for prank purposes)
                        val total = txList.sumOf { it.amount }
                        val isPositive = txList.firstOrNull()?.type == "RECEIVED"
                        
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .background(Color(0xFFF9FAFB))
                                .padding(horizontal = 16.dp, vertical = 12.dp),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text(
                                text = monthYear,
                                fontSize = 15.sp,
                                color = Color.Gray
                            )
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Text(
                                    text = if (isPositive) "+ ₹${total.toInt()}" else "₹${total.toInt()}",
                                    fontSize = 15.sp,
                                    color = if (isPositive) PhonePeSuccessGreen else Color.Black,
                                    fontWeight = FontWeight.Medium
                                )
                                Spacer(modifier = Modifier.width(4.dp))
                                Text(">", color = Color.Gray, fontSize = 14.sp)
                            }
                        }
                    }

                    items(txList) { tx ->
                        HistoryItemRow(tx = tx, onClick = { onNavigateToReceipt(tx.id) })
                    }
                }
            }
        }
    }
}

@Composable
fun HistoryItemRow(
    tx: PrankTransaction,
    onClick: () -> Unit
) {
    val isReceived = tx.type == "RECEIVED"
    
    val sdf = remember { SimpleDateFormat("dd MMM", Locale.US) }
    
    // Logic for "2 hours ago" vs "04 Jul"
    val diffMillis = System.currentTimeMillis() - tx.timestamp
    val hours = diffMillis / (1000 * 60 * 60)
    val dateStr = if (hours in 1..24) {
        "$hours hours ago"
    } else {
        sdf.format(Date(tx.timestamp))
    }

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() }
            .background(Color.White)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp, vertical = 16.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Row(
                modifier = Modifier.weight(1f),
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Icon box
                Box(
                    modifier = Modifier
                        .size(48.dp)
                        .clip(RoundedCornerShape(12.dp))
                        .background(Color(0xFFF3F4F6)),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = if (isReceived) "↙" else "↗",
                        fontSize = 24.sp,
                        color = Color.Black,
                        fontWeight = FontWeight.Light
                    )
                }

                Spacer(modifier = Modifier.width(16.dp))

                // Details (Left side text)
                Column {
                    Text(
                        text = if (isReceived) "Received from" else if (tx.receiverUpiId.contains("google", ignoreCase = true)) "Payment to" else "Paid to",
                        fontSize = 13.sp,
                        color = Color.Gray
                    )
                    Spacer(modifier = Modifier.height(2.dp))
                    Text(
                        text = tx.receiverName,
                        fontSize = 16.sp,
                        fontWeight = FontWeight.Normal,
                        color = Color.Black,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis
                    )
                    Spacer(modifier = Modifier.height(2.dp))
                    Text(
                        text = dateStr,
                        fontSize = 13.sp,
                        color = Color.Gray
                    )
                }
            }

            // Right side (Amount and Status)
            Column(
                horizontalAlignment = Alignment.End,
                modifier = Modifier.padding(start = 12.dp)
            ) {
                Text(
                    text = if (isReceived) "+ ₹${tx.amount.toInt()}" else "₹${tx.amount.toInt()}",
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold,
                    color = if (isReceived) PhonePeSuccessGreen else Color.Black
                )
                Spacer(modifier = Modifier.height(4.dp))
                Row(verticalAlignment = Alignment.CenterVertically) {
                    if (tx.status == "FAILED") {
                        Text(
                            text = "Failed",
                            fontSize = 13.sp,
                            color = Color.Gray
                        )
                        Spacer(modifier = Modifier.width(4.dp))
                        Box(
                            modifier = Modifier
                                .size(14.dp)
                                .clip(CircleShape)
                                .background(PhonePeFailedRed),
                            contentAlignment = Alignment.Center
                        ) {
                            Text("!", color = Color.White, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                        }
                    } else {
                        Text(
                            text = if (isReceived) "Credited to" else "Debited from",
                            fontSize = 13.sp,
                            color = Color.Gray
                        )
                        Spacer(modifier = Modifier.width(4.dp))
                        // Fake UPI/Bank Icon (squiggly symbol used in placeholder)
                        Box(
                            modifier = Modifier
                                .size(14.dp)
                                .clip(RoundedCornerShape(4.dp))
                                .background(Color.Transparent),
                            contentAlignment = Alignment.Center
                        ) {
                            Text("∽", color = PhonePePurple, fontSize = 14.sp, fontWeight = FontWeight.Bold)
                        }
                    }
                }
            }
        }
        
        // Divider
        Divider(
            color = Color(0xFFF3F4F6),
            thickness = 1.dp,
            modifier = Modifier.padding(start = 80.dp)
        )
    }
}
