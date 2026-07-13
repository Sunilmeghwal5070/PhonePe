package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.PriorityHigh
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.ui.theme.PhonePePurple

@Composable
fun WrongPinScreen(
    bankName: String,
    bankDesc: String,
    errorTitle: String = "Payment failed",
    onResetPin: () -> Unit,
    onReEnterPin: () -> Unit,
    onDone: () -> Unit
) {
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFF5E5E5E)) // Dark grey background
    ) {
        // Center Error Icon
        Column(
            modifier = Modifier.align(Alignment.Center).offset(y = (-80).dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Box(
                modifier = Modifier
                    .size(100.dp)
                    .border(6.dp, Color(0xFFD32F2F), CircleShape),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.Default.PriorityHigh,
                    contentDescription = "Error",
                    tint = Color(0xFFD32F2F),
                    modifier = Modifier.size(60.dp)
                )
            }
            Spacer(modifier = Modifier.height(24.dp))
            Text(
                text = errorTitle,
                color = Color.White,
                fontSize = 22.sp,
                fontWeight = FontWeight.Bold,
                textAlign = TextAlign.Center,
                lineHeight = 28.sp
            )
        }

        // Bottom Sheet part
        Column(
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .fillMaxWidth()
                .background(Color.White, RoundedCornerShape(topStart = 16.dp, topEnd = 16.dp))
                .padding(24.dp)
        ) {
            Text(
                text = if (errorTitle.contains("Insufficient", ignoreCase = true)) "Insufficient Balance" else "Wrong UPI PIN",
                fontSize = 24.sp,
                fontWeight = FontWeight.Bold,
                color = Color.Black
            )
            if (!errorTitle.contains("Insufficient", ignoreCase = true)) {
                Text("Hint: The default PIN is 1234 (change it in Bank Accounts).", fontSize = 12.sp, color = Color.Gray)
            }
            Spacer(modifier = Modifier.height(16.dp))
            
            Row(verticalAlignment = Alignment.CenterVertically) {
                com.example.ui.components.BankLogo(bankName = bankName, size = 24.dp)
                Spacer(modifier = Modifier.width(12.dp))
                Text(
                    text = bankDesc,
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.Black
                )
            }
            Spacer(modifier = Modifier.height(16.dp))
            
            Row(verticalAlignment = Alignment.Top) {
                Text("•", fontSize = 16.sp, color = Color.Black, modifier = Modifier.padding(end = 8.dp))
                Text(
                    text = if (errorTitle.contains("Insufficient", ignoreCase = true)) "Your bank account does not have sufficient balance for this transaction. Please try again with a lower amount or use another account." else "You've entered the wrong UPI PIN. Please check and try again.",
                    fontSize = 15.sp,
                    color = Color.DarkGray,
                    lineHeight = 20.sp
                )
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                OutlinedButton(
                    onClick = onResetPin,
                    modifier = Modifier.weight(1f),
                    border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFF5f259f)),
                    colors = ButtonDefaults.outlinedButtonColors(contentColor = Color(0xFF5f259f))
                ) {
                    Text("RESET UPI PIN")
                }
                OutlinedButton(
                    onClick = onReEnterPin,
                    modifier = Modifier.weight(1f),
                    border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFF5f259f)),
                    colors = ButtonDefaults.outlinedButtonColors(contentColor = Color(0xFF5f259f))
                ) {
                    Text("RE-ENTER UPI PIN")
                }
            }
            
            HorizontalDivider(modifier = Modifier.padding(vertical = 16.dp), color = Color(0xFFF0F0F0))
            
            Text(
                text = "DONE",
                color = Color(0xFF5f259f),
                fontWeight = FontWeight.Bold,
                fontSize = 16.sp,
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable { onDone() }
                    .padding(vertical = 8.dp),
                textAlign = TextAlign.Center
            )
        }
    }
}


