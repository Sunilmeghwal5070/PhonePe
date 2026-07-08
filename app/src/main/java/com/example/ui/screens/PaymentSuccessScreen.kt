package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material3.*
import androidx.compose.animation.core.*
import android.media.MediaPlayer
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalView
import android.graphics.Bitmap
import androidx.core.content.FileProvider
import android.content.Intent
import java.io.File
import java.io.FileOutputStream
import androidx.compose.runtime.LaunchedEffect
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
    bankName: String = "State Bank of India",
    onDone: () -> Unit,
    onViewDetails: () -> Unit
) {
    val currentTime = SimpleDateFormat("dd MMMM yyyy 'at' hh:mm a", Locale.getDefault()).format(Date())

    
    val context = LocalContext.current
    LaunchedEffect(Unit) {
        val resourceId = context.resources.getIdentifier("payment_success", "raw", context.packageName)
        if (resourceId != 0) {
            try {
                val mediaPlayer = MediaPlayer.create(context, resourceId)
                mediaPlayer.start()
                mediaPlayer.setOnCompletionListener {
                    it.release()
                }
            } catch (e: Exception) {
                // Ignore
            }
        }
    }

    
    val view = LocalView.current
    val onShare = {
        try {
            val bitmap = Bitmap.createBitmap(view.width, view.height, Bitmap.Config.ARGB_8888)
            val canvas = android.graphics.Canvas(bitmap)
            view.draw(canvas)
            
            val file = File(context.cacheDir, "receipt.png")
            val stream = FileOutputStream(file)
            bitmap.compress(Bitmap.CompressFormat.PNG, 100, stream)
            stream.close()
            
            val uri = FileProvider.getUriForFile(context, "${context.packageName}.provider", file)
            val intent = Intent(Intent.ACTION_SEND).apply {
                type = "image/png"
                putExtra(Intent.EXTRA_STREAM, uri)
                addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            }
            context.startActivity(Intent.createChooser(intent, "Share Receipt"))
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

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
                    modifier = Modifier.fillMaxWidth().padding(vertical = 12.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        com.example.ui.components.BankLogo(bankName = bankName, size = 24.dp)
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(bankName, fontSize = 14.sp, color = Color.Gray)
                    }
                }
                
                HorizontalDivider(thickness = 1.dp, color = Color(0xFFEEEEEE))
                
                Row(
                    modifier = Modifier.fillMaxWidth().padding(top = 16.dp),
                    horizontalArrangement = Arrangement.SpaceEvenly
                ) {
                    TextButton(onClick = onViewDetails) {
                        Text("View Details", color = Color.Black)
                    }
                    TextButton(onClick = onShare) {
                        Text("Share Receipt", color = Color.Black)
                    }
                }
            }
        }
        
        Spacer(modifier = Modifier.weight(1f))
        
        TextButton(
            onClick = onDone,
            modifier = Modifier.padding(bottom = 16.dp)
        ) {
            Text("Done", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 18.sp)
        }
        
        Column(
            modifier = Modifier.fillMaxWidth().padding(bottom = 32.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text("Powered by", fontSize = 12.sp, color = Color.White.copy(alpha = 0.7f))
            Spacer(modifier = Modifier.height(8.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
                coil.compose.AsyncImage(
                    model = coil.request.ImageRequest.Builder(androidx.compose.ui.platform.LocalContext.current)
                        .data("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/UPI-Logo-vector.svg/1024px-UPI-Logo-vector.svg.png")
                        .crossfade(true)
                        .build(),
                    contentDescription = "UPI",
                    modifier = Modifier.height(20.dp),
                    colorFilter = androidx.compose.ui.graphics.ColorFilter.tint(Color.White),
                    contentScale = androidx.compose.ui.layout.ContentScale.Fit
                )
                Spacer(modifier = Modifier.width(8.dp))
                Text("|", color = Color.White.copy(alpha = 0.7f))
                Spacer(modifier = Modifier.width(8.dp))
                coil.compose.AsyncImage(
                    model = coil.request.ImageRequest.Builder(androidx.compose.ui.platform.LocalContext.current)
                        .data("https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/ICICI_Bank_Logo.svg/512px-ICICI_Bank_Logo.svg.png")
                        .crossfade(true)
                        .build(),
                    contentDescription = "ICICI Bank",
                    modifier = Modifier.height(20.dp),
                    contentScale = androidx.compose.ui.layout.ContentScale.Fit
                )
            }
        }
    }
}
