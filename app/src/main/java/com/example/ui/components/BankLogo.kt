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
import androidx.compose.ui.res.painterResource
import android.annotation.SuppressLint
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import coil.request.ImageRequest

@SuppressLint("DiscouragedApi")
@Composable
fun BankLogo(bankName: String, size: Dp = 40.dp, modifier: Modifier = Modifier) {
    val context = LocalContext.current
    
    val safeBankName = bankName.lowercase().replace(" ", "_").replace("-", "_")
    
    val imageCode = when {
        safeBankName.contains("state_bank") || safeBankName == "sbi" -> "sbi"
        safeBankName.contains("hdfc") -> "hdfc"
        safeBankName.contains("icici") -> "icici"
        safeBankName.contains("punjab") || safeBankName == "pnb" -> "pnb"
        safeBankName.contains("baroda") || safeBankName == "bob" -> "bob"
        safeBankName.contains("axis") -> "axis"
        safeBankName.contains("paytm") -> "paytm"
        safeBankName.contains("union") -> "union"
        safeBankName.contains("canara") -> "canara"
        safeBankName.contains("kotak") -> "kotak"
        safeBankName.contains("yes_bank") -> "yes"
        safeBankName.contains("indusind") -> "indusind"
        safeBankName.contains("idfc") -> "idfc"
        safeBankName.contains("india_post") -> "ippb"
        safeBankName.contains("airtel") -> "airtel"
        else -> safeBankName
    }
    
    val expectedDrawableName = "logo_$imageCode"
    val resourceId = context.resources.getIdentifier(expectedDrawableName, "drawable", context.packageName)
    
    val isSmall = size < 24.dp
    
    if (resourceId != 0) {
        androidx.compose.foundation.Image(
            painter = painterResource(id = resourceId),
            contentDescription = bankName,
            contentScale = ContentScale.Fit,
            modifier = modifier
                .size(size)
                .clip(CircleShape)
                .background(Color.White)
        )
    } else {
        val domain = when (imageCode) {
            "sbi" -> "sbi.co.in"
            "hdfc" -> "hdfcbank.com"
            "icici" -> "icicibank.com"
            "pnb" -> "pnbindia.in"
            "bob" -> "bankofbaroda.in"
            "axis" -> "axisbank.com"
            "paytm" -> "paytmbank.com"
            "union" -> "unionbankofindia.co.in"
            "canara" -> "canarabank.com"
            "kotak" -> "kotak.com"
            "yes" -> "yesbank.in"
            "indusind" -> "indusind.com"
            "idfc" -> "idfcfirstbank.com"
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
                modifier = modifier
                    .size(size)
                    .clip(CircleShape)
                    .background(Color.White)
            )
        } else {
            Box(
                modifier = modifier
                    .size(size)
                    .background(Color.White, CircleShape),
                contentAlignment = Alignment.Center
            ) {
                Icon(Icons.Default.AccountBalance, contentDescription = null, tint = Color(0xFF1976D2), modifier = Modifier.size(size * 0.6f))
            }
        }
    }
}
