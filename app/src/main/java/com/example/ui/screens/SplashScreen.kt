package com.example.ui.screens

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.GenericShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.Language
import androidx.compose.material.icons.filled.Shield
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.ui.theme.PhonePePurple
import com.example.ui.theme.PhonePeSuccessGreen
import com.example.ui.theme.PhonePeTextDark
import com.example.ui.theme.PhonePeTextMuted
import kotlinx.coroutines.delay

@Composable
fun SplashScreen(
    onTimeout: () -> Unit
) {
    LaunchedEffect(Unit) {
        delay(2000) // Show splash for 2 seconds
        onTimeout()
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.White)
            .padding(16.dp)
    ) {
        // Centered Main Logo
        Column(
            modifier = Modifier.align(Alignment.Center),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // Centered App Logo
            Image(
                painter = androidx.compose.ui.res.painterResource(id = com.example.R.drawable.ic_launcher_foreground),
                contentDescription = "Logo",
                contentScale = androidx.compose.ui.layout.ContentScale.Crop,
                modifier = Modifier
                    .size(125.dp)
                    .clip(CircleShape)
                    .background(PhonePePurple)
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            // "PhonePe" Text below logo
            Text(
                text = "PhonePe",
                color = PhonePePurple,
                fontSize = 42.sp,
                fontWeight = FontWeight.ExtraBold,
                fontFamily = FontFamily.SansSerif,
                letterSpacing = (-1).sp
            )
        }

        // Bottom Footer (Security & Compliance Badges)
        Row(
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .padding(bottom = 32.dp)
                .fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceEvenly,
            verticalAlignment = Alignment.CenterVertically
        ) {
            // 1. PCI DSS COMPLIANT
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(4.dp)
            ) {
                Icon(
                    imageVector = Icons.Default.CheckCircle,
                    contentDescription = null,
                    tint = PhonePeSuccessGreen,
                    modifier = Modifier.size(24.dp)
                )
                Column {
                    Text(
                        text = "PCI DSS",
                        color = Color(0xFF6B21A8), // Deep purple for PCI label
                        fontWeight = FontWeight.Bold,
                        fontSize = 11.sp,
                        lineHeight = 12.sp
                    )
                    Text(
                        text = "COMPLIANT",
                        color = PhonePeTextMuted,
                        fontSize = 8.sp,
                        fontWeight = FontWeight.SemiBold,
                        lineHeight = 9.sp
                    )
                }
            }

            // 2. 100% SECURED Shield
            Column(
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.spacedBy(1.dp)
            ) {
                // Custom drawn green shield
                Box(
                    modifier = Modifier
                        .size(34.dp, 38.dp)
                        .background(PhonePeSuccessGreen, shape = GenericShape { size, _ ->
                            moveTo(size.width / 2f, 0f)
                            lineTo(size.width, size.height * 0.25f)
                            lineTo(size.width, size.height * 0.7f)
                            quadraticTo(size.width, size.height, size.width / 2f, size.height)
                            quadraticTo(0f, size.height, 0f, size.height * 0.7f)
                            lineTo(0f, size.height * 0.25f)
                            close()
                        }),
                    contentAlignment = Alignment.Center
                ) {
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.Center,
                        modifier = Modifier.offset(y = (-1).dp)
                    ) {
                        Text(
                            text = "100%",
                            color = Color.White,
                            fontSize = 9.sp,
                            fontWeight = FontWeight.ExtraBold,
                            lineHeight = 10.sp
                        )
                        Text(
                            text = "SECURED",
                            color = Color.White,
                            fontSize = 6.sp,
                            fontWeight = FontWeight.Bold,
                            lineHeight = 7.sp
                        )
                    }
                }
            }

            // 3. ISO 27001 CERTIFIED
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(4.dp)
            ) {
                Icon(
                    imageVector = Icons.Default.Language,
                    contentDescription = null,
                    tint = PhonePeSuccessGreen,
                    modifier = Modifier.size(24.dp)
                )
                Column {
                    Text(
                        text = "ISO 27001",
                        color = Color(0xFF6B21A8),
                        fontWeight = FontWeight.Bold,
                        fontSize = 11.sp,
                        lineHeight = 12.sp
                    )
                    Text(
                        text = "CERTIFIED",
                        color = PhonePeTextMuted,
                        fontSize = 8.sp,
                        fontWeight = FontWeight.SemiBold,
                        lineHeight = 9.sp
                    )
                }
            }
        }
    }
}
