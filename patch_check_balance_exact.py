import re

content = """package com.example.ui.screens

import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.ExperimentalAnimationApi
import androidx.compose.animation.core.*
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.*
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.rotate
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

enum class CheckBalanceState {
    LIST,
    PIN,
    LOADING,
    SUCCESS
}

@OptIn(ExperimentalMaterial3Api::class, ExperimentalAnimationApi::class)
@Composable
fun CheckBalanceScreen(onBack: () -> Unit) {
    var currentState by remember { mutableStateOf(CheckBalanceState.LIST) }
    var enteredPin by remember { mutableStateOf("") }

    AnimatedContent(targetState = currentState, label = "screen_transition") { state ->
        when (state) {
            CheckBalanceState.LIST -> {
                BalanceListScreen(
                    onBack = onBack,
                    onAccountClick = { currentState = CheckBalanceState.PIN }
                )
            }
            CheckBalanceState.PIN -> {
                PinEntryScreen(
                    pin = enteredPin,
                    onPinChange = { newPin -> enteredPin = newPin },
                    onSubmit = { 
                        currentState = CheckBalanceState.LOADING
                    }
                )
            }
            CheckBalanceState.LOADING -> {
                LoadingScreen()
                LaunchedEffect(Unit) {
                    delay(2000) // 2 seconds loading
                    currentState = CheckBalanceState.SUCCESS
                }
            }
            CheckBalanceState.SUCCESS -> {
                SuccessScreen(
                    onBack = { 
                        currentState = CheckBalanceState.LIST
                        enteredPin = ""
                    }
                )
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun BalanceListScreen(onBack: () -> Unit, onAccountClick: () -> Unit) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Check Balance", fontWeight = FontWeight.Bold, fontSize = 20.sp) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    IconButton(onClick = { }) {
                        Icon(Icons.AutoMirrored.Filled.HelpOutline, contentDescription = "Help")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = Color.White
                )
            )
        },
        containerColor = Color.White
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .verticalScroll(rememberScrollState())
        ) {
            // Banner
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                shape = RoundedCornerShape(12.dp),
                colors = CardDefaults.cardColors(containerColor = Color.White),
                elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text(
                                text = "Daily Mutual Fund SIP @ ₹10!",
                                fontWeight = FontWeight.Bold,
                                fontSize = 14.sp
                            )
                            Spacer(modifier = Modifier.width(8.dp))
                            Box(
                                modifier = Modifier
                                    .size(20.dp)
                                    .background(Color.Black, CircleShape),
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(
                                    imageVector = Icons.AutoMirrored.Filled.ArrowForward,
                                    contentDescription = null,
                                    tint = Color.White,
                                    modifier = Modifier.size(12.dp)
                                )
                            }
                        }
                        Spacer(modifier = Modifier.height(4.dp))
                        Text(
                            text = "Invest now",
                            color = Color.Gray,
                            fontSize = 13.sp
                        )
                    }
                    Box(
                        modifier = Modifier
                            .size(48.dp)
                            .background(Color(0xFFE3F2FD), RoundedCornerShape(8.dp)),
                        contentAlignment = Alignment.Center
                    ) {
                        Text("₹10", color = Color(0xFFE91E63), fontWeight = FontWeight.Bold)
                    }
                }
            }

            Spacer(modifier = Modifier.height(8.dp))

            // Canara Bank Account
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable { onAccountClick() }
                    .padding(horizontal = 16.dp, vertical = 12.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Box(
                    modifier = Modifier
                        .size(40.dp)
                        .border(1.dp, Color(0xFFEEEEEE), CircleShape),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(Icons.Default.AccountBalance, contentDescription = null, tint = Color(0xFF1976D2), modifier = Modifier.size(24.dp))
                }
                
                Spacer(modifier = Modifier.width(16.dp))
                
                Column(modifier = Modifier.weight(1f)) {
                    Text("Canara Bank", fontSize = 16.sp, color = Color.Black)
                    Text("Bank Account", color = Color.Gray, fontSize = 14.sp)
                }
                
                Icon(
                    imageVector = Icons.AutoMirrored.Filled.KeyboardArrowRight,
                    contentDescription = null,
                    tint = Color.Gray
                )
            }
            
            HorizontalDivider(color = Color(0xFFF5F5F5), thickness = 1.dp, modifier = Modifier.padding(start = 72.dp))

            // PhonePe Wallet
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable { }
                    .padding(horizontal = 16.dp, vertical = 16.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(
                    imageVector = Icons.Default.AccountBalanceWallet,
                    contentDescription = null,
                    tint = Color(0xFFE65100),
                    modifier = Modifier.size(32.dp).padding(start = 4.dp, end = 4.dp)
                )
                
                Spacer(modifier = Modifier.width(16.dp))
                
                Column(modifier = Modifier.weight(1f)) {
                    Text("PhonePe Wallet", fontSize = 16.sp, color = Color.Black)
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Box(
                            modifier = Modifier
                                .size(14.dp)
                                .background(Color(0xFF168039), CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Text("%", color = Color.White, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                        }
                        Spacer(modifier = Modifier.width(4.dp))
                        Text("Earn up to 2% cashback", color = Color(0xFF168039), fontSize = 13.sp)
                    }
                }
                
                Text(
                    text = "Activate",
                    color = Color(0xFF5f259f),
                    fontWeight = FontWeight.Bold,
                    fontSize = 14.sp
                )
            }
            
            HorizontalDivider(color = Color(0xFFF5F5F5), thickness = 1.dp, modifier = Modifier.padding(start = 72.dp))

            // Add new payment method
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable { }
                    .padding(horizontal = 16.dp, vertical = 16.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(
                    imageVector = Icons.Default.AddCircleOutline,
                    contentDescription = null,
                    tint = Color.Black,
                    modifier = Modifier.size(32.dp).padding(start = 4.dp, end = 4.dp)
                )
                
                Spacer(modifier = Modifier.width(16.dp))
                
                Column(modifier = Modifier.weight(1f)) {
                    Text("Add new payment method", fontSize = 16.sp, color = Color.Black)
                    Text("Bank Account, UPI Lite & more", color = Color.Gray, fontSize = 13.sp)
                }
                
                Icon(
                    imageVector = Icons.AutoMirrored.Filled.KeyboardArrowRight,
                    contentDescription = null,
                    tint = Color.Gray
                )
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(300.dp)
                    .background(Color(0xFFF5F5F5))
            )
        }
    }
}

@Composable
fun PinEntryScreen(pin: String, onPinChange: (String) -> Unit, onSubmit: () -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.White)
    ) {
        // Top Header
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp, vertical = 12.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column {
                Text("Canara Bank", fontSize = 18.sp, color = Color.Black)
                Text("XXXXXXXX0513", fontSize = 16.sp, color = Color.Black)
            }
            Column(horizontalAlignment = Alignment.End) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("UPI", fontWeight = FontWeight.Bold, fontStyle = FontStyle.Italic, fontSize = 24.sp, color = Color(0xFF666666))
                    Icon(Icons.Default.PlayArrow, contentDescription = null, tint = Color(0xFF168039), modifier = Modifier.size(20.dp))
                }
                Text("UNIFIED PAYMENTS INTERFACE", fontSize = 6.sp, color = Color.Gray)
            }
        }
        
        // Gray Check Balance Bar
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .background(Color(0xFFEEEEEE))
                .padding(horizontal = 16.dp, vertical = 8.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text("Check Balance", fontSize = 16.sp, color = Color.Gray)
            Icon(Icons.Default.KeyboardArrowDown, contentDescription = null, tint = Color.Black)
        }
        
        Spacer(modifier = Modifier.height(24.dp))
        
        Text(
            text = "ENTER 4-DIGIT UPI PIN",
            fontSize = 14.sp,
            color = Color.Black,
            modifier = Modifier.fillMaxWidth(),
            textAlign = TextAlign.Center
        )
        
        Spacer(modifier = Modifier.height(32.dp))
        
        // PIN Dots
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.Center,
            verticalAlignment = Alignment.CenterVertically
        ) {
            for (i in 0 until 4) {
                Box(
                    modifier = Modifier
                        .padding(horizontal = 12.dp)
                        .width(24.dp)
                        .height(24.dp),
                    contentAlignment = Alignment.Center
                ) {
                    if (i < pin.length) {
                        Box(modifier = Modifier.size(12.dp).background(Color.Black, CircleShape))
                    } else {
                        HorizontalDivider(modifier = Modifier.width(24.dp), thickness = 1.dp, color = Color.Black)
                    }
                }
            }
        }
        
        Spacer(modifier = Modifier.weight(1f))
        
        Text(
            text = "UPI PIN will keep your account secure from\nunauthorized access. Do not share this PIN\nwith anyone.",
            fontSize = 13.sp,
            color = Color.Gray,
            textAlign = TextAlign.Center,
            fontWeight = FontWeight.Bold,
            modifier = Modifier.fillMaxWidth().padding(horizontal = 32.dp)
        )
        
        Spacer(modifier = Modifier.height(32.dp))
        
        // Keypad
        Box(modifier = Modifier.fillMaxWidth().background(Color(0xFFF2F2F2))) {
            Column(modifier = Modifier.fillMaxWidth().padding(vertical = 12.dp)) {
                val buttonModifier = Modifier.weight(1f).height(64.dp)
                
                @Composable
                fun KeypadRow(n1: String, n2: String, n3: String) {
                    Row(modifier = Modifier.fillMaxWidth()) {
                        KeypadButton(n1, buttonModifier) { if (pin.length < 4) onPinChange(pin + n1) }
                        KeypadButton(n2, buttonModifier) { if (pin.length < 4) onPinChange(pin + n2) }
                        KeypadButton(n3, buttonModifier) { if (pin.length < 4) onPinChange(pin + n3) }
                    }
                }
                
                KeypadRow("1", "2", "3")
                KeypadRow("4", "5", "6")
                KeypadRow("7", "8", "9")
                
                Row(modifier = Modifier.fillMaxWidth()) {
                    Box(modifier = buttonModifier.clickable { if (pin.isNotEmpty()) onPinChange(pin.dropLast(1)) }, contentAlignment = Alignment.Center) {
                        Canvas(modifier = Modifier.size(32.dp, 24.dp)) {
                            val w = size.width
                            val h = size.height
                            val path = Path().apply {
                                moveTo(w * 0.3f, 0f)
                                lineTo(w, 0f)
                                lineTo(w, h)
                                lineTo(w * 0.3f, h)
                                lineTo(0f, h / 2f)
                                close()
                            }
                            drawPath(path, color = Color(0xFF071252))
                            
                            drawLine(Color.White, start = androidx.compose.ui.geometry.Offset(w*0.45f, h*0.25f), end = androidx.compose.ui.geometry.Offset(w*0.8f, h*0.75f), strokeWidth = 4f, cap = StrokeCap.Round)
                            drawLine(Color.White, start = androidx.compose.ui.geometry.Offset(w*0.8f, h*0.25f), end = androidx.compose.ui.geometry.Offset(w*0.45f, h*0.75f), strokeWidth = 4f, cap = StrokeCap.Round)
                        }
                    }
                    KeypadButton("0", buttonModifier) { if (pin.length < 4) onPinChange(pin + "0") }
                    Box(modifier = buttonModifier.clickable { if (pin.length == 4) onSubmit() }, contentAlignment = Alignment.Center) {
                        Box(
                            modifier = Modifier.size(44.dp).background(if (pin.length == 4) Color(0xFF071252) else Color.Gray, CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(Icons.Default.Check, contentDescription = "Submit", tint = Color.White, modifier = Modifier.size(28.dp))
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun KeypadButton(number: String, modifier: Modifier, onClick: () -> Unit) {
    Box(
        modifier = modifier.clickable(onClick = onClick),
        contentAlignment = Alignment.Center
    ) {
        Text(text = number, fontSize = 32.sp, fontWeight = FontWeight.ExtraBold, color = Color(0xFF071252))
    }
}

@Composable
fun LoadingScreen() {
    Column(
        modifier = Modifier.fillMaxSize().background(Color.White),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(modifier = Modifier.weight(1f))
        
        val infiniteTransition = rememberInfiniteTransition(label = "loading")
        val rotation by infiniteTransition.animateFloat(
            initialValue = 0f,
            targetValue = 360f,
            animationSpec = infiniteRepeatable(
                animation = tween(1200, easing = LinearEasing),
                repeatMode = RepeatMode.Restart
            ),
            label = "rotation"
        )
        
        Canvas(modifier = Modifier.size(100.dp).rotate(rotation)) {
            drawArc(
                color = Color(0xFFFFF9E6),
                startAngle = 0f,
                sweepAngle = 360f,
                useCenter = false,
                style = Stroke(width = 6.dp.toPx(), cap = StrokeCap.Round)
            )
            drawArc(
                color = Color(0xFFF57C00),
                startAngle = -90f,
                sweepAngle = 120f,
                useCenter = false,
                style = Stroke(width = 6.dp.toPx(), cap = StrokeCap.Round)
            )
        }
        
        Spacer(modifier = Modifier.height(32.dp))
        
        Text("Fetching bank balance", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color(0xFF222222))
        
        Spacer(modifier = Modifier.weight(1f))
        
        Text("Please do not press back or close the app", fontSize = 12.sp, color = Color(0xFF666666), modifier = Modifier.padding(bottom = 24.dp))
    }
}

@Composable
fun SuccessScreen(onBack: () -> Unit) {
    androidx.activity.compose.BackHandler { onBack() }
    
    Column(
        modifier = Modifier.fillMaxSize().background(Color.White),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(modifier = Modifier.height(48.dp))
        
        Box(
            modifier = Modifier.size(120.dp).background(Color(0xFF388E3C), CircleShape),
            contentAlignment = Alignment.Center
        ) {
            Icon(Icons.Default.Check, contentDescription = "Success", tint = Color.White, modifier = Modifier.size(80.dp))
        }
        
        Spacer(modifier = Modifier.height(32.dp))
        
        Text(
            text = "Available Balance fetched\\nsuccessful",
            fontSize = 22.sp,
            fontWeight = FontWeight.Bold,
            color = Color.Black,
            textAlign = TextAlign.Center,
            modifier = Modifier.padding(horizontal = 24.dp)
        )
        
        Spacer(modifier = Modifier.height(24.dp))
        
        Row(verticalAlignment = Alignment.CenterVertically) {
            Canvas(modifier = Modifier.size(24.dp)) {
                val path1 = Path().apply {
                    moveTo(size.width * 0.2f, size.height * 0.8f)
                    lineTo(size.width * 0.5f, size.height * 0.2f)
                    lineTo(size.width * 0.8f, size.height * 0.8f)
                    close()
                }
                drawPath(path1, color = Color(0xFF1976D2), style = Stroke(width = 2.dp.toPx()))
                
                val path2 = Path().apply {
                    moveTo(size.width * 0.2f, size.height * 0.4f)
                    lineTo(size.width * 0.5f, size.height * 1.0f)
                    lineTo(size.width * 0.8f, size.height * 0.4f)
                    close()
                }
                drawPath(path2, color = Color(0xFFFFC107), style = Stroke(width = 2.dp.toPx()))
            }
            Spacer(modifier = Modifier.width(12.dp))
            Text("Canara Bank - 0513", fontSize = 18.sp, color = Color.Black)
        }
        
        Spacer(modifier = Modifier.height(24.dp))
        
        Text("Available Balance", fontSize = 14.sp, color = Color.Gray)
        Spacer(modifier = Modifier.height(8.dp))
        Text("₹10", fontSize = 42.sp, color = Color.Black)
        
        Spacer(modifier = Modifier.height(48.dp))
        HorizontalDivider(thickness = 1.dp, color = Color(0xFFF0F0F0))
        
        Spacer(modifier = Modifier.height(24.dp))
        Text("EXPLORE WITH CHATGPT", fontSize = 11.sp, color = Color.Gray, fontWeight = FontWeight.Bold, letterSpacing = 1.sp)
        Spacer(modifier = Modifier.height(24.dp))
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceEvenly
        ) {
            IconColumn(Icons.Default.Lightbulb, "Ask Me\\nAnything")
            IconColumn(Icons.Default.Calculate, "Plan My\\nBudget")
            IconColumn(Icons.Default.Image, "Create Any\\nImage")
            IconColumn(Icons.Default.Settings, "Know Your\\nAstrology")
        }
        
        Spacer(modifier = Modifier.weight(1f))
        
        Card(
            modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 16.dp),
            colors = CardDefaults.cardColors(containerColor = Color(0xFF1E073D)),
            shape = RoundedCornerShape(12.dp)
        ) {
            Column(modifier = Modifier.padding(16.dp).fillMaxWidth()) {
                Text("Personal Loan from", color = Color(0xFFD8B4E2), fontSize = 14.sp, modifier = Modifier.align(Alignment.CenterHorizontally))
                Spacer(modifier = Modifier.height(4.dp))
                Text("₹6K to ₹10L", color = Color.White, fontSize = 28.sp, fontWeight = FontWeight.Bold, modifier = Modifier.align(Alignment.CenterHorizontally))
                
                Spacer(modifier = Modifier.height(16.dp))
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceEvenly,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Box(contentAlignment = Alignment.Center) {
                        Icon(Icons.Default.Timer, contentDescription = null, tint = Color(0xFF9FA8DA), modifier = Modifier.size(48.dp))
                        Text("10 MINS", color = Color.White, fontSize = 10.sp, fontWeight = FontWeight.Bold, modifier = Modifier.align(Alignment.BottomCenter).offset(y = 12.dp))
                    }
                    
                    Icon(Icons.Default.LocalMall, contentDescription = null, tint = Color(0xFF90CAF9), modifier = Modifier.size(64.dp))
                }
                Spacer(modifier = Modifier.height(8.dp))
            }
        }
    }
}

@Composable
fun IconColumn(icon: androidx.compose.ui.graphics.vector.ImageVector, label: String) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Box(
            modifier = Modifier.size(56.dp).border(1.dp, Color(0xFFEEEEEE), CircleShape),
            contentAlignment = Alignment.Center
        ) {
            Icon(icon, contentDescription = null, tint = Color.DarkGray, modifier = Modifier.size(28.dp))
        }
        Spacer(modifier = Modifier.height(12.dp))
        Text(label, fontSize = 11.sp, color = Color.Gray, textAlign = TextAlign.Center, lineHeight = 14.sp)
    }
}
"""

with open('app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt', 'w') as f:
    f.write(content)
