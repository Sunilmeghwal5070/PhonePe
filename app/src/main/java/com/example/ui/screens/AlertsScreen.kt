package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.filled.Star
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
import com.example.ui.theme.*

data class PrankAlert(
    val id: Int,
    val title: String,
    val body: String,
    val time: String,
    val isUnread: Boolean = true
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AlertsScreen() {
    val alerts = remember {
        mutableStateListOf(
            PrankAlert(
                id = 1,
                title = "Blast Offer! ₹10,00,000 credited 💸",
                body = "A fictional one million rupees has been deposited into your account. Please use this clone screen immediately to throw a party for your friends! 😎🍩",
                time = "Just now"
            ),
            PrankAlert(
                id = 2,
                title = "Secret message from Bank Manager 🤫",
                body = "The manager says: 'Brother, you have so much balance that even our bank employees hesitate to ask for tea in front of you!' ☕️😂",
                time = "2 hours ago"
            ),
            PrankAlert(
                id = 3,
                title = "Rewards unlocked! 🏆",
                body = "Congratulations! You surprised your friends using this excellent clone. Keep making payment screens like this and keep them laughing.",
                time = "Yesterday"
            ),
            PrankAlert(
                id = 4,
                title = "Safe and Secure 🛡️",
                body = "This app is secure and has no connection to your real account.",
                time = "3 days ago"
            )
        )
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFFF5F6FA))
    ) {
        // Header
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .background(Color.White)
                .padding(vertical = 14.dp, horizontal = 16.dp)
        ) {
            Text(
                text = "Notifications & Alerts",
                fontSize = 18.sp,
                fontWeight = FontWeight.Bold,
                color = PhonePeTextDark,
                modifier = Modifier.align(Alignment.Center)
            )
        }

        if (alerts.isEmpty()) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Icon(
                        imageVector = Icons.Default.Notifications,
                        contentDescription = null,
                        tint = PhonePeTextMuted.copy(alpha = 0.3f),
                        modifier = Modifier.size(64.dp)
                    )
                    Spacer(modifier = Modifier.height(12.dp))
                    Text("No notifications yet", fontWeight = FontWeight.Bold, color = PhonePeTextDark)
                }
            }
        } else {
            LazyColumn(
                modifier = Modifier.fillMaxSize(),
                contentPadding = PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                items(alerts) { alert ->
                    Card(
                        colors = CardDefaults.cardColors(containerColor = Color.White),
                        shape = RoundedCornerShape(10.dp),
                        elevation = CardDefaults.cardElevation(1.dp),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(14.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Box(
                                modifier = Modifier
                                    .size(38.dp)
                                    .clip(CircleShape)
                                    .background(PhonePeLightPurple),
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(
                                    imageVector = Icons.Default.Star,
                                    contentDescription = null,
                                    tint = PhonePePurple,
                                    modifier = Modifier.size(18.dp)
                                )
                            }

                            Spacer(modifier = Modifier.width(12.dp))

                            Column(modifier = Modifier.weight(1f)) {
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Text(
                                        text = alert.title,
                                        fontWeight = FontWeight.Bold,
                                        fontSize = 14.sp,
                                        color = PhonePeTextDark,
                                        maxLines = 1,
                                        overflow = TextOverflow.Ellipsis,
                                        modifier = Modifier.weight(1f)
                                    )
                                    Text(
                                        text = alert.time,
                                        fontSize = 10.sp,
                                        color = PhonePeTextMuted
                                    )
                                }
                                Spacer(modifier = Modifier.height(4.dp))
                                Text(
                                    text = alert.body,
                                    fontSize = 12.sp,
                                    color = PhonePeTextDark.copy(alpha = 0.8f),
                                    lineHeight = 16.sp
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}
