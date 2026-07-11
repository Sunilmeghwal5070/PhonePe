package com.example.ui.screens

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.*
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import kotlin.random.Random
import androidx.compose.foundation.Canvas
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import com.example.ui.PrankViewModel
import com.example.ui.components.BankLogo

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProfileScreen(
    viewModel: PrankViewModel,
    prefsManager: com.example.ui.PrefsManager,
    onBack: () -> Unit,
    onNavigateToEditDetails: () -> Unit = {},
    onNavigateToAccountDetails: () -> Unit = {}
) {
    val userProfile by viewModel.userProfileManager.userProfile.collectAsState()
    val bankAccounts by viewModel.bankAccounts.collectAsState()
    val defaultBank = bankAccounts.firstOrNull()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.Black)
                    }
                },
                actions = {
                    IconButton(onClick = { }) {
                        Icon(Icons.AutoMirrored.Filled.HelpOutline, contentDescription = "Help", tint = Color.Black)
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
                .background(Color.White)
                .padding(paddingValues)
                .verticalScroll(rememberScrollState())
        ) {
            // User Header
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 8.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Box(
                    modifier = Modifier
                        .size(48.dp)
                        .clip(RoundedCornerShape(12.dp))
                        .background(Color(0xFFFBC02D)),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = if (userProfile.name.isNotBlank()) userProfile.name.first().toString().uppercase() else "Y",
                        color = Color.White,
                        fontWeight = FontWeight.Bold,
                        fontSize = 20.sp
                    )
                }
                Spacer(modifier = Modifier.width(16.dp))
                Column(modifier = Modifier.weight(1f)) {
                    Text(userProfile.name.ifBlank { "Yashwant Meghwal" }, fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color.Black)
                    Spacer(modifier = Modifier.height(2.dp))
                    Text("+91 ${userProfile.phone.ifBlank { "6367512667" }}", fontSize = 14.sp, color = Color.Gray)
                }
                Text(
                    text = "Manage",
                    color = Color(0xFF5f259f),
                    fontWeight = FontWeight.Bold,
                    fontSize = 14.sp,
                    modifier = Modifier.clickable { onNavigateToEditDetails() }
                )
            }

            Spacer(modifier = Modifier.height(16.dp))

            // Warning Card
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp),
                shape = RoundedCornerShape(12.dp),
                colors = CardDefaults.cardColors(containerColor = Color(0xFFF9F9FB)),
                border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFE0E0E0))
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.Info, contentDescription = null, tint = Color(0xFF455A64), modifier = Modifier.size(16.dp))
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("Not receiving money on PhonePe", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color(0xFF455A64))
                    }
                    Spacer(modifier = Modifier.height(16.dp))
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
                        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.weight(1f)) {
                            Box(modifier = Modifier.size(40.dp).background(Color(0xFFEDE7F6), RoundedCornerShape(8.dp)), contentAlignment = Alignment.Center) {
                                Text("पे", color = Color(0xFF5f259f), fontWeight = FontWeight.Bold, fontSize = 20.sp)
                            }
                            Spacer(modifier = Modifier.width(12.dp))
                            Text("Receive money here\nfrom any UPI app", fontSize = 16.sp, color = Color.Black)
                        }
                        Button(
                            onClick = { },
                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF5f259f)),
                            shape = RoundedCornerShape(8.dp),
                            modifier = Modifier.height(36.dp)
                        ) {
                            Text("Proceed", fontSize = 14.sp)
                        }
                    }
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            // QR Code Card
            Card(
                modifier = Modifier
                    .width(280.dp)
                    .align(Alignment.CenterHorizontally),
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(containerColor = Color.White),
                elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
                border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFEEEEEE))
            ) {
                Column(
                    modifier = Modifier.padding(24.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Box(modifier = Modifier.size(200.dp).background(Color.White)) {
                        Canvas(modifier = Modifier.fillMaxSize()) {
                            val blockSize = size.width / 25
                            // Draw corner squares
                            fun drawFinderPattern(x: Float, y: Float) {
                                drawRect(
                                    color = Color.Black,
                                    topLeft = Offset(x, y),
                                    size = Size(blockSize * 7, blockSize * 7)
                                )
                                drawRect(
                                    color = Color.White,
                                    topLeft = Offset(x + blockSize, y + blockSize),
                                    size = Size(blockSize * 5, blockSize * 5)
                                )
                                drawRect(
                                    color = Color.Black,
                                    topLeft = Offset(x + blockSize * 2, y + blockSize * 2),
                                    size = Size(blockSize * 3, blockSize * 3)
                                )
                            }
                            
                            drawFinderPattern(0f, 0f)
                            drawFinderPattern(size.width - blockSize * 7, 0f)
                            drawFinderPattern(0f, size.height - blockSize * 7)
                            
                            // Draw random blocks to simulate QR
                            val random = Random(42)
                            for (i in 0 until 25) {
                                for (j in 0 until 25) {
                                    // Avoid finder patterns
                                    val inTopLeft = i < 8 && j < 8
                                    val inTopRight = i > 16 && j < 8
                                    val inBottomLeft = i < 8 && j > 16
                                    // Avoid center for logo
                                    val inCenter = i in 10..14 && j in 10..14
                                    
                                    if (!inTopLeft && !inTopRight && !inBottomLeft && !inCenter) {
                                        if (random.nextBoolean()) {
                                            drawRect(
                                                color = Color.Black,
                                                topLeft = Offset(i * blockSize, j * blockSize),
                                                size = Size(blockSize, blockSize)
                                            )
                                        }
                                    }
                                }
                            }
                        }
                        
                        // Center Logo
                        Box(
                            modifier = Modifier.align(Alignment.Center).size(48.dp).background(Color.White, CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Box(modifier = Modifier.size(40.dp).background(Color.Black, CircleShape), contentAlignment = Alignment.Center) {
                                Text("पे", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 24.sp)
                            }
                        }
                    }
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        BankLogo(bankName = defaultBank?.bankName ?: "Union Bank of India", size = 20.dp)
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("${defaultBank?.bankName?.take(10) ?: "Union Bank"}... - ${defaultBank?.bankDesc?.takeLast(4) ?: "0365"}", fontSize = 14.sp, color = Color.Black)
                    }
                }
            }

            Spacer(modifier = Modifier.height(24.dp))
            HorizontalDivider(thickness = 8.dp, color = Color(0xFFF5F5F5))
            Spacer(modifier = Modifier.height(16.dp))

            // Suggested for you
            Text(
                "Suggested for you",
                fontSize = 18.sp,
                fontWeight = FontWeight.Bold,
                color = Color.Black,
                modifier = Modifier.padding(horizontal = 16.dp)
            )
            Spacer(modifier = Modifier.height(16.dp))
            
            Row(
                modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                SuggestedItem(title = "PhonePe\nCard", icon = Icons.Default.CreditCard, hasBadge = true)
                SuggestedItem(title = "Pay with\nFingerprint", icon = Icons.Default.Fingerprint)
                SuggestedItem(title = "Wish Credit\nCard", icon = Icons.Default.CardGiftcard)
                SuggestedItem(title = "Wallet", icon = Icons.Default.AccountBalanceWallet)
            }

            Spacer(modifier = Modifier.height(24.dp))
            HorizontalDivider(thickness = 8.dp, color = Color(0xFFF5F5F5))
            Spacer(modifier = Modifier.height(16.dp))

            // Payment Methods
            Text(
                "Payment Methods",
                fontSize = 18.sp,
                fontWeight = FontWeight.Bold,
                color = Color.Black,
                modifier = Modifier.padding(horizontal = 16.dp)
            )
            Spacer(modifier = Modifier.height(8.dp))

            ProfileMethodItem(icon = Icons.Default.AccountBalance, title = "Bank Accounts", subtitle = "Set UPI PIN, Add Accounts & more", onClick = onNavigateToAccountDetails)
            ProfileMethodItem(icon = Icons.Default.CreditCard, title = "RuPay on UPI", subtitle = "Pay with your credit card via UPI", onClick = {})
            ProfileMethodItem(icon = Icons.Default.AccountBalanceWallet, title = "PhonePe Wallet", subtitle = "Earn up to 2% cashback", actionText = "Try Now", onClick = {})
            ProfileMethodItem(icon = Icons.Default.Payment, title = "Credit/Debit Cards", subtitle = "Manage your saved cards", onClick = {})
            ProfileMethodItem(icon = Icons.Default.People, title = "Pocket Money", subtitle = "Powered by UPI Circle", onClick = {})
            ProfileMethodItem(icon = Icons.Default.Bolt, title = "UPI Lite", subtitle = "Pin-less payments up to ₹1,000", actionText = "Activate", onClick = {})
            ProfileMethodItem(icon = Icons.Default.Money, title = "Credit Line on UPI", subtitle = "Avail Credit from your bank", onClick = {})
            ProfileMethodItem(icon = Icons.Default.CardGiftcard, title = "PhonePe Gift Card", subtitle = "Gift for your loved ones", onClick = {})

            Spacer(modifier = Modifier.height(8.dp))
            HorizontalDivider(thickness = 8.dp, color = Color(0xFFF5F5F5))
            Spacer(modifier = Modifier.height(16.dp))

            // Payment Settings
            Text(
                "Payment Settings",
                fontSize = 18.sp,
                fontWeight = FontWeight.Bold,
                color = Color.Black,
                modifier = Modifier.padding(horizontal = 16.dp)
            )
            Spacer(modifier = Modifier.height(8.dp))

            ProfileMethodItem(icon = Icons.Default.Autorenew, title = "AutoPay", subtitle = "Manage your IPOs, SIPs & more", onClick = {})
            ProfileMethodItem(icon = Icons.Default.Language, title = "International", subtitle = "Scan & Pay at Global Merchants", onClick = {})
            ProfileMethodItem(icon = Icons.Default.Settings, title = "UPI Settings", subtitle = "Manage UPI IDs and UPI Number", onClick = {})

            Spacer(modifier = Modifier.height(8.dp))
            HorizontalDivider(thickness = 8.dp, color = Color(0xFFF5F5F5))
            Spacer(modifier = Modifier.height(8.dp))

            ProfileMethodItem(icon = Icons.Default.Tune, title = "Preferences & Security", subtitle = "Languages, reminders, notifications,\npermissions, themes, screen lock, etc", onClick = {})
            
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 16.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(Icons.Default.ScreenRotation, contentDescription = null, tint = Color.Black, modifier = Modifier.size(24.dp))
                Spacer(modifier = Modifier.width(16.dp))
                Text("Shake to Scan", fontSize = 16.sp, color = Color.Black, modifier = Modifier.weight(1f))
                var shakeEnabled by remember { mutableStateOf(false) }
                Switch(
                    checked = shakeEnabled,
                    onCheckedChange = { shakeEnabled = it },
                    colors = SwitchDefaults.colors(checkedThumbColor = Color(0xFF5f259f), checkedTrackColor = Color(0xFFE8EAF6))
                )
            }

            Spacer(modifier = Modifier.height(8.dp))
            HorizontalDivider(thickness = 8.dp, color = Color(0xFFF5F5F5))
            Spacer(modifier = Modifier.height(8.dp))

            ProfileMethodItem(icon = Icons.Default.CardGiftcard, title = "Refer and earn ₹200", onClick = {})
            ProfileMethodItem(icon = Icons.AutoMirrored.Filled.HelpOutline, title = "Help and support", onClick = {})

            ProfileMethodItem(icon = Icons.Default.Info, title = "About PhonePe", subtitle = "Developer by Sunil Meghwal", onClick = {})
            
            // App License/Key Details
            val activationKey = prefsManager.getActivationKey() ?: "Unknown"
            val expiryTime = prefsManager.getActivationExpiry()
            val formatter = java.text.SimpleDateFormat("dd MMM yyyy, hh:mm a", java.util.Locale.getDefault())
            val expiryDateStr = if (expiryTime > 0) formatter.format(java.util.Date(expiryTime)) else "N/A"
            
            ProfileMethodItem(
                icon = Icons.Default.VpnKey, 
                title = "App License Details", 
                subtitle = "Key: $activationKey\nExpires: $expiryDateStr", 
                onClick = {}
            )

            
            HorizontalDivider(color = Color(0xFFF0F0F0))
            
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable { }
                    .padding(horizontal = 16.dp, vertical = 20.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(Icons.AutoMirrored.Filled.ExitToApp, contentDescription = null, tint = Color(0xFFD32F2F), modifier = Modifier.size(24.dp))
                Spacer(modifier = Modifier.width(16.dp))
                Text("Log out", fontSize = 16.sp, fontWeight = FontWeight.Medium, color = Color(0xFFD32F2F))
            }

            Spacer(modifier = Modifier.height(32.dp))
        }
    }
}

@Composable
fun SuggestedItem(title: String, icon: ImageVector, hasBadge: Boolean = false) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Box {
            Box(
                modifier = Modifier
                    .size(64.dp)
                    .border(1.dp, Color(0xFFEEEEEE), RoundedCornerShape(12.dp))
                    .clip(RoundedCornerShape(12.dp))
                    .background(Color.White),
                contentAlignment = Alignment.Center
            ) {
                Icon(icon, contentDescription = null, tint = Color(0xFF5f259f), modifier = Modifier.size(32.dp))
            }
            if (hasBadge) {
                Box(
                    modifier = Modifier
                        .offset(x = (-4).dp, y = (-8).dp)
                        .background(Color(0xFF880E4F), RoundedCornerShape(4.dp))
                        .padding(horizontal = 4.dp, vertical = 2.dp)
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.Star, contentDescription = null, tint = Color(0xFF4CAF50), modifier = Modifier.size(10.dp))
                        Text(" Free", fontSize = 8.sp, color = Color.White, fontWeight = FontWeight.Bold)
                    }
                }
            }
        }
        Spacer(modifier = Modifier.height(8.dp))
        Text(title, fontSize = 12.sp, color = Color.Black, textAlign = androidx.compose.ui.text.style.TextAlign.Center)
    }
}

@Composable
fun ProfileMethodItem(
    icon: ImageVector,
    title: String,
    subtitle: String? = null,
    actionText: String? = null,
    onClick: () -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick)
            .padding(horizontal = 16.dp, vertical = 16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(icon, contentDescription = null, tint = Color(0xFF1976D2), modifier = Modifier.size(28.dp))
        Spacer(modifier = Modifier.width(16.dp))
        Column(modifier = Modifier.weight(1f)) {
            Text(title, fontSize = 16.sp, color = Color.Black)
            if (subtitle != null) {
                Spacer(modifier = Modifier.height(2.dp))
                Text(subtitle, fontSize = 14.sp, color = Color.Gray, lineHeight = 18.sp)
            }
        }
        if (actionText != null) {
            Text(actionText, color = Color(0xFF5f259f), fontWeight = FontWeight.Bold, fontSize = 14.sp)
            Spacer(modifier = Modifier.width(8.dp))
        } else {
            Icon(Icons.AutoMirrored.Filled.KeyboardArrowRight, contentDescription = null, tint = Color.Gray)
        }
    }
}


