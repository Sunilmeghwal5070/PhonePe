package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material3.*
import androidx.compose.animation.core.*
import androidx.compose.runtime.getValue
import androidx.compose.ui.draw.scale
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

@Composable
fun PaymentSuccessScreen(
    amount: String,
    payeeName: String = "Karishna Karishna",
    upiId: String = "krishna88750@axl",
    onDone: () -> Unit,
    onViewDetails: () -> Unit
) {
    val currentTime = SimpleDateFormat("dd MMMM yyyy 'at' hh:mm a", Locale.getDefault()).format(Date())

    val infiniteTransition = rememberInfiniteTransition()
    val scale by infiniteTransition.animateFloat(
        initialValue = 1f,
        targetValue = 1.15f,
        animationSpec = infiniteRepeatable(
            animation = tween(800, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        )
    )


    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFF388E3C)),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(modifier = Modifier.weight(1f))
        
        Box(
            modifier = Modifier
                .size(80.dp)
                .scale(scale)
                .background(Color.White, CircleShape),
            contentAlignment = Alignment.Center
        ) {
            Icon(Icons.Default.Check, contentDescription = null, tint = Color(0xFF388E3C), modifier = Modifier.size(50.dp))
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        Text(
            text = "Payment Successful",
            color = Color.White,
            fontSize = 22.sp,
            fontWeight = FontWeight.Bold
        )
        
        Spacer(modifier = Modifier.height(4.dp))
        
        Text(
            text = currentTime,
            color = Color.White.copy(alpha = 0.9f),
            fontSize = 14.sp
        )
        
        Spacer(modifier = Modifier.height(32.dp))
        
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp),
            colors = CardDefaults.cardColors(containerColor = Color.White),
            shape = RoundedCornerShape(16.dp)
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Box(
                        modifier = Modifier
                            .size(60.dp)
                            .background(Color(0xFF29B6F6), CircleShape),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(payeeName.take(2).uppercase(), color = Color.White, fontSize = 24.sp, fontWeight = FontWeight.Bold)
                    }
                    Spacer(modifier = Modifier.width(16.dp))
                    Column {
                        Text(payeeName, fontSize = 18.sp, fontWeight = FontWeight.Bold)
                        Text(upiId, color = Color.Gray, fontSize = 14.sp)
                        Spacer(modifier = Modifier.height(8.dp))
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text("₹$amount", fontSize = 24.sp, fontWeight = FontWeight.Bold)
                            Text("Split Expense", color = Color(0xFF512DA8), fontWeight = FontWeight.Bold, fontSize = 14.sp)
                        }
                    }
                }
                
                Spacer(modifier = Modifier.height(16.dp))
                HorizontalDivider(thickness = 1.dp, color = Color(0xFFEEEEEE))
                
                Row(
                    modifier = Modifier.fillMaxWidth().padding(top = 16.dp),
                    horizontalArrangement = Arrangement.SpaceEvenly
                ) {
                    TextButton(onClick = onViewDetails) {
                        Text("View Details", color = Color.Black)
                    }
                    TextButton(onClick = { /* Share Receipt */ }) {
                        Text("Share Receipt", color = Color.Black)
                    }
                }
            }
        }
        
        Spacer(modifier = Modifier.weight(1f))
        
        TextButton(
            onClick = onDone,
            modifier = Modifier.padding(bottom = 32.dp)
        ) {
            Text("Done", color = Color(0xFF512DA8), fontWeight = FontWeight.Bold, fontSize = 18.sp)
        }
    }
}
