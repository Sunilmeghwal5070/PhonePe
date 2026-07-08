package com.example.ui.screens

import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.ui.theme.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SearchScreen(
    onCreatePrank: () -> Unit
) {
    val context = LocalContext.current
    var searchQuery by remember { mutableStateOf("") }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFFF5F6FA))
    ) {
        // Search Top Bar (Matches PhonePe search style)
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .background(Color.White)
                .padding(horizontal = 16.dp, vertical = 12.dp)
        ) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(48.dp)
                    .clip(RoundedCornerShape(24.dp))
                    .background(Color(0xFFF1F3F6))
                    .border(1.dp, Color(0xFFE2E8F0), RoundedCornerShape(24.dp))
                    .padding(horizontal = 16.dp)
            ) {
                Icon(
                    imageVector = Icons.Default.Search,
                    contentDescription = "Search icon",
                    tint = PhonePeTextMuted,
                    modifier = Modifier.size(20.dp)
                )
                
                Spacer(modifier = Modifier.width(8.dp))
                
                Box(modifier = Modifier.weight(1f), contentAlignment = Alignment.CenterStart) {
                    if (searchQuery.isEmpty()) {
                        Text(
                            text = "Search for 'contacts'",
                            color = PhonePeTextMuted,
                            fontSize = 15.sp
                        )
                    }
                    BasicTextFieldWithoutInnerPadding(
                        value = searchQuery,
                        onValueChange = { searchQuery = it },
                        modifier = Modifier.fillMaxWidth()
                    )
                }

                Icon(
                    imageVector = Icons.Default.Mic,
                    contentDescription = "Voice Search",
                    tint = PhonePeTextMuted,
                    modifier = Modifier
                        .size(20.dp)
                        .clickable {
                            Toast.makeText(context, "Voice input not available in clone", Toast.LENGTH_SHORT).show()
                        }
                )
            }
        }

        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(20.dp)
        ) {
            // Section 1: Popular
            Column {
                Text(
                    text = "Popular",
                    fontSize = 15.sp,
                    fontWeight = FontWeight.Bold,
                    color = PhonePeTextDark,
                    modifier = Modifier.padding(bottom = 12.dp)
                )
                
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    PopularItem(
                        icon = Icons.Default.AccountBalanceWallet,
                        label = "Wallet",
                        onClick = {
                            Toast.makeText(context, "Wallet opens...", Toast.LENGTH_SHORT).show()
                        }
                    )
                    PopularItem(
                        icon = Icons.Default.PhoneAndroid,
                        label = "Mobile\nRecharge",
                        onClick = onCreatePrank
                    )
                    PopularItem(
                        icon = Icons.Default.Payment,
                        label = "Loan\nRepayment",
                        onClick = onCreatePrank
                    )
                    PopularItem(
                        icon = Icons.Default.DirectionsCar,
                        label = "FASTag\nRecharge",
                        onClick = {
                            Toast.makeText(context, "FASTag recharging is currently unavailable.", Toast.LENGTH_SHORT).show()
                        }
                    )
                }
            }

            // Section 2: New for you
            Column {
                Text(
                    text = "New for you",
                    fontSize = 15.sp,
                    fontWeight = FontWeight.Bold,
                    color = PhonePeTextDark,
                    modifier = Modifier.padding(bottom = 12.dp)
                )

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    // Card 1: Silver
                    Card(
                        modifier = Modifier
                            .weight(1f)
                            .height(180.dp),
                        colors = CardDefaults.cardColors(containerColor = Color.White),
                        shape = RoundedCornerShape(12.dp),
                        elevation = CardDefaults.cardElevation(2.dp)
                    ) {
                        Column {
                            // Header background block representing a premium card
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height(90.dp)
                                    .background(
                                        Brush.verticalGradient(
                                            listOf(Color(0xFF374151), Color(0xFF111827))
                                        )
                                    )
                                    .padding(8.dp),
                                contentAlignment = Alignment.Center
                            ) {
                                androidx.compose.foundation.Image(
                                    painter = androidx.compose.ui.res.painterResource(id = com.example.R.drawable.ic_launcher_foreground),
                                    contentDescription = "Logo",
                                    contentScale = androidx.compose.ui.layout.ContentScale.Crop,
                                    modifier = Modifier
                                        .size(40.dp)
                                        .clip(CircleShape)
                                )
                            }
                            Column(modifier = Modifier.padding(10.dp)) {
                                Text(
                                    text = "The new age Sil...",
                                    fontWeight = FontWeight.Bold,
                                    fontSize = 13.sp,
                                    color = PhonePeTextDark
                                )
                                Spacer(modifier = Modifier.height(4.dp))
                                Text(
                                    text = "Start your Silver savings journey",
                                    fontSize = 11.sp,
                                    color = PhonePeTextMuted,
                                    lineHeight = 14.sp
                                )
                            }
                        }
                    }

                    // Card 2: Share.market
                    Card(
                        modifier = Modifier
                            .weight(1f)
                            .height(180.dp),
                        colors = CardDefaults.cardColors(containerColor = Color.White),
                        shape = RoundedCornerShape(12.dp),
                        elevation = CardDefaults.cardElevation(2.dp)
                    ) {
                        Column {
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height(90.dp)
                                    .background(Color(0xFF5f259f)) // Share market purple
                                    .padding(8.dp),
                                contentAlignment = Alignment.Center
                            ) {
                                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                    Text(
                                        text = "share.market",
                                        color = Color.White,
                                        fontWeight = FontWeight.ExtraBold,
                                        fontSize = 14.sp
                                    )
                                    Row(
                                        horizontalArrangement = Arrangement.spacedBy(4.dp),
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Text("Balance ₹100", color = Color.Green, fontSize = 9.sp, fontWeight = FontWeight.Bold)
                                        Text("=", color = Color.White, fontSize = 9.sp)
                                        Text("Buying ₹500", color = Color.Yellow, fontSize = 9.sp, fontWeight = FontWeight.Bold)
                                    }
                                }
                            }
                            Column(modifier = Modifier.padding(10.dp)) {
                                Text(
                                    text = "Leverage up to 5x",
                                    fontWeight = FontWeight.Bold,
                                    fontSize = 13.sp,
                                    color = PhonePeTextDark
                                )
                                Spacer(modifier = Modifier.height(4.dp))
                                Text(
                                    text = "₹100 = ₹500 buying power. Trade now.",
                                    fontSize = 11.sp,
                                    color = PhonePeTextMuted,
                                    lineHeight = 14.sp
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
fun PopularItem(
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    label: String,
    onClick: () -> Unit
) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = Modifier
            .width(76.dp)
            .clickable { onClick() }
    ) {
        Box(
            modifier = Modifier
                .size(46.dp)
                .clip(CircleShape)
                .background(Color.White)
                .border(1.dp, Color(0xFFE2E8F0), CircleShape),
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = icon,
                contentDescription = null,
                tint = PhonePePurple,
                modifier = Modifier.size(22.dp)
            )
        }
        Spacer(modifier = Modifier.height(6.dp))
        Text(
            text = label,
            fontSize = 11.sp,
            color = PhonePeTextDark,
            textAlign = TextAlign.Center,
            lineHeight = 13.sp
        )
    }
}

// Simple helper textfield to avoid full material styling noise
@Composable
fun BasicTextFieldWithoutInnerPadding(
    value: String,
    onValueChange: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    androidx.compose.foundation.text.BasicTextField(
        value = value,
        onValueChange = onValueChange,
        textStyle = LocalTextStyle.current.copy(fontSize = 15.sp, color = PhonePeTextDark),
        modifier = modifier
    )
}
