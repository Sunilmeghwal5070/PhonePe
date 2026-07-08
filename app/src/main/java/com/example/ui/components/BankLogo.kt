package com.example.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AccountBalance
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import coil.request.ImageRequest

@Composable
fun BankLogo(bankName: String, size: Dp = 40.dp) {
    val domain = when (bankName.lowercase().trim()) {
        "state bank of india", "sbi" -> "sbi.co.in"
        "hdfc bank", "hdfc" -> "hdfcbank.com"
        "icici bank", "icici" -> "icicibank.com"
        "punjab national bank", "pnb" -> "pnbindia.in"
        "bank of baroda", "bob" -> "bankofbaroda.in"
        "axis bank", "axis" -> "axisbank.com"
        "paytm payments bank", "paytm" -> "paytmbank.com"
        "union bank of india", "union bank" -> "unionbankofindia.co.in"
        "canara bank" -> "canarabank.com"
        "kotak mahindra bank", "kotak" -> "kotak.com"
        "yes bank" -> "yesbank.in"
        "indusind bank" -> "indusind.com"
        "idfc first bank" -> "idfcfirstbank.com"
        else -> null
    }

    if (domain != null) {
        val logoUrl = "https://logo.clearbit.com/$domain"
        AsyncImage(
            model = ImageRequest.Builder(LocalContext.current)
                .data(logoUrl)
                .crossfade(true)
                .build(),
            contentDescription = bankName,
            contentScale = ContentScale.Fit,
            modifier = Modifier
                .size(size)
                .clip(CircleShape)
                .background(Color.White)
                .border(1.dp, Color(0xFFEEEEEE), CircleShape)
                .padding(4.dp)
        )
    } else {
        Box(
            modifier = Modifier
                .size(size)
                .background(Color.White, CircleShape)
                .border(1.dp, Color(0xFFEEEEEE), CircleShape),
            contentAlignment = Alignment.Center
        ) {
            Icon(Icons.Default.AccountBalance, contentDescription = null, tint = Color(0xFF1976D2), modifier = Modifier.size(size * 0.6f))
        }
    }
}
