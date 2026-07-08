package com.example.ui.screens

import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.ExperimentalAnimationApi
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.KeyboardArrowDown
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.animation.core.*
import androidx.compose.ui.draw.scale
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.delay
import com.example.ui.PrankViewModel
import androidx.compose.ui.text.style.TextAlign
import android.widget.Toast
import androidx.compose.ui.platform.LocalContext

@Composable
fun RechargePinScreen(
    amount: String,
    bankId: String,
    viewModel: PrankViewModel,
    onBack: () -> Unit,
    onSuccess: () -> Unit
) {
    val bankAccounts by viewModel.bankAccounts.collectAsState()
    val account = bankAccounts.find { it.id == bankId } ?: bankAccounts.firstOrNull()
    
    var enteredPin by remember { mutableStateOf("") }
    val context = LocalContext.current

    PinEntryScreen(
        bankName = account?.bankName ?: "Bank",
        actionText = "Recharge Mobile",
        pin = enteredPin,
        onPinChange = { enteredPin = it },
        onSubmit = {
            if (enteredPin == account?.pin) {
                // Deduct balance
                account?.let { 
                    val currentBal = it.balance
                    val amt = amount.toDoubleOrNull() ?: 0.0
                    viewModel.updateBankAccount(it.copy(balance = (currentBal - amt)))
                }
                onSuccess()
            } else {
                Toast.makeText(context, "Incorrect UPI PIN", Toast.LENGTH_SHORT).show()
                enteredPin = ""
            }
        }
    )
}

@Composable
fun RechargeProcessingScreen(
    name: String,
    amount: String,
    onSuccess: (Int) -> Unit
) {
    var step by remember { mutableStateOf(0) }

    LaunchedEffect(Unit) {
        delay(1500)
        step = 1
        delay(1500)
        onSuccess((1000000000..Int.MAX_VALUE).random()) // Random Transaction ID
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.White),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        CircularProgressIndicator(color = Color(0xFF5f259f), modifier = Modifier.size(64.dp))
        Spacer(modifier = Modifier.height(24.dp))
        Text(
            if (step == 0) "Connecting securely..." else "Processing Recharge of ₹$amount to $name",
            fontSize = 16.sp,
            fontWeight = FontWeight.Medium,
            color = Color.Black
        )
    }
}

@Composable
fun RechargeSuccessScreen(
    amount: String,
    name: String,
    transactionId: Int,
    onDone: () -> Unit
) {

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
            .background(Color(0xFFE8F5E9)),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(modifier = Modifier.height(64.dp))
        
        Box(
            modifier = Modifier
                .size(100.dp)
                .scale(scale)
                .background(Color(0xFF4CAF50), CircleShape),
            contentAlignment = Alignment.Center
        ) {
            Icon(Icons.Default.Check, contentDescription = "Success", tint = Color.White, modifier = Modifier.size(64.dp))
        }
        
        Spacer(modifier = Modifier.height(24.dp))
        
        Text("Recharge Successful", fontSize = 24.sp, fontWeight = FontWeight.Bold, color = Color(0xFF2E7D32))
        
        Spacer(modifier = Modifier.height(16.dp))
        
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            colors = CardDefaults.cardColors(containerColor = Color.White),
            shape = RoundedCornerShape(12.dp)
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text("Recharge Amount", color = Color.Gray, fontSize = 14.sp)
                    Text("₹$amount", fontWeight = FontWeight.Bold, fontSize = 16.sp)
                }
                Spacer(modifier = Modifier.height(12.dp))
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text("Mobile Number", color = Color.Gray, fontSize = 14.sp)
                    Text(name, fontWeight = FontWeight.Medium, fontSize = 14.sp)
                }
                Spacer(modifier = Modifier.height(12.dp))
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text("Transaction ID", color = Color.Gray, fontSize = 14.sp)
                    Text("T$transactionId", fontWeight = FontWeight.Medium, fontSize = 14.sp)
                }
            }
        }
        
        Spacer(modifier = Modifier.weight(1f))
        
        Button(
            onClick = onDone,
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
                .height(50.dp),
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF5f259f)),
            shape = RoundedCornerShape(8.dp)
        ) {
            Text("DONE", color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
        }
        
        Spacer(modifier = Modifier.height(24.dp))
    }
}
