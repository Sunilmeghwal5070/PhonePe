package com.example.ui.screens

import android.widget.Toast
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.Phone
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.zIndex
import androidx.compose.ui.draw.clipToBounds
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush

import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.CompositingStrategy
import androidx.compose.ui.draw.drawWithContent
import androidx.compose.ui.graphics.Color
import androidx.compose.animation.core.*
import androidx.compose.animation.animateContentSize
import kotlinx.coroutines.delay
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.data.PrankTransaction
import com.example.ui.PrankViewModel
import com.example.ui.theme.*
import java.text.SimpleDateFormat
import java.util.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    viewModel: PrankViewModel,
    onCreatePrank: () -> Unit,
    onNavigateToReceipt: (Int) -> Unit,
    onNavigateToQr: () -> Unit = {},
    onNavigateToCheckBalance: () -> Unit = {},
    onNavigateToProfile: () -> Unit = {},
    onNavigateToContactList: () -> Unit = {},
    onNavigateToMobileRecharge: () -> Unit = {}
) {
    val context = LocalContext.current
    val transactions by viewModel.allTransactions.collectAsState()
    val userProfile by viewModel.userProfileManager.userProfile.collectAsState()
    
    var showDialogText by remember { mutableStateOf<String?>(null) }
    var showDialogTitle by remember { mutableStateOf<String?>(null) }
    
    var showRechargeReminder by remember { mutableStateOf(!viewModel.hasShownRechargeReminder) }

    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFFF5F6FA))
    ) {
        // 2. Beautiful "Trade with 5x leverage" Grid Ad Banner (Matches screenshot 1 perfectly!)
        item {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(250.dp)
                    .background(Color(0xFF2E0854))
                    .clipToBounds()
            ) {
                // Top App Bar Overlay
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .zIndex(1f) // Ensures this Row renders above the grid animation
                        .padding(horizontal = 14.dp, vertical = 10.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Box(
                        modifier = Modifier
                            .size(52.dp)
                            .clickable { onNavigateToProfile() },
                        contentAlignment = Alignment.Center
                    ) {
                        Box(
                            modifier = Modifier
                                .size(48.dp)
                                .clip(CircleShape)
                                .background(Color(0xFFFBC02D)),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(
                                text = if (userProfile.name.isNotBlank()) userProfile.name.first().toString().uppercase() else "Y",
                                color = Color.White,
                                fontWeight = FontWeight.Bold,
                                fontSize = 24.sp
                            )
                        }
                        Box(
                            modifier = Modifier
                                .size(20.dp)
                                .align(Alignment.BottomEnd)
                                .clip(CircleShape)
                                .background(Color.White)
                                .border(1.dp, Color.LightGray, CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = Icons.Default.QrCode,
                                contentDescription = null,
                                tint = Color(0xFF5f259f),
                                modifier = Modifier.size(12.dp)
                            )
                        }
                    }
                    Icon(
                        imageVector = Icons.Default.HelpOutline,
                        contentDescription = "Help",
                        tint = Color.White,
                        modifier = Modifier
                            .size(24.dp)
                            .clickable {
                                showDialogTitle = "Help & Support 💡"
                                showDialogText = "Here you can manage your settings. Click on 'Money Transfer' to proceed!"
                            }
                    )
                }

                // Animated Lens Distortion effect for grid
                val infiniteTransition = rememberInfiniteTransition(label = "lens")
                val animProgress by infiniteTransition.animateFloat(
                    initialValue = -0.2f,
                    targetValue = 1.2f,
                    animationSpec = infiniteRepeatable(
                        animation = tween(3500, easing = LinearEasing),
                        repeatMode = RepeatMode.Restart
                    ),
                    label = "lensProgress"
                )
                
                // Radial echo effect
                val echoRadius by infiniteTransition.animateFloat(
                    initialValue = 0f,
                    targetValue = 600f,
                    animationSpec = infiniteRepeatable(
                        animation = tween(2500, easing = LinearOutSlowInEasing),
                        repeatMode = RepeatMode.Restart
                    ),
                    label = "echoRadius"
                )
                val echoAlpha by infiniteTransition.animateFloat(
                    initialValue = 0.6f,
                    targetValue = 0f,
                    animationSpec = infiniteRepeatable(
                        animation = tween(2500, easing = LinearOutSlowInEasing),
                        repeatMode = RepeatMode.Restart
                    ),
                    label = "echoAlpha"
                )

                // Background grid lines drawn dynamically with distortion
                Canvas(modifier = Modifier.fillMaxSize()) {
                    val gridSpacing = 24.dp.toPx()
                    val gridColor = Color(0xFF4B1D8C).copy(alpha = 0.6f)
                    
                    val center = Offset(size.width * animProgress, size.height / 2f)
                    val radius = 100.dp.toPx()
                    val maxBulge = 24.dp.toPx()

                    fun bulgePoint(x: Float, y: Float): Offset {
                        val dx = x - center.x
                        val dy = y - center.y
                        val dist = kotlin.math.sqrt(dx * dx + dy * dy)
                        if (dist < radius && dist > 0f) {
                            val bulgeAmount = maxBulge * kotlin.math.sin((1f - dist / radius) * (Math.PI / 2).toFloat()).toFloat()
                            return Offset(
                                x + (dx / dist) * bulgeAmount,
                                y + (dy / dist) * bulgeAmount
                            )
                        }
                        return Offset(x, y)
                    }

                    // Draw radial echo effect
                    drawCircle(
                        color = Color.White.copy(alpha = echoAlpha),
                        radius = echoRadius,
                        center = Offset(size.width / 2f, size.height / 2f),
                        style = Stroke(width = 4f)
                    )
                    drawCircle(
                        color = Color(0xFFCCFF00).copy(alpha = echoAlpha * 0.5f),
                        radius = echoRadius * 0.8f,
                        center = Offset(size.width / 2f, size.height / 2f),
                        style = Stroke(width = 8f)
                    )

                    var x = 0f
                    while (x < size.width) {
                        val path = androidx.compose.ui.graphics.Path()
                        var y = 0f
                        val step = 10f
                        var first = true
                        while (y <= size.height + step) {
                            val p = bulgePoint(x, y)
                            if (first) {
                                path.moveTo(p.x, p.y)
                                first = false
                            } else {
                                path.lineTo(p.x, p.y)
                            }
                            y += step
                        }
                        drawPath(path, color = gridColor, style = Stroke(width = 1f))
                        x += gridSpacing
                    }
                    
                    var yOffset = 0f
                    while (yOffset < size.height) {
                        val path = androidx.compose.ui.graphics.Path()
                        var cx = 0f
                        val step = 10f
                        var first = true
                        while (cx <= size.width + step) {
                            val p = bulgePoint(cx, yOffset)
                            if (first) {
                                path.moveTo(p.x, p.y)
                                first = false
                            } else {
                                path.lineTo(p.x, p.y)
                            }
                            cx += step
                        }
                        drawPath(path, color = gridColor, style = Stroke(width = 1f))
                        yOffset += gridSpacing
                    }
                    
                    drawCircle(
                        color = Color(0xFF7E38D1).copy(alpha = 0.3f),
                        radius = radius * 0.8f,
                        center = center
                    )
                }

                // Banner Content
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(14.dp),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.SpaceBetween
                ) {
                    
                    // Formula Block Animation State
                    var animationStep by remember { mutableIntStateOf(0) }
                    LaunchedEffect(Unit) {
                        while (true) {
                            animationStep = 0
                            delay(1000)
                            animationStep = 1 // show =
                            delay(800)
                            animationStep = 2 // show 500
                            delay(800)
                            animationStep = 3 // shine text
                            delay(2000)
                        }
                    }

                    // Shine effect progress
                    val shimmerProgress by animateFloatAsState(
                        targetValue = if (animationStep >= 3) 2f else -0.5f,
                        animationSpec = tween(durationMillis = 1500, easing = LinearEasing),
                        label = "shimmer"
                    )

                    // Headline
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.Center,
                        modifier = Modifier
                            .graphicsLayer { compositingStrategy = CompositingStrategy.Offscreen }
                            .drawWithContent {
                                drawContent()
                                val w = size.width
                                val startX = shimmerProgress * w
                                val brush = Brush.linearGradient(
                                    colors = listOf(Color.Transparent, Color.White.copy(alpha = 0.5f), Color.Transparent),
                                    start = androidx.compose.ui.geometry.Offset(startX, 0f),
                                    end = androidx.compose.ui.geometry.Offset(startX + (w * 0.3f), 0f)
                                )
                                drawRect(brush = brush, blendMode = androidx.compose.ui.graphics.BlendMode.SrcAtop)
                            }
                    ) {
                        Text(
                            text = "Trade with ",
                            color = Color.White,
                            fontSize = 20.sp,
                            fontWeight = FontWeight.ExtraBold,
                            fontFamily = FontFamily.SansSerif
                        )
                        Text(
                            text = "5x leverage",
                            color = Color(0xFFCCFF00), // Lime Green
                            fontSize = 20.sp,
                            fontWeight = FontWeight.ExtraBold,
                            fontFamily = FontFamily.SansSerif
                        )
                    }

                    // Formula Block
                    Row(
                        modifier = Modifier
                            .animateContentSize()
                            .padding(horizontal = 8.dp)
                            .border(1.dp, Color(0xFF5f259f).copy(alpha = 0.8f), RoundedCornerShape(12.dp))
                            .background(Color(0xFF1E033A).copy(alpha = 0.8f))
                            .padding(horizontal = 14.dp, vertical = 10.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.Center
                    ) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Text("₹100", color = Color.White, fontSize = 24.sp, fontWeight = FontWeight.ExtraBold)
                            Text("balance", color = Color.LightGray, fontSize = 11.sp)
                        }

                        androidx.compose.animation.AnimatedVisibility(
                            visible = animationStep >= 1,
                            enter = androidx.compose.animation.fadeIn() + androidx.compose.animation.expandHorizontally()
                        ) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Spacer(modifier = Modifier.width(16.dp))
                                Text("=", color = Color(0xFFCCFF00), fontSize = 28.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                        
                        androidx.compose.animation.AnimatedVisibility(
                            visible = animationStep >= 2,
                            enter = androidx.compose.animation.fadeIn() + androidx.compose.animation.expandHorizontally()
                        ) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Spacer(modifier = Modifier.width(16.dp))
                                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                    Text("₹500", color = Color.White, fontSize = 24.sp, fontWeight = FontWeight.ExtraBold)
                                    Text("in buying power", color = Color.LightGray, fontSize = 11.sp)
                                }
                            }
                        }
                    }

                    // Call to Action
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.Center,
                        modifier = Modifier
                            .clip(RoundedCornerShape(12.dp))
                            .clickable {
                                // Add click event if needed
                            }
                    ) {
                        Text(
                            text = "Switch to ",
                            color = Color.White,
                            fontSize = 15.sp,
                            fontWeight = FontWeight.Bold
                        )
                        Text(
                            text = "share",
                            color = Color.White,
                            fontSize = 15.sp,
                            fontWeight = FontWeight.ExtraBold
                        )
                        Box(
                            modifier = Modifier
                                .padding(horizontal = 4.dp)
                                .size(6.dp)
                                .clip(CircleShape)
                                .background(Color(0xFF00E676))
                        )
                        Text(
                            text = "market",
                            color = Color(0xFF00E676),
                            fontSize = 15.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                }
            }
        }
        
        // 3. Money Transfers Grid
        item {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(Color.White)
                    .padding(vertical = 16.dp, horizontal = 12.dp)
            ) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = "Money Transfers",
                            fontWeight = FontWeight.Bold,
                            color = PhonePeTextDark,
                            fontSize = 14.sp
                        )
                        
                        // Refer -> ₹200 bubble
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier
                                .clip(RoundedCornerShape(12.dp))
                                .background(Color(0xFFFFF3E0))
                                .clickable {
                                    showDialogTitle = "Referral Bonus 💰"
                                    showDialogText = "Share the link of this app with your friends and get ₹200! 🤑🔥"
                                }
                                .padding(horizontal = 8.dp, vertical = 4.dp)
                        ) {
                            Icon(
                                imageVector = Icons.Default.MonetizationOn,
                                contentDescription = null,
                                tint = Color(0xFFFF9800),
                                modifier = Modifier.size(14.dp)
                            )
                            Spacer(modifier = Modifier.width(4.dp))
                            Text(
                                text = "Refer → ₹200",
                                color = Color(0xFFE65100),
                                fontSize = 11.sp,
                                fontWeight = FontWeight.Bold
                            )
                        }
                    }
                    
                    Spacer(modifier = Modifier.height(18.dp))
                    
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        TransferButton(
                            iconContent = { ToMobileIcon() },
                            label = "To Mobile\nNumber",
                            onClick = onNavigateToContactList
                        )
                        TransferButton(
                            iconContent = { ToBankIcon() },
                            label = "To Bank &\nSelf A/c",
                            onClick = onCreatePrank
                        )
                        TransferButton(
                            iconContent = { PhonePeWalletIcon() },
                            label = "PhonePe\nWallet",
                            onClick = {}
                        )
                        TransferButton(
                            iconContent = { CheckBalanceIcon() },
                            label = "Check\nBalance",
                            onClick = onNavigateToCheckBalance
                        )
                    }
                }
            }

        // 4. Two Capsule Ads Side-by-Side
        item {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 12.dp)
                    .padding(bottom = 12.dp),
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                // Left Capsule Card
                Card(
                    modifier = Modifier
                        .weight(1f)
                        .clickable {
                            Toast.makeText(context, "Silver Savings opening...", Toast.LENGTH_SHORT).show()
                        },
                    colors = CardDefaults.cardColors(containerColor = Color.White),
                    shape = RoundedCornerShape(8.dp),
                    elevation = CardDefaults.cardElevation(1.dp)
                ) {
                    Row(
                        modifier = Modifier.padding(10.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(
                            imageVector = Icons.Default.Savings,
                            contentDescription = null,
                            tint = Color(0xFF78909C),
                            modifier = Modifier.size(20.dp)
                        )
                        Spacer(modifier = Modifier.width(6.dp))
                        Text(
                            text = "Start Silver savings instantly",
                            fontSize = 10.sp,
                            fontWeight = FontWeight.SemiBold,
                            color = PhonePeTextDark,
                            maxLines = 2,
                            overflow = TextOverflow.Visible
                        )
                    }
                }

                // Right Capsule Card
                Card(
                    modifier = Modifier
                        .weight(1f)
                        .clickable {
                            Toast.makeText(context, "Opening share.market...", Toast.LENGTH_SHORT).show()
                        },
                    colors = CardDefaults.cardColors(containerColor = Color.White),
                    shape = RoundedCornerShape(8.dp),
                    elevation = CardDefaults.cardElevation(1.dp)
                ) {
                    Row(
                        modifier = Modifier.padding(10.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(
                            imageVector = Icons.Default.TrendingUp,
                            contentDescription = null,
                            tint = PhonePePurple,
                            modifier = Modifier.size(20.dp)
                        )
                        Spacer(modifier = Modifier.width(6.dp))
                        Text(
                            text = "Trade at ₹0 Brokerage",
                            fontSize = 10.sp,
                            fontWeight = FontWeight.SemiBold,
                            color = PhonePeTextDark,
                            maxLines = 2,
                            overflow = TextOverflow.Visible
                        )
                    }
                }
            }
        }

        // 5. Section: Recharge & Pay Bills
        item {
            Card(
                colors = CardDefaults.cardColors(containerColor = Color.White),
                shape = RoundedCornerShape(12.dp),
                elevation = CardDefaults.cardElevation(1.dp),
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 12.dp)
                    .padding(bottom = 12.dp)
            ) {
                Column(modifier = Modifier.padding(14.dp)) {
                    Text(
                        text = "Recharge & Pay Bills",
                        fontWeight = FontWeight.Bold,
                        color = PhonePeTextDark,
                        fontSize = 14.sp
                    )
                    Spacer(modifier = Modifier.height(14.dp))
                    
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        BillButton(
                            icon = Icons.Default.PhoneAndroid,
                            label = "Mobile\nRecharge",
                            onClick = onNavigateToMobileRecharge
                        )
                        BillButton(
                            icon = Icons.Default.MenuBook,
                            label = "Tuition\nFees",
                            onClick = {
                                Toast.makeText(context, "Tuition fees paid!", Toast.LENGTH_SHORT).show()
                            }
                        )
                        BillButton(
                            icon = Icons.Default.Lightbulb,
                            label = "Electricity\nBill",
                            onClick = {
                                showDialogTitle = "Electricity Bill Warning! ⚡"
                                showDialogText = "Your house electricity bill is ₹1,48,290/-. Superman is coming tomorrow morning to cut your electricity! 🦸‍♂️🔋"
                            }
                        )
                        BillButton(
                            icon = Icons.Default.Payment,
                            label = "Loan\nRepayment",
                            onClick = onCreatePrank
                        )
                    }

                    Spacer(modifier = Modifier.height(14.dp))
                    Divider(color = PhonePeBorderGray, thickness = 0.5.dp)
                    Spacer(modifier = Modifier.height(12.dp))

                    // Jio SIM Banner Row
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable {
                                Toast.makeText(context, "Ordering free Jio SIM...", Toast.LENGTH_SHORT).show()
                            },
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(
                                imageVector = Icons.Default.SimCard,
                                contentDescription = null,
                                tint = Color(0xFFD32F2F),
                                modifier = Modifier.size(20.dp)
                            )
                            Spacer(modifier = Modifier.width(10.dp))
                            Text(
                                text = "Free Delivery of Jio SIM",
                                fontSize = 12.sp,
                                fontWeight = FontWeight.SemiBold,
                                color = PhonePeTextDark
                            )
                        }
                        
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text(
                                text = "More",
                                color = PhonePePurple,
                                fontSize = 12.sp,
                                fontWeight = FontWeight.Bold
                            )
                            Icon(
                                imageVector = Icons.Default.KeyboardArrowRight,
                                contentDescription = null,
                                tint = PhonePePurple,
                                modifier = Modifier.size(16.dp)
                            )
                        }
                    }
                }
            }
        }

        // 6. Section: Loans
        item {
            Card(
                colors = CardDefaults.cardColors(containerColor = Color.White),
                shape = RoundedCornerShape(12.dp),
                elevation = CardDefaults.cardElevation(1.dp),
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 12.dp)
                    .padding(bottom = 12.dp)
            ) {
                Column(modifier = Modifier.padding(14.dp)) {
                    Text(
                        text = "Loans",
                        fontWeight = FontWeight.Bold,
                        color = PhonePeTextDark,
                        fontSize = 14.sp
                    )
                    Spacer(modifier = Modifier.height(14.dp))
                    
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        BillButton(
                            icon = Icons.Default.Person,
                            label = "Personal\nLoan",
                            onClick = {
                                Toast.makeText(context, "Personal Loan eligibility...", Toast.LENGTH_SHORT).show()
                            }
                        )
                        BillButton(
                            icon = Icons.Default.BarChart,
                            label = "Mutual\nFunds Loan",
                            onClick = {
                                Toast.makeText(context, "Mutual Funds Loan...", Toast.LENGTH_SHORT).show()
                            }
                        )
                        BillButton(
                            icon = Icons.Default.Category,
                            label = "Gold\nLoan",
                            onClick = {
                                Toast.makeText(context, "Gold Loan...", Toast.LENGTH_SHORT).show()
                            }
                        )
                        // Credit Score Button with FREE Badge!
                        Column(
                            horizontalAlignment = Alignment.CenterHorizontally,
                            modifier = Modifier
                                .width(80.dp)
                                .clickable {
                                    Toast.makeText(context, "Checking Credit Score...", Toast.LENGTH_SHORT).show()
                                }
                        ) {
                            Box(contentAlignment = Alignment.TopCenter) {
                                Box(
                                    modifier = Modifier
                                        .size(44.dp)
                                        .clip(RoundedCornerShape(12.dp))
                                        .border(1.dp, PhonePeBorderGray, RoundedCornerShape(12.dp))
                                        .background(Color.White),
                                    contentAlignment = Alignment.Center
                                ) {
                                    Icon(imageVector = Icons.Default.Speed, contentDescription = null, tint = PhonePePurple, modifier = Modifier.size(22.dp))
                                }
                                // Tiny "FREE" badge on top of credit score icon
                                Box(
                                    modifier = Modifier
                                        .offset(y = (-8).dp)
                                        .clip(RoundedCornerShape(4.dp))
                                        .background(Color(0xFFE65100))
                                        .padding(horizontal = 4.dp, vertical = 1.dp)
                                ) {
                                    Text("FREE", color = Color.White, fontSize = 7.sp, fontWeight = FontWeight.Bold)
                                }
                            }
                            Spacer(modifier = Modifier.height(6.dp))
                            Text(
                                text = "Credit\nScore",
                                fontSize = 11.sp,
                                color = PhonePeTextDark,
                                textAlign = TextAlign.Center,
                                lineHeight = 14.sp
                            )
                        }
                    }

                    Spacer(modifier = Modifier.height(14.dp))
                    Divider(color = PhonePeBorderGray, thickness = 0.5.dp)
                    Spacer(modifier = Modifier.height(12.dp))

                    // MF Loans Banner Row
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable {
                                Toast.makeText(context, "MF Loans active...", Toast.LENGTH_SHORT).show()
                            },
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(
                                imageVector = Icons.Default.BusinessCenter,
                                contentDescription = null,
                                tint = Color(0xFFFBC02D),
                                modifier = Modifier.size(20.dp)
                            )
                            Spacer(modifier = Modifier.width(10.dp))
                            Text(
                                text = "MF loans starting 10% p.a.",
                                fontSize = 12.sp,
                                fontWeight = FontWeight.SemiBold,
                                color = PhonePeTextDark
                            )
                        }
                        
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text(
                                text = "More",
                                color = PhonePePurple,
                                fontSize = 12.sp,
                                fontWeight = FontWeight.Bold
                            )
                            Icon(
                                imageVector = Icons.Default.KeyboardArrowRight,
                                contentDescription = null,
                                tint = PhonePePurple,
                                modifier = Modifier.size(16.dp)
                            )
                        }
                    }
                }
            }
        }

        // 7. Section: Gold, Silver & Platinum
        item {
            Card(
                colors = CardDefaults.cardColors(containerColor = Color.White),
                shape = RoundedCornerShape(12.dp),
                elevation = CardDefaults.cardElevation(1.dp),
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 12.dp)
                    .padding(bottom = 12.dp)
            ) {
                Column(modifier = Modifier.padding(14.dp)) {
                    Text(
                        text = "Gold, Silver & Platinum",
                        fontWeight = FontWeight.Bold,
                        color = PhonePeTextDark,
                        fontSize = 14.sp
                    )
                    Spacer(modifier = Modifier.height(14.dp))
                    
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        BillButton(
                            icon = Icons.Default.Savings,
                            label = "Daily Gold\nwith ₹10",
                            onClick = {
                                Toast.makeText(context, "Investing ₹10 daily...", Toast.LENGTH_SHORT).show()
                            }
                        )
                        BillButton(
                            icon = Icons.Default.CardGiftcard,
                            label = "Buy\nGold",
                            onClick = {
                                Toast.makeText(context, "Buy Gold...", Toast.LENGTH_SHORT).show()
                            }
                        )
                        BillButton(
                            icon = Icons.Default.Eco,
                            label = "Daily Silver\nwith ₹10",
                            onClick = {
                                Toast.makeText(context, "Investing ₹10 daily in Silver...", Toast.LENGTH_SHORT).show()
                            }
                        )
                        BillButton(
                            icon = Icons.Default.Diamond,
                            label = "Buy\nSilver",
                            onClick = {
                                Toast.makeText(context, "Buy Silver...", Toast.LENGTH_SHORT).show()
                            }
                        )
                    }

                    Spacer(modifier = Modifier.height(14.dp))
                    Divider(color = PhonePeBorderGray, thickness = 0.5.dp)
                    Spacer(modifier = Modifier.height(12.dp))

                    // Platinum Banner Row
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable {
                                Toast.makeText(context, "Save in pure Platinum...", Toast.LENGTH_SHORT).show()
                            },
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(
                                imageVector = Icons.Default.CurrencyExchange,
                                contentDescription = null,
                                tint = Color(0xFF00796B),
                                modifier = Modifier.size(20.dp)
                            )
                            Spacer(modifier = Modifier.width(10.dp))
                            Text(
                                text = "Save in pure Platinum daily",
                                fontSize = 12.sp,
                                fontWeight = FontWeight.SemiBold,
                                color = PhonePeTextDark
                            )
                        }
                        
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text(
                                text = "More",
                                color = PhonePePurple,
                                fontSize = 12.sp,
                                fontWeight = FontWeight.Bold
                            )
                            Icon(
                                imageVector = Icons.Default.KeyboardArrowRight,
                                contentDescription = null,
                                tint = PhonePePurple,
                                modifier = Modifier.size(16.dp)
                            )
                        }
                    }
                }
            }
        }

        // 8. Section: Insurance
        item {
            Card(
                colors = CardDefaults.cardColors(containerColor = Color.White),
                shape = RoundedCornerShape(12.dp),
                elevation = CardDefaults.cardElevation(1.dp),
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 12.dp)
                    .padding(bottom = 12.dp)
            ) {
                Column(modifier = Modifier.padding(14.dp)) {
                    Text(
                        text = "Insurance",
                        fontWeight = FontWeight.Bold,
                        color = PhonePeTextDark,
                        fontSize = 14.sp
                    )
                    Spacer(modifier = Modifier.height(14.dp))
                    
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        BillButton(
                            icon = Icons.Default.TwoWheeler,
                            label = "Bike\nInsurance",
                            onClick = {
                                Toast.makeText(context, "Bike Insurance...", Toast.LENGTH_SHORT).show()
                            }
                        )
                        BillButton(
                            icon = Icons.Default.DirectionsCar,
                            label = "Car\nInsurance",
                            onClick = {
                                Toast.makeText(context, "Car Insurance...", Toast.LENGTH_SHORT).show()
                            }
                        )
                        BillButton(
                            icon = Icons.Default.MedicalServices,
                            label = "Health\nInsurance",
                            onClick = {
                                Toast.makeText(context, "Health Insurance...", Toast.LENGTH_SHORT).show()
                            }
                        )
                        BillButton(
                            icon = Icons.Default.Shield,
                            label = "LIC/Life\nInsurance",
                            onClick = {
                                Toast.makeText(context, "LIC/Life Insurance...", Toast.LENGTH_SHORT).show()
                            }
                        )
                    }

                    Spacer(modifier = Modifier.height(14.dp))
                    Divider(color = PhonePeBorderGray, thickness = 0.5.dp)
                    Spacer(modifier = Modifier.height(12.dp))

                    // Accident Cover Banner Row
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clickable {
                                Toast.makeText(context, "Get ₹20L Accident Cover...", Toast.LENGTH_SHORT).show()
                            },
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(
                                imageVector = Icons.Default.HealthAndSafety,
                                contentDescription = null,
                                tint = Color(0xFFE040FB),
                                modifier = Modifier.size(20.dp)
                            )
                            Spacer(modifier = Modifier.width(10.dp))
                            Text(
                                text = "Get ₹20L* Accident Cover",
                                fontSize = 12.sp,
                                fontWeight = FontWeight.SemiBold,
                                color = PhonePeTextDark
                            )
                        }
                        
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text(
                                text = "More",
                                color = PhonePePurple,
                                fontSize = 12.sp,
                                fontWeight = FontWeight.Bold
                            )
                            Icon(
                                imageVector = Icons.Default.KeyboardArrowRight,
                                contentDescription = null,
                                tint = PhonePePurple,
                                modifier = Modifier.size(16.dp)
                            )
                        }
                    }
                }
            }
        }

        item {
            // My QR Button Section
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp)
                    .clickable { onNavigateToQr() },
                colors = CardDefaults.cardColors(containerColor = Color.White),
                shape = RoundedCornerShape(12.dp)
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Box(
                        modifier = Modifier
                            .size(40.dp)
                            .clip(CircleShape)
                            .background(PhonePeLightPurple),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            imageVector = Icons.Default.QrCode,
                            contentDescription = "My QR",
                            tint = PhonePePurple
                        )
                    }
                    Spacer(modifier = Modifier.width(16.dp))
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = "My QR Code",
                            fontWeight = FontWeight.Bold,
                            fontSize = 16.sp,
                            color = PhonePeTextDark
                        )
                        Text(
                            text = "Show QR to receive money",
                            fontSize = 12.sp,
                            color = PhonePeTextMuted
                        )
                    }
                    Icon(
                        imageVector = Icons.Default.ChevronRight,
                        contentDescription = "Go",
                        tint = PhonePeTextMuted
                    )
                }
            }
            Spacer(modifier = Modifier.height(24.dp))
        }
    }

    // Dialog warnings/pranks
    if (showDialogText != null && showDialogTitle != null) {
        AlertDialog(
            onDismissRequest = {
                showDialogText = null
                showDialogTitle = null
            },
            title = {
                Text(
                    text = showDialogTitle!!,
                    fontWeight = FontWeight.Bold,
                    color = PhonePePurple
                )
            },
            text = {
                Text(text = showDialogText!!, fontSize = 14.sp)
            },
            confirmButton = {
                Button(
                    onClick = {
                        showDialogText = null
                        showDialogTitle = null
                    },
                    colors = ButtonDefaults.buttonColors(containerColor = PhonePePurple)
                ) {
                    Text("Paid successfully! ✅", color = Color.White)
                }
            }
        )
    }

    if (showRechargeReminder) {
        RechargeReminderDialog(
            phoneNumber = "887596642",
            onDismiss = {
                showRechargeReminder = false
                viewModel.hasShownRechargeReminder = true
            },
            onRecharge = {
                showRechargeReminder = false
                viewModel.hasShownRechargeReminder = true
                onNavigateToMobileRecharge()
            }
        )
    }
}

@Composable
fun TransferButton(
    iconContent: @Composable () -> Unit,
    label: String,
    onClick: () -> Unit
) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = Modifier
            .width(85.dp)
            .clickable { onClick() }
    ) {
        iconContent()
        Spacer(modifier = Modifier.height(8.dp))
        Text(
            text = label,
            fontSize = 11.5.sp,
            color = PhonePeTextDark,
            textAlign = TextAlign.Center,
            lineHeight = 15.sp,
            fontWeight = FontWeight.Medium
        )
    }
}

@Composable
fun ToMobileIcon() {
    Box(
        modifier = Modifier.size(60.dp)
    ) {
        Box(
            modifier = Modifier
                .size(56.dp)
                .clip(CircleShape)
                .background(PhonePePurple)
                .align(Alignment.Center),
            contentAlignment = Alignment.Center
        ) {
            Box(
                modifier = Modifier
                    .size(26.dp, 36.dp)
                    .border(2.dp, Color.White, RoundedCornerShape(6.dp))
                    .clip(RoundedCornerShape(6.dp)),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.Default.Person,
                    contentDescription = null,
                    tint = Color.White,
                    modifier = Modifier.size(16.dp).offset(y = (-4).dp)
                )
                Icon(
                    imageVector = Icons.Default.Phone,
                    contentDescription = null,
                    tint = Color.White,
                    modifier = Modifier.size(12.dp).offset(y = 6.dp)
                )
            }
        }
        // Green badge
        Box(
            modifier = Modifier
                .size(14.dp)
                .align(Alignment.TopEnd)
                .offset(x = (-2).dp, y = 2.dp)
                .background(PhonePeSuccessGreen, CircleShape)
                .border(2.dp, Color.White, CircleShape)
        )
    }
}

@Composable
fun ToBankIcon() {
    Box(modifier = Modifier.size(60.dp), contentAlignment = Alignment.Center) {
        Box(
            modifier = Modifier
                .size(56.dp)
                .clip(CircleShape)
                .background(PhonePePurple),
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = Icons.Default.AccountBalance,
                contentDescription = null,
                tint = Color.White,
                modifier = Modifier.size(32.dp)
            )
        }
    }
}

@Composable
fun PhonePeWalletIcon() {
    Box(modifier = Modifier.size(60.dp)) {
        Box(
            modifier = Modifier
                .size(56.dp)
                .clip(CircleShape)
                .background(PhonePePurple)
                .align(Alignment.Center),
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = Icons.Default.AccountBalanceWallet,
                contentDescription = null,
                tint = Color.White,
                modifier = Modifier.size(32.dp).offset(x = (-2).dp, y = 2.dp)
            )
            Text("₹", color = PhonePePurple, fontSize = 14.sp, fontWeight = FontWeight.Bold, modifier = Modifier.offset(x = 1.dp, y = 2.dp))
        }
        // Badge
        Box(
            modifier = Modifier
                .align(Alignment.TopCenter)
                .background(Color(0xFFD32F2F), RoundedCornerShape(4.dp))
                .padding(horizontal = 4.dp, vertical = 2.dp)
        ) {
            Text("2% back", color = Color.White, fontSize = 9.sp, fontWeight = FontWeight.Bold)
        }
    }
}

@Composable
fun CheckBalanceIcon() {
    Box(modifier = Modifier.size(60.dp), contentAlignment = Alignment.Center) {
        Box(
            modifier = Modifier
                .size(56.dp)
                .clip(CircleShape)
                .background(PhonePePurple),
            contentAlignment = Alignment.Center
        ) {
            Box(
                modifier = Modifier
                    .size(24.dp, 32.dp)
                    .background(Color.White, RoundedCornerShape(4.dp)),
                contentAlignment = Alignment.Center
            ) {
                Text("₹", color = PhonePePurple, fontSize = 16.sp, fontWeight = FontWeight.Bold)
            }
        }
    }
}

@Composable
fun BillButton(
    icon: ImageVector,
    label: String,
    onClick: () -> Unit
) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = Modifier
            .width(80.dp)
            .clickable { onClick() }
    ) {
        Box(
            modifier = Modifier
                .size(44.dp)
                .clip(RoundedCornerShape(12.dp))
                .border(1.dp, PhonePeBorderGray, RoundedCornerShape(12.dp))
                .background(Color.White),
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = icon,
                contentDescription = null,
                tint = PhonePePurple,
                modifier = Modifier.size(22.dp)
            )
        }

@Composable
fun PrankItemRow(
    tx: PrankTransaction,
    onClick: () -> Unit
) {
    val context = LocalContext.current
    val sdf = remember { SimpleDateFormat("dd MMM yyyy, hh:mm a", Locale.getDefault()) }
    val dateStr = remember(tx.timestamp) { sdf.format(Date(tx.timestamp)) }
    
    // Initials of the payee
    val initials = remember(tx.receiverName) {
        tx.receiverName.split(" ")
            .filter { it.isNotBlank() }
            .take(2)
            .joinToString("") { it.take(1).uppercase() }
            .ifBlank { "P" }
    }

    Card(
        colors = CardDefaults.cardColors(containerColor = Color.White),
        shape = RoundedCornerShape(10.dp),
        elevation = CardDefaults.cardElevation(1.dp),
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 12.dp, vertical = 4.dp)
            .clickable { onClick() }
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(12.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier.weight(1f)
            ) {
                // Circle with payee initials
                Box(
                    modifier = Modifier
                        .size(40.dp)
                        .clip(CircleShape)
                        .background(PhonePeLightPurple),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = initials,
                        color = PhonePePurple,
                        fontWeight = FontWeight.Bold,
                        fontSize = 15.sp
                    )
                }

                Spacer(modifier = Modifier.width(12.dp))

                Column {
                    Text(
                        text = tx.receiverName,
                        fontWeight = FontWeight.Bold,
                        color = PhonePeTextDark,
                        fontSize = 14.sp,
                        maxLines = 2,
                        overflow = TextOverflow.Ellipsis
                    )
                    Spacer(modifier = Modifier.height(2.dp))
                    Text(
                        text = dateStr,
                        fontSize = 11.sp,
                        color = PhonePeTextMuted
                    )
                }
            }

            Column(horizontalAlignment = Alignment.End) {
                Text(
                    text = "₹${String.format(Locale.US, "%,.2f", tx.amount)}",
                    fontWeight = FontWeight.ExtraBold,
                    color = PhonePeTextDark,
                    fontSize = 15.sp
                )
                Spacer(modifier = Modifier.height(2.dp))
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Box(
                        modifier = Modifier
                            .size(6.dp)
                            .clip(CircleShape)
                            .background(
                                if (tx.status == "SUCCESS") PhonePeSuccessGreen else PhonePeFailedRed
                            )
                    )
                    Spacer(modifier = Modifier.width(4.dp))
                    Text(
                        text = if (tx.status == "SUCCESS") "Successful" else "Failed",
                        color = if (tx.status == "SUCCESS") PhonePeSuccessGreen else PhonePeFailedRed,
                        fontSize = 11.sp,
                        fontWeight = FontWeight.Bold
                    )
                }
            }
        }
    
    

}}}}
