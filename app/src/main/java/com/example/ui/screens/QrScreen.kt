package com.example.ui.screens

import android.widget.Toast
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.HelpOutline
import androidx.compose.material.icons.filled.ContentCopy
import androidx.compose.material.icons.filled.FileDownload
import androidx.compose.material.icons.filled.Share
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.StrokeJoin
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlin.random.Random

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun QrScreen(onBack: () -> Unit = {}) {
    val context = LocalContext.current
    val clipboardManager = LocalClipboardManager.current
    val upiId = "sunilmeghwal6367@ybl"

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
                    IconButton(onClick = { 
                        Toast.makeText(context, "Help", Toast.LENGTH_SHORT).show() 
                    }) {
                        Icon(Icons.AutoMirrored.Filled.HelpOutline, contentDescription = "Help", tint = Color.Black)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.White)
            )
        },
        containerColor = Color.White
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .background(Color.White),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Spacer(modifier = Modifier.height(24.dp))
            
            // Bank Logo
            Box(
                modifier = Modifier
                    .size(48.dp)
                    .border(1.dp, Color(0xFFE0E0E0), RoundedCornerShape(12.dp)),
                contentAlignment = Alignment.Center
            ) {
                // Union Bank logo approximation (red 'u' with blue lines)
                Canvas(modifier = Modifier.size(24.dp)) {
                    val redColor = Color(0xFFE53935)
                    val blueColor = Color(0xFF1E88E5)
                    
                    // Draw intertwined U / S shape
                    drawPath(
                        path = Path().apply {
                            moveTo(size.width * 0.2f, size.height * 0.2f)
                            lineTo(size.width * 0.2f, size.height * 0.6f)
                            quadraticBezierTo(
                                size.width * 0.2f, size.height * 0.9f,
                                size.width * 0.5f, size.height * 0.9f
                            )
                            quadraticBezierTo(
                                size.width * 0.8f, size.height * 0.9f,
                                size.width * 0.8f, size.height * 0.6f
                            )
                            lineTo(size.width * 0.8f, size.height * 0.1f)
                        },
                        color = redColor,
                        style = Stroke(width = 4.dp.toPx(), cap = StrokeCap.Round, join = StrokeJoin.Round)
                    )
                    
                    drawPath(
                        path = Path().apply {
                            moveTo(size.width * 0.8f, size.height * 0.1f)
                            lineTo(size.width * 0.5f, size.height * 0.1f)
                            quadraticBezierTo(
                                size.width * 0.1f, size.height * 0.1f,
                                size.width * 0.1f, size.height * 0.4f
                            )
                            lineTo(size.width * 0.1f, size.height * 0.9f)
                        },
                        color = blueColor,
                        style = Stroke(width = 4.dp.toPx(), cap = StrokeCap.Round, join = StrokeJoin.Round)
                    )
                }
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            
            Text(
                text = "Union Bank Of India - 0365",
                fontSize = 20.sp,
                fontWeight = FontWeight.Bold,
                color = Color.Black
            )
            
            Spacer(modifier = Modifier.height(8.dp))
            
            Text(
                text = "Primary account for receiving money",
                fontSize = 14.sp,
                color = Color(0xFF388E3C)
            )
            
            Spacer(modifier = Modifier.height(32.dp))
            
            // Large QR Code
            Box(
                modifier = Modifier
                    .size(280.dp)
                    .background(Color.White),
                contentAlignment = Alignment.Center
            ) {
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
                
                // PhonePe Logo in Center
                Box(
                    modifier = Modifier
                        .size(56.dp)
                        .background(Color.White, CircleShape),
                    contentAlignment = Alignment.Center
                ) {
                    Box(
                        modifier = Modifier
                            .size(48.dp)
                            .background(Color.Black, CircleShape),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = "पे",
                            color = Color.White,
                            fontSize = 24.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(32.dp))
            
            // UPI ID
            Row(
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier.clickable {
                    clipboardManager.setText(AnnotatedString(upiId))
                    Toast.makeText(context, "UPI ID copied!", Toast.LENGTH_SHORT).show()
                }
            ) {
                Text(
                    text = "UPI ID: $upiId",
                    fontSize = 16.sp,
                    color = Color.DarkGray
                )
                Spacer(modifier = Modifier.width(8.dp))
                Icon(
                    imageVector = Icons.Default.ContentCopy,
                    contentDescription = "Copy",
                    tint = Color.Gray,
                    modifier = Modifier.size(18.dp)
                )
            }
            
            Spacer(modifier = Modifier.height(32.dp))
            
            // Action Buttons
            Row(
                horizontalArrangement = Arrangement.Center,
                modifier = Modifier.fillMaxWidth()
            ) {
                OutlinedButton(
                    onClick = { Toast.makeText(context, "Downloading QR...", Toast.LENGTH_SHORT).show() },
                    shape = RoundedCornerShape(8.dp),
                    colors = ButtonDefaults.outlinedButtonColors(contentColor = Color.Black),
                    border = androidx.compose.foundation.BorderStroke(1.dp, Color.LightGray),
                    modifier = Modifier.height(48.dp).padding(end = 16.dp)
                ) {
                    Icon(Icons.Default.FileDownload, contentDescription = null, modifier = Modifier.size(20.dp))
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("Download", fontWeight = FontWeight.SemiBold, fontSize = 16.sp)
                }
                
                OutlinedButton(
                    onClick = { Toast.makeText(context, "Sharing...", Toast.LENGTH_SHORT).show() },
                    shape = RoundedCornerShape(8.dp),
                    colors = ButtonDefaults.outlinedButtonColors(contentColor = Color.Black),
                    border = androidx.compose.foundation.BorderStroke(1.dp, Color.LightGray),
                    modifier = Modifier.height(48.dp)
                ) {
                    Icon(Icons.Default.Share, contentDescription = null, modifier = Modifier.size(20.dp))
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("Share", fontWeight = FontWeight.SemiBold, fontSize = 16.sp)
                }
            }
            
            Spacer(modifier = Modifier.weight(1f))
            
            // Bottom Banner
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(Color(0xFFF9F9F9))
                    .padding(vertical = 16.dp, horizontal = 24.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Column {
                        Text("Supported on all UPI apps", color = Color.Gray, fontSize = 12.sp)
                        Spacer(modifier = Modifier.height(8.dp))
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            // PhonePe text logo
                            Text("पे PhonePe", fontWeight = FontWeight.Bold, color = Color.Gray, fontSize = 12.sp)
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("BHIM", fontWeight = FontWeight.Bold, color = Color.Gray, fontSize = 12.sp, fontStyle = androidx.compose.ui.text.font.FontStyle.Italic)
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("G Pay", fontWeight = FontWeight.Bold, color = Color.Gray, fontSize = 12.sp)
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("Paytm", fontWeight = FontWeight.Bold, color = Color.Gray, fontSize = 12.sp)
                        }
                    }
                    
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Box(
                            modifier = Modifier
                                .width(1.dp)
                                .height(32.dp)
                                .background(Color.LightGray)
                        )
                        Spacer(modifier = Modifier.width(16.dp))
                        Column {
                            Text("Powered by", color = Color.Gray, fontSize = 10.sp)
                            Text("UPI", fontWeight = FontWeight.Bold, fontSize = 14.sp, fontStyle = androidx.compose.ui.text.font.FontStyle.Italic, color = Color.Gray)
                        }
                    }
                }
            }
        }
    }
}
