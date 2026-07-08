package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.delay

@Composable
fun PaymentProcessingScreen(onProcessingComplete: () -> Unit) {
    LaunchedEffect(Unit) {
        delay(2500)
        onProcessingComplete()
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.White),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        // Toggle/pill animation simulation
        Box(
            modifier = Modifier
                .width(80.dp)
                .height(32.dp)
                .background(Color(0xFFEDE7F6), RoundedCornerShape(16.dp))
        ) {
            Box(
                modifier = Modifier
                    .size(32.dp)
                    .background(Color(0xFF9036F5), RoundedCornerShape(16.dp))
            )
        }
        
        Spacer(modifier = Modifier.height(24.dp))
        
        Text(
            text = "Connecting Securely",
            fontSize = 18.sp,
            fontWeight = FontWeight.Bold,
            color = Color.Black
        )
    }
}
