package com.example.ui.screens

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Receipt
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.collectAsState
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.ui.PrankViewModel
import java.text.SimpleDateFormat
import java.util.*
import com.example.R

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SendMoneyScreen(
    viewModel: PrankViewModel,
    onBack: () -> Unit,
    onNewPayment: () -> Unit,
    onContactSelect: (String) -> Unit
) {
    val transactions by viewModel.allTransactions.collectAsState()
    
    // Group transactions by payee name to create recent chats
    val recentChats = transactions.groupBy { it.receiverName }.map { (name, txs) ->
        val latest = txs.maxByOrNull { it.timestamp }!!
        latest
    }.sortedByDescending { it.timestamp }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { 
                    Column {
                        Text("Send Money", fontWeight = FontWeight.Bold, fontSize = 20.sp)
                        Text("to any UPI app", color = Color.Gray, fontSize = 14.sp)
                    }
                },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.White)
            )
        },
        floatingActionButton = {
            ExtendedFloatingActionButton(
                onClick = onNewPayment,
                containerColor = Color(0xFF5f259f),
                contentColor = Color.White,
                icon = { Icon(Icons.Default.Add, contentDescription = "New Payment") },
                text = { Text("New Payment", fontWeight = FontWeight.Bold) }
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
                    .background(Color(0xFFF3F4F6), RoundedCornerShape(24.dp))
                    .padding(horizontal = 16.dp, vertical = 4.dp)
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.Search, contentDescription = "Search", tint = Color.Gray)
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("Start a new payment from h...", color = Color.Gray)
                }
            }

            // Split Expenses
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(Icons.Default.Receipt, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(32.dp))
                Spacer(modifier = Modifier.width(16.dp))
                Text("Split expenses", fontSize = 18.sp)
                Spacer(modifier = Modifier.width(8.dp))
                Box(
                    modifier = Modifier
                        .background(Color(0xFF1976D2), RoundedCornerShape(4.dp))
                        .padding(horizontal = 6.dp, vertical = 2.dp)
                ) {
                    Text("New", color = Color.White, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                }
            }
            
            HorizontalDivider(color = Color(0xFFEEEEEE), thickness = 1.dp)
            
            Text(
                text = "PAYMENTS & CHAT",
                color = Color.Gray,
                fontSize = 12.sp,
                fontWeight = FontWeight.Bold,
                modifier = Modifier.padding(16.dp)
            )
            
            LazyColumn(
                modifier = Modifier.fillMaxSize()
            ) {
                items(recentChats) { tx ->
                    val dateFormat = SimpleDateFormat("dd/MM", Locale.getDefault())
                    val timeFormat = SimpleDateFormat("hh:mm a", Locale.getDefault())
                    val dateStr = if (System.currentTimeMillis() - tx.timestamp < 86400000) {
                        timeFormat.format(Date(tx.timestamp))
                    } else {
                        dateFormat.format(Date(tx.timestamp))
                    }
                    
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable { onContactSelect(tx.receiverName) }
                            .padding(horizontal = 16.dp, vertical = 12.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Box(
                            modifier = Modifier
                                .size(48.dp)
                                .clip(CircleShape)
                                .background(Color(0xFF78909C)),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(tx.receiverName.take(1).uppercase(), color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                            // Small UPI icon placeholder at bottom right
                            Box(
                                modifier = Modifier
                                    .align(Alignment.BottomEnd)
                                    .background(Color.White, CircleShape)
                                    .padding(2.dp)
                            ) {
                                Text("UPI", fontSize = 6.sp, fontWeight = FontWeight.Bold, color = Color.Black)
                            }
                        }
                        
                        Spacer(modifier = Modifier.width(16.dp))
                        
                        Column(modifier = Modifier.weight(1f)) {
                            Text(tx.receiverName, fontSize = 16.sp, color = Color.Black)
                            Text("You: ₹${tx.amount.toInt()} - Sent Securely", fontSize = 14.sp, color = Color.Gray)
                        }
                        
                        Text(dateStr, fontSize = 12.sp, color = Color.Gray)
                    }
                }
            }
        }
    }
}
