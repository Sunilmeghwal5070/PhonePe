package com.example.ui.screens

import androidx.compose.animation.core.*
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.FlashlightOn
import androidx.compose.material.icons.filled.HelpOutline
import androidx.compose.material.icons.filled.Image
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.LaunchedEffect
import kotlinx.coroutines.delay
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.R

@Composable
fun ScannerScreen(
    onBack: () -> Unit,
    onScanComplete: () -> Unit = {}
) {
    LaunchedEffect(Unit) {
        delay(2500)
        onScanComplete()
    }
    val infiniteTransition = rememberInfiniteTransition(label = "scanner")
    val scanAnim by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 260f,
        animationSpec = infiniteRepeatable(
            animation = tween(2000, easing = LinearEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "scanLine"
    )

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFF2C2C2C))
            .clickable { onScanComplete() }
    ) {
        // Here normally we would have a CameraPreview, but since camera is disabled
        // we can just put a placeholder image or a dark gradient
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(Color(0xFF1E1E1E).copy(alpha = 0.9f))
        )

        // Top Bar
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(top = 48.dp, start = 16.dp, end = 16.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                IconButton(onClick = onBack) {
                    Icon(imageVector = Icons.Default.ArrowBack, contentDescription = "Back", tint = Color.White)
                }
                Spacer(modifier = Modifier.width(8.dp))
                Column {
                    Text(text = "Scan any QR", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.SemiBold)
                    Text(text = "PhonePe • Google Pay • BHIM • Paytm", color = Color.LightGray, fontSize = 12.sp)
                }
            }
            IconButton(onClick = { /* Help */ }) {
                Icon(imageVector = Icons.Default.HelpOutline, contentDescription = "Help", tint = Color.White)
            }
        }

        // Center Viewfinder
        Box(
            modifier = Modifier
                .align(Alignment.Center)
                .size(280.dp)
                .clip(RoundedCornerShape(24.dp))
                .background(Color.White.copy(alpha = 0.1f))
        ) {
            // Scanner corners
            val cornerLength = 40.dp
            val cornerWidth = 4.dp
            val cornerColor = Color(0xFF9036F5) // PhonePe Purple
            
            // Top Left
            Box(modifier = Modifier.align(Alignment.TopStart).padding(16.dp)) {
                Box(modifier = Modifier.size(cornerLength, cornerWidth).background(cornerColor, RoundedCornerShape(topStart = 8.dp, topEnd = 8.dp)))
                Box(modifier = Modifier.size(cornerWidth, cornerLength).background(cornerColor, RoundedCornerShape(topStart = 8.dp, bottomStart = 8.dp)))
            }
            // Top Right
            Box(modifier = Modifier.align(Alignment.TopEnd).padding(16.dp)) {
                Box(modifier = Modifier.align(Alignment.TopEnd).size(cornerLength, cornerWidth).background(cornerColor, RoundedCornerShape(topStart = 8.dp, topEnd = 8.dp)))
                Box(modifier = Modifier.align(Alignment.TopEnd).size(cornerWidth, cornerLength).background(cornerColor, RoundedCornerShape(topEnd = 8.dp, bottomEnd = 8.dp)))
            }
            // Bottom Left
            Box(modifier = Modifier.align(Alignment.BottomStart).padding(16.dp)) {
                Box(modifier = Modifier.align(Alignment.BottomStart).size(cornerWidth, cornerLength).background(cornerColor, RoundedCornerShape(topStart = 8.dp, bottomStart = 8.dp)))
                Box(modifier = Modifier.align(Alignment.BottomStart).size(cornerLength, cornerWidth).background(cornerColor, RoundedCornerShape(bottomStart = 8.dp, bottomEnd = 8.dp)))
            }
            // Bottom Right
            Box(modifier = Modifier.align(Alignment.BottomEnd).padding(16.dp)) {
                Box(modifier = Modifier.align(Alignment.BottomEnd).size(cornerWidth, cornerLength).background(cornerColor, RoundedCornerShape(topEnd = 8.dp, bottomEnd = 8.dp)))
                Box(modifier = Modifier.align(Alignment.BottomEnd).size(cornerLength, cornerWidth).background(cornerColor, RoundedCornerShape(bottomStart = 8.dp, bottomEnd = 8.dp)))
            }
            
            // Animated Scan Line
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(2.dp)
                    .offset(y = scanAnim.dp)
                    .background(Color(0xFF9036F5)) // Purple line
            )
        }

        // Action Buttons (Upload QR and Torch)
        Row(
            modifier = Modifier
                .align(Alignment.Center)
                .offset(y = 220.dp)
                .fillMaxWidth(),
            horizontalArrangement = Arrangement.Center
        ) {
            Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.padding(horizontal = 24.dp)) {
                Box(
                    modifier = Modifier
                        .size(56.dp)
                        .clip(CircleShape)
                        .background(Color.White.copy(alpha = 0.2f))
                        .border(1.dp, Color.White.copy(alpha = 0.3f), CircleShape),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(imageVector = Icons.Default.Image, contentDescription = "Upload QR", tint = Color.White, modifier = Modifier.size(24.dp))
                }
                Spacer(modifier = Modifier.height(8.dp))
                Text(text = "Upload QR", color = Color.White, fontSize = 14.sp)
            }
            
            Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.padding(horizontal = 24.dp)) {
                Box(
                    modifier = Modifier
                        .size(56.dp)
                        .clip(CircleShape)
                        .background(Color.White.copy(alpha = 0.2f))
                        .border(1.dp, Color.White.copy(alpha = 0.3f), CircleShape),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(imageVector = Icons.Default.FlashlightOn, contentDescription = "Torch", tint = Color.White, modifier = Modifier.size(24.dp))
                }
                Spacer(modifier = Modifier.height(8.dp))
                Text(text = "Torch", color = Color.White, fontSize = 14.sp)
            }
        }

        // Bottom Logos
        Row(
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .padding(bottom = 32.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(text = "BHIM", color = Color.White.copy(alpha = 0.7f), fontWeight = FontWeight.Bold, fontSize = 18.sp, fontStyle = androidx.compose.ui.text.font.FontStyle.Italic)
            Text(text = " | ", color = Color.White.copy(alpha = 0.5f), fontSize = 18.sp)
            Text(text = "UPI", color = Color.White.copy(alpha = 0.7f), fontWeight = FontWeight.Bold, fontSize = 18.sp, fontStyle = androidx.compose.ui.text.font.FontStyle.Italic)
        }
    }
}
