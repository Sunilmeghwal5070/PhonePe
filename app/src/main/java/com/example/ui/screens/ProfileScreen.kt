package com.example.ui.screens
import androidx.compose.ui.text.style.TextAlign

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.*
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.graphics.vector.ImageVector

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProfileScreen(
    onBack: () -> Unit,
    onNavigateToEditDetails: () -> Unit = {},
    onNavigateToAccountDetails: () -> Unit = {}
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { },
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
            // Profile Header
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(Color.White)
                    .padding(horizontal = 16.dp, vertical = 12.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Box(
                    modifier = Modifier
                        .size(48.dp)
                        .background(Color(0xFFE4B610), CircleShape),
                    contentAlignment = Alignment.Center
                ) {
                    Text("Y", color = Color.White, fontSize = 24.sp, fontWeight = FontWeight.Bold)
                }
                
                Spacer(modifier = Modifier.width(16.dp))
                
                Column(modifier = Modifier.weight(1f)) {
                    Text("Yashwant Meghwal", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color.Black)
                    Text("+91 6367512667", fontSize = 14.sp, color = Color.Gray)
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
            
            // Receive Money Banner
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp),
                shape = RoundedCornerShape(12.dp),
                colors = CardDefaults.cardColors(containerColor = Color.White),
                border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFE0E0E0))
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.Error, contentDescription = null, tint = Color(0xFF607D8B), modifier = Modifier.size(16.dp))
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("Not receiving money on PhonePe", fontWeight = FontWeight.Bold, fontSize = 13.sp, color = Color(0xFF455A64))
                    }
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Box(
                                modifier = Modifier
                                    .size(40.dp)
                                    .background(Color(0xFFF3E5F5), RoundedCornerShape(8.dp)),
                                contentAlignment = Alignment.Center
                            ) {
                                Text("पे", color = Color(0xFF5f259f), fontWeight = FontWeight.Bold)
                            }
                            Spacer(modifier = Modifier.width(12.dp))
                            Text(
                                text = "Receive money here\nfrom any UPI app",
                                fontSize = 14.sp,
                                color = Color.Black
                            )
                        }
                        
                        Button(
                            onClick = { },
                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF5f259f)),
                            shape = RoundedCornerShape(8.dp),
                            contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp)
                        ) {
                            Text("Proceed", color = Color.White, fontWeight = FontWeight.Bold)
                        }
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            
            // QR Code
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp),
                shape = RoundedCornerShape(12.dp),
                colors = CardDefaults.cardColors(containerColor = Color.White),
                elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
            ) {
                Column(
                    modifier = Modifier.fillMaxWidth().padding(16.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Box(
                        modifier = Modifier
                            .size(200.dp)
                            .background(Color.LightGray) // placeholder for QR
                    ) {
                        // In reality this would be an image
                        Icon(
                            Icons.Default.QrCode2,
                            contentDescription = "QR Code",
                            modifier = Modifier.fillMaxSize()
                        )
                        Box(
                            modifier = Modifier
                                .align(Alignment.Center)
                                .size(40.dp)
                                .background(Color.White, CircleShape)
                                .padding(4.dp)
                                .background(Color.Black, CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Text("पे", color = Color.White, fontWeight = FontWeight.Bold)
                        }
                    }
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Box(
                            modifier = Modifier.size(24.dp).border(1.dp, Color.Gray, RoundedCornerShape(4.dp)),
                            contentAlignment = Alignment.Center
                        ) {
                            Text("S", color = Color.Red, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                        }
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("Union Bank... - 0365", fontSize = 14.sp, color = Color.Black)
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            
            // Suggested for you
            Column(modifier = Modifier.fillMaxWidth().background(Color.White)) {
                Text(
                    text = "Suggested for you",
                    fontWeight = FontWeight.Bold,
                    fontSize = 16.sp,
                    color = Color.Black,
                    modifier = Modifier.padding(16.dp)
                )
                
                Row(
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    SuggestedItem(icon = Icons.Default.CreditCard, label = "PhonePe\nHDFC Card")
                    SuggestedItem(icon = Icons.Default.Fingerprint, label = "Pay with\nFingerprint")
                    SuggestedItem(icon = Icons.Default.CreditScore, label = "Wish Credit\nCard")
                    SuggestedItem(icon = Icons.Default.AccountBalanceWallet, label = "Wallet")
                }
                Spacer(modifier = Modifier.height(16.dp))
            }
            
            Spacer(modifier = Modifier.height(8.dp))
            
            // Payment Methods
            Column(modifier = Modifier.fillMaxWidth().background(Color.White)) {
                Text(
                    text = "Payment Methods",
                    fontWeight = FontWeight.Bold,
                    fontSize = 16.sp,
                    color = Color.Black,
                    modifier = Modifier.padding(16.dp)
                )
                
                ListItemWithIcon(Icons.Default.AccountBalance, "Bank Accounts", "Set UPI PIN, Add Accounts & more", tint = Color(0xFF1976D2), onClick = onNavigateToAccountDetails)
                ListItemWithIcon(Icons.Default.CreditCard, "RuPay on UPI", "Pay with your credit card via UPI", tint = Color(0xFF1976D2))
                ListItemWithAction(Icons.Default.AccountBalanceWallet, "PhonePe Wallet", "Earn up to 2% cashback", "Try Now", tint = Color(0xFFE65100))
                ListItemWithIcon(Icons.Default.Payment, "Credit/Debit Cards", "Manage your saved cards", tint = Color(0xFF1976D2))
                ListItemWithIcon(Icons.Default.People, "Pocket Money", "Powered by UPI Circle", tint = Color(0xFFE91E63))
                ListItemWithAction(Icons.Default.Bolt, "UPI Lite", "Pin-less payments up to ₹1,000", "Activate", tint = Color(0xFF00B0FF))
                ListItemWithIcon(Icons.Default.CreditScore, "Credit Line on UPI", "Avail Credit from your bank", tint = Color(0xFF388E3C))
                ListItemWithIcon(Icons.Default.CardGiftcard, "PhonePe Gift Card", "Gift for your loved ones", tint = Color(0xFF5f259f))
                
                // Fingerprint Banner
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(Color(0xFF31106A))
                        .padding(16.dp)
                ) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween,
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Column {
                            Text("Did you know?", color = Color(0xFF9E7DE8), fontSize = 12.sp)
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Text("You can pay using Fingerprint.", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                                Spacer(modifier = Modifier.width(8.dp))
                                Box(modifier = Modifier.size(16.dp).background(Color.White, CircleShape), contentAlignment = Alignment.Center) {
                                    Icon(Icons.AutoMirrored.Filled.ArrowForward, contentDescription = null, tint = Color(0xFF31106A), modifier = Modifier.size(12.dp))
                                }
                            }
                        }
                        Icon(Icons.Default.Fingerprint, contentDescription = null, tint = Color(0xFF00B0FF), modifier = Modifier.size(48.dp))
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(8.dp))
            
            // Payment Settings
            Column(modifier = Modifier.fillMaxWidth().background(Color.White)) {
                Text(
                    text = "Payment Settings",
                    fontWeight = FontWeight.Bold,
                    fontSize = 16.sp,
                    color = Color.Black,
                    modifier = Modifier.padding(16.dp)
                )
                
                ListItemWithIcon(Icons.Default.Autorenew, "AutoPay", "Manage your IPOs, SIPs & more", tint = Color(0xFF5f259f))
                ListItemWithIcon(Icons.Default.Public, "International", "Scan & Pay at Global Merchants", tint = Color(0xFF00BCD4))
                ListItemWithIcon(Icons.Default.Settings, "UPI Settings", "Manage UPI IDs and UPI Number", tint = Color(0xFF546E7A))
            }
            
            Spacer(modifier = Modifier.height(8.dp))
            
            // Other settings
            Column(modifier = Modifier.fillMaxWidth().background(Color.White)) {
                ListItemWithIcon(Icons.Default.Tune, "Preferences & Security", "Languages, reminders, notifications,\npermissions, themes, screen lock, etc", tint = Color.Black)
                
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable { }
                        .padding(horizontal = 16.dp, vertical = 16.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(Icons.Default.ScreenRotation, contentDescription = null, tint = Color.Black)
                    Spacer(modifier = Modifier.width(16.dp))
                    Text("Shake to Scan", fontSize = 16.sp, color = Color.Black, modifier = Modifier.weight(1f))
                    Switch(checked = true, onCheckedChange = { }, colors = SwitchDefaults.colors(checkedThumbColor = Color.White, checkedTrackColor = Color(0xFF388E3C)))
                }
                
                HorizontalDivider(color = Color(0xFFF0F0F0))
                
                ListItemWithIcon(Icons.Default.CardGiftcard, "Refer and earn ₹200", null, tint = Color.Black)
                ListItemWithIcon(Icons.Default.HelpOutline, "Help and support", null, tint = Color.Black)
                ListItemWithIcon(Icons.Default.Info, "About PhonePe", null, tint = Color.Black)
            }
            
            Spacer(modifier = Modifier.height(8.dp))
            
            // Log out
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(Color.White)
                    .clickable { }
                    .padding(horizontal = 16.dp, vertical = 24.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(Icons.AutoMirrored.Filled.ExitToApp, contentDescription = null, tint = Color(0xFFD32F2F))
                Spacer(modifier = Modifier.width(16.dp))
                Text("Log out", fontSize = 16.sp, color = Color(0xFFD32F2F))
            }
            
            Spacer(modifier = Modifier.height(24.dp))
        }
    }
}

@Composable
fun SuggestedItem(icon: ImageVector, label: String) {
    Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.width(72.dp)) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(48.dp)
                .background(Color(0xFFF5F5F5), RoundedCornerShape(8.dp))
                .border(1.dp, Color(0xFFE0E0E0), RoundedCornerShape(8.dp)),
            contentAlignment = Alignment.Center
        ) {
            Icon(icon, contentDescription = null, tint = Color(0xFF5f259f))
        }
        Spacer(modifier = Modifier.height(8.dp))
        Text(
            text = label,
            fontSize = 11.sp,
            color = Color.Black,
            textAlign = TextAlign.Center,
            lineHeight = 14.sp
        )
    }
}

@Composable
fun ListItemWithIcon(icon: ImageVector, title: String, subtitle: String?, tint: Color, onClick: () -> Unit = {}) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() }
            .padding(horizontal = 16.dp, vertical = 16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(icon, contentDescription = null, tint = tint, modifier = Modifier.size(24.dp))
        Spacer(modifier = Modifier.width(16.dp))
        Column(modifier = Modifier.weight(1f)) {
            Text(title, fontSize = 16.sp, color = Color.Black)
            if (subtitle != null) {
                Spacer(modifier = Modifier.height(2.dp))
                Text(subtitle, fontSize = 13.sp, color = Color.Gray, lineHeight = 18.sp)
            }
        }
        Icon(Icons.AutoMirrored.Filled.KeyboardArrowRight, contentDescription = null, tint = Color.Gray)
    }
    HorizontalDivider(color = Color(0xFFF0F0F0), modifier = Modifier.padding(start = 56.dp))
}

@Composable
fun ListItemWithAction(icon: ImageVector, title: String, subtitle: String, actionText: String, tint: Color, onClick: () -> Unit = {}) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() }
            .padding(horizontal = 16.dp, vertical = 16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(icon, contentDescription = null, tint = tint, modifier = Modifier.size(24.dp))
        Spacer(modifier = Modifier.width(16.dp))
        Column(modifier = Modifier.weight(1f)) {
            Text(title, fontSize = 16.sp, color = Color.Black)
            Spacer(modifier = Modifier.height(2.dp))
            Text(subtitle, fontSize = 13.sp, color = Color.Gray)
        }
        Text(
            text = actionText,
            color = Color(0xFF5f259f),
            fontWeight = FontWeight.Bold,
            fontSize = 14.sp
        )
    }
    HorizontalDivider(color = Color(0xFFF0F0F0), modifier = Modifier.padding(start = 56.dp))
}
