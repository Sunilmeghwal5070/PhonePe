package com.example.ui.screens

import android.content.Intent
import android.speech.tts.TextToSpeech
import android.widget.Toast
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.*
import androidx.compose.animation.expandVertically
import androidx.compose.animation.fadeIn
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.ArrowForward
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.rotate
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.ui.PrankViewModel
import com.example.ui.theme.*
import java.text.DecimalFormat
import java.text.SimpleDateFormat
import java.util.*
import kotlinx.coroutines.delay

enum class PaymentState {
    PROCESSING,
    SUCCESS_ANIMATION,
    RECEIPT_DETAILS
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ReceiptScreen(
    transactionId: Int,
    skipAnimation: Boolean = false,
    viewModel: PrankViewModel,
    onDone: () -> Unit,
    onNavigateToCheckBalance: () -> Unit = {}
) {
    val context = LocalContext.current
    val clipboardManager = LocalClipboardManager.current
    
    // Select transaction and listen to state
    LaunchedEffect(transactionId) {
        viewModel.selectTransactionById(transactionId)
    }
    
    val tx by viewModel.selectedTransaction.collectAsState()
    val userProfile by viewModel.userProfileManager.userProfile.collectAsState()
    
    // For History clicks, we can skip animation if it's old.
    // If it's a new transaction just created, it should play the animation.
    var paymentState by remember { mutableStateOf(PaymentState.PROCESSING) }
    var detailsExpanded by remember { mutableStateOf(true) }
    
    // Speech Synthesis (TTS) - PhonePe Smart Speaker Voice!
    var tts by remember { mutableStateOf<TextToSpeech?>(null) }
    
    // Initialize TTS on start
    DisposableEffect(context) {
        tts = TextToSpeech(context) { status ->
            if (status == TextToSpeech.SUCCESS) {
                tts?.language = Locale("hi", "IN")
            }
        }
        onDispose {
            tts?.stop()
            tts?.shutdown()
        }
    }

    LaunchedEffect(tx) {
        val currentTx = tx
        if (currentTx != null) {
            val isOldTx = skipAnimation || (System.currentTimeMillis() - currentTx.timestamp) > 60000 // 1 minute
            if (isOldTx) {
                paymentState = PaymentState.RECEIPT_DETAILS
            } else {
                paymentState = PaymentState.PROCESSING
                delay(1800) // Processing delay
                if (currentTx.status == "SUCCESS") {
                    paymentState = PaymentState.SUCCESS_ANIMATION
                    delay(2600) // Success screen celebration delay
                }
                paymentState = PaymentState.RECEIPT_DETAILS
            }
        }
    }

    LaunchedEffect(paymentState, tx) {
        val currentTx = tx
        if (paymentState == PaymentState.SUCCESS_ANIMATION && currentTx != null && currentTx.status == "SUCCESS") {
            val amountInt = currentTx.amount.toInt()
            val textToSpeak = "Received $amountInt rupees on PhonePe"
            tts?.speak(textToSpeak, TextToSpeech.QUEUE_FLUSH, null, "PhonePePrankTts")
        }
    }

    if (tx == null) {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            CircularProgressIndicator(color = PhonePePurple)
        }
        return
    }

    val currentTx = tx!!
    val decimalFormat = DecimalFormat("#,##,###.00")
    
    val sdf = SimpleDateFormat("hh:mm a 'on' dd MMM yyyy", Locale.getDefault())
    val formattedDate = sdf.format(Date(currentTx.timestamp))

    fun copyText(text: String, label: String) {
        clipboardManager.setText(AnnotatedString(text))
        Toast.makeText(context, "$label Copied!", Toast.LENGTH_SHORT).show()
    }

    fun shareTransaction() {
        val shareMsg = """
            *PhonePe Transaction Receipt*
            ----------------------------------
            Status: ${currentTx.status}
            Received From: ${currentTx.receiverName}
            Phone: ${currentTx.receiverPhone}
            Amount: ₹${currentTx.amount.toInt()}
            Date: $formattedDate
            Txn ID: ${currentTx.transactionId}
            UTR: ${currentTx.utr}
            ----------------------------------
            Shared via PhonePe
        """.trimIndent()
        
        val intent = Intent(Intent.ACTION_SEND).apply {
            type = "text/plain"
            putExtra(Intent.EXTRA_TEXT, shareMsg)
        }
        context.startActivity(Intent.createChooser(intent, "Share Receipt Via"))
    }

    if (paymentState == PaymentState.RECEIPT_DETAILS && currentTx.type == "RECHARGE") {
        RechargeSuccessScreen(transactionId = transactionId, viewModel = viewModel, onDone = onDone)
        return
    }

    when (paymentState) {
        PaymentState.PROCESSING -> {
            ProcessingScreen(
                amount = currentTx.amount,
                receiverName = currentTx.receiverName,
                receiverPhone = currentTx.receiverPhone,
                receiverUpiId = currentTx.receiverUpiId,
                onSkip = { paymentState = PaymentState.RECEIPT_DETAILS }
            )
        }
        PaymentState.SUCCESS_ANIMATION -> {
            SuccessAnimationScreen(
                amount = currentTx.amount,
                receiverName = currentTx.receiverName,
                onSkip = { paymentState = PaymentState.RECEIPT_DETAILS }
            )
        }
        PaymentState.RECEIPT_DETAILS -> {
            Scaffold(
                containerColor = Color(0xFFF2F2F2),
                topBar = {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .background(Color(0xFF168039))
                            .padding(top = 16.dp, bottom = 12.dp, start = 8.dp, end = 16.dp)
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            IconButton(onClick = onDone) {
                                Icon(
                                    imageVector = Icons.Default.ArrowBack,
                                    contentDescription = "Back",
                                    tint = Color.White
                                )
                            }
                            Spacer(modifier = Modifier.width(4.dp))
                            Column {
                                Text(
                                    text = "Transaction Successful",
                                    color = Color.White,
                                    fontSize = 18.sp,
                                    fontWeight = FontWeight.Bold
                                )
                                Text(
                                    text = formattedDate,
                                    color = Color.White.copy(alpha = 0.9f),
                                    fontSize = 13.sp
                                )
                            }
                        }
                    }
                }
            ) { paddingValues ->
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(paddingValues)
                        .verticalScroll(rememberScrollState())
                ) {
                    Spacer(modifier = Modifier.height(16.dp))
                    // Main Receipt Card
                    Card(
                        colors = CardDefaults.cardColors(containerColor = Color.White),
                        shape = RoundedCornerShape(12.dp),
                        modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp)
                    ) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            Text(if (currentTx.type == "PAID") "Paid to" else "Received from", fontWeight = FontWeight.Bold, fontSize = 16.sp, color = Color.Black)
                            Spacer(modifier = Modifier.height(16.dp))
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.Top
                            ) {
                                Row(modifier = Modifier.weight(1f)) {
                                    Box(
                                        modifier = Modifier
                                            .size(44.dp)
                                            .background(Color(0xFF5f259f), RoundedCornerShape(12.dp)),
                                        contentAlignment = Alignment.Center
                                    ) {
                                        Icon(
                                            imageVector = Icons.AutoMirrored.Filled.ArrowForward,
                                            contentDescription = null,
                                            tint = Color.White,
                                            modifier = Modifier.size(20.dp).rotate(if (currentTx.type == "PAID") -45f else 135f)
                                        )
                                    }
                                    Spacer(modifier = Modifier.width(12.dp))
                                    Column {
                                        Text(
                                            text = currentTx.receiverName.uppercase(),
                                            fontSize = 15.sp,
                                            color = Color.DarkGray,
                                            lineHeight = 20.sp
                                        )
                                        val phoneStr = if (currentTx.receiverPhone.length >= 4) "XXXXXXX${currentTx.receiverPhone.takeLast(4)}" else "XXXXXXX9749"
                                        Text(
                                            text = phoneStr,
                                            fontSize = 14.sp,
                                            color = Color.Gray
                                        )
                                    }
                                }
                                Text(
                                    text = "₹${currentTx.amount.toInt()}",
                                    fontWeight = FontWeight.Bold,
                                    fontSize = 20.sp,
                                    color = Color.Black
                                )
                            }
                            
                            Spacer(modifier = Modifier.height(16.dp))
                            
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Text(text = "Banking Name", fontSize = 13.sp, color = Color.Gray)
                                Text(text = "  :  ", fontSize = 13.sp, color = Color.Gray)
                                Text(text = currentTx.receiverName, fontSize = 13.sp, color = Color.Gray)
                                Spacer(modifier = Modifier.width(4.dp))
                                Icon(Icons.Default.VerifiedUser, tint = Color(0xFF168039), modifier = Modifier.size(12.dp), contentDescription = null)
                            }
                            
                            Spacer(modifier = Modifier.height(16.dp))
                            
                            // Transfer details
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .clickable { detailsExpanded = !detailsExpanded }
                                    .padding(vertical = 12.dp),
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.SpaceBetween
                            ) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Icon(Icons.Default.ListAlt, contentDescription = null, tint = Color.DarkGray)
                                    Spacer(modifier = Modifier.width(12.dp))
                                    Text("Transfer Details", fontSize = 15.sp, color = Color.Black)
                                }
                                Icon(if (detailsExpanded) Icons.Default.KeyboardArrowUp else Icons.Default.KeyboardArrowDown, contentDescription = null, tint = Color.Black)
                            }
                            
                            if (detailsExpanded) {
                                Column(modifier = Modifier.padding(start = 36.dp)) {
                                    Text("PhonePe Transaction ID", fontSize = 12.sp, color = Color.Gray)
                                    Row(verticalAlignment = Alignment.CenterVertically) {
                                        Text(currentTx.transactionId, fontSize = 14.sp, color = Color.DarkGray)
                                        Spacer(modifier = Modifier.weight(1f))
                                        IconButton(onClick = { copyText(currentTx.transactionId, "Txn ID") }, modifier = Modifier.size(32.dp)) {
                                            Icon(Icons.Default.ContentCopy, contentDescription = null, tint = PhonePePurple, modifier = Modifier.size(18.dp))
                                        }
                                    }
                                    Spacer(modifier = Modifier.height(12.dp))
                                    Text(if (currentTx.type == "PAID") "Debited from" else "Credited to", fontSize = 12.sp, color = Color.Gray)
                                    Spacer(modifier = Modifier.height(6.dp))
                                    Row(verticalAlignment = Alignment.CenterVertically) {
                                        Box(
                                            modifier = Modifier
                                                .size(32.dp)
                                                .border(1.dp, Color(0xFFEEEEEE), RoundedCornerShape(8.dp)),
                                            contentAlignment = Alignment.Center
                                        ) {
                                            Text(if (currentTx.type == "PAID") currentTx.senderBankName.take(1).uppercase() else currentTx.receiverName.take(1).uppercase(), color = Color(0xFFe31837), fontWeight = FontWeight.Bold, fontSize = 18.sp)
                                        }
                                        Spacer(modifier = Modifier.width(12.dp))
                                        Text(if (currentTx.type == "PAID") userProfile.name else currentTx.receiverName, fontSize = 15.sp, color = Color.DarkGray)
                                        Spacer(modifier = Modifier.weight(1f))
                                        Text("₹${currentTx.amount.toInt()}", fontSize = 15.sp, color = Color.DarkGray)
                                    }
                                    Spacer(modifier = Modifier.height(6.dp))
                                    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(start = 44.dp)) {
                                        Text("UTR: ${currentTx.utr}", fontSize = 14.sp, color = Color.Gray)
                                        Spacer(modifier = Modifier.weight(1f))
                                        IconButton(onClick = { copyText(currentTx.utr, "UTR") }, modifier = Modifier.size(32.dp)) {
                                            Icon(Icons.Default.ContentCopy, contentDescription = null, tint = PhonePePurple, modifier = Modifier.size(18.dp))
                                        }
                                    }
                                }
                            }
                            
                            Spacer(modifier = Modifier.height(24.dp))
                            
                            // Action buttons
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceAround
                            ) {
                                ReceiptActionButton(icon = Icons.Default.CallMade, label = "Send\nMoney", onClick = { onDone() })
                                ReceiptActionButton(icon = Icons.Default.AccountBalance, label = "Check\nBalance", onClick = { onNavigateToCheckBalance() })
                                ReceiptActionButton(icon = Icons.Default.Schedule, label = "View\nHistory", onClick = { onDone() })
                                ReceiptActionButton(icon = Icons.Default.Share, label = "Share\nReceipt", onClick = { shareTransaction() })
                            }
                        }
                    }
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    // Support Card
                    Card(
                        colors = CardDefaults.cardColors(containerColor = Color.White),
                        shape = RoundedCornerShape(12.dp),
                        modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp).clickable { }
                    ) {
                        Row(
                            modifier = Modifier.fillMaxWidth().padding(16.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Icon(Icons.Default.HelpOutline, contentDescription = null, tint = Color.DarkGray, modifier = Modifier.size(20.dp))
                            Spacer(modifier = Modifier.width(12.dp))
                            Text("Contact PhonePe Support", fontSize = 15.sp, color = Color.DarkGray)
                            Spacer(modifier = Modifier.weight(1f))
                            Icon(Icons.Default.KeyboardArrowRight, contentDescription = null, tint = Color.Gray)
                        }
                    }
                    
                    Spacer(modifier = Modifier.height(32.dp))
                    
                    // Footer
                    Column(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Text("Powered by", fontSize = 12.sp, color = Color.Gray)
                        Spacer(modifier = Modifier.height(4.dp))
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            coil.compose.AsyncImage(
                            model = coil.request.ImageRequest.Builder(androidx.compose.ui.platform.LocalContext.current)
                                .data("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/UPI-Logo-vector.svg/1024px-UPI-Logo-vector.svg.png")
                                .crossfade(true)
                                .build(),
                            contentDescription = "UPI",
                            modifier = Modifier.height(20.dp),
                            contentScale = androidx.compose.ui.layout.ContentScale.Fit
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("|", color = Color(0xFF666666))
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
                    
                    Spacer(modifier = Modifier.height(32.dp))
                }
            }
        }
    }
}

@Composable
fun ReceiptActionButton(icon: ImageVector, label: String, onClick: () -> Unit) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = Modifier.clickable { onClick() }
    ) {
        Box(
            modifier = Modifier
                .size(48.dp)
                .background(PhonePeLightPurple, CircleShape),
            contentAlignment = Alignment.Center
        ) {
            Icon(icon, contentDescription = null, tint = PhonePePurple)
        }
        Spacer(modifier = Modifier.height(8.dp))
        Text(label, fontSize = 12.sp, color = Color.DarkGray, textAlign = TextAlign.Center, lineHeight = 16.sp)
    }
}

@Composable
fun ProcessingScreen(
    amount: Double,
    receiverName: String,
    receiverPhone: String,
    receiverUpiId: String,
    onSkip: () -> Unit
) {
    val context = LocalContext.current
    val initials = remember(receiverName) {
        receiverName.split(" ")
            .filter { it.isNotBlank() }
            .take(2)
            .joinToString("") { it.take(1).uppercase() }
            .ifBlank { "P" }
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.White)
    ) {
        // Skip Button in top right
        TextButton(
            onClick = onSkip,
            modifier = Modifier
                .align(Alignment.TopEnd)
                .padding(16.dp)
        ) {
            Text("Skip", color = PhonePePurple, fontWeight = FontWeight.Bold, fontSize = 14.sp)
        }

        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.SpaceBetween
        ) {
            Spacer(modifier = Modifier.height(48.dp))

            Column(
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                // Payee Initials Circle
                Box(
                    modifier = Modifier
                        .size(80.dp)
                        .clip(CircleShape)
                        .background(PhonePeLightPurple),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = initials,
                        color = PhonePePurple,
                        fontWeight = FontWeight.Bold,
                        fontSize = 28.sp
                    )
                }

                Spacer(modifier = Modifier.height(8.dp))

                Text(
                    text = "Paying ₹${amount.toInt()}",
                    fontSize = 24.sp,
                    fontWeight = FontWeight.Bold,
                    color = PhonePeTextDark
                )

                Text(
                    text = "To: $receiverName",
                    fontSize = 18.sp,
                    fontWeight = FontWeight.SemiBold,
                    color = PhonePeTextDark
                )

                if (receiverPhone.isNotBlank()) {
                    Text(
                        text = "+91 $receiverPhone",
                        fontSize = 14.sp,
                        color = PhonePeTextMuted
                    )
                } else if (receiverUpiId.isNotBlank()) {
                    Text(
                        text = receiverUpiId,
                        fontSize = 14.sp,
                        color = PhonePeTextMuted
                    )
                }

                Spacer(modifier = Modifier.height(32.dp))

                // Custom Spinning Arc Loader
                val infiniteTransition = rememberInfiniteTransition(label = "rotation")
                val rotationAngle by infiniteTransition.animateFloat(
                    initialValue = 0f,
                    targetValue = 360f,
                    animationSpec = infiniteRepeatable(
                        animation = tween(1200, easing = LinearEasing),
                        repeatMode = RepeatMode.Restart
                    ),
                    label = "rotationAngle"
                )

                Box(modifier = Modifier.size(52.dp), contentAlignment = Alignment.Center) {
                    Canvas(
                        modifier = Modifier
                            .fillMaxSize()
                            .rotate(rotationAngle)
                    ) {
                        drawArc(
                            color = PhonePePurple,
                            startAngle = 0f,
                            sweepAngle = 280f,
                            useCenter = false,
                            style = Stroke(width = 4.dp.toPx(), cap = StrokeCap.Round)
                        )
                    }
                }
            }

            // Bottom security check info
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.Center,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(bottom = 24.dp)
            ) {
                Icon(
                    imageVector = Icons.Default.Lock,
                    contentDescription = "Secure",
                    tint = PhonePeSuccessGreen,
                    modifier = Modifier.size(16.dp)
                )
                Spacer(modifier = Modifier.width(6.dp))
                Text(
                    text = "Connecting securely",
                    fontSize = 13.sp,
                    color = PhonePeTextMuted,
                    fontWeight = FontWeight.Medium
                )
            }
        }
    }
}

@Composable
fun SuccessAnimationScreen(
    amount: Double,
    receiverName: String,
    onSkip: () -> Unit
) {
    val infiniteTransition = rememberInfiniteTransition(label = "ripple")
    
    // Wave ripple animations radiating outwards
    val scale1 by infiniteTransition.animateFloat(
        initialValue = 1f,
        targetValue = 2.8f,
        animationSpec = infiniteRepeatable(
            animation = tween(1800, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "scale1"
    )
    val alpha1 by infiniteTransition.animateFloat(
        initialValue = 0.5f,
        targetValue = 0f,
        animationSpec = infiniteRepeatable(
            animation = tween(1800, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "alpha1"
    )

    val scale2 by infiniteTransition.animateFloat(
        initialValue = 1f,
        targetValue = 2.8f,
        animationSpec = infiniteRepeatable(
            animation = tween(1800, delayMillis = 600, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "scale2"
    )
    val alpha2 by infiniteTransition.animateFloat(
        initialValue = 0.5f,
        targetValue = 0f,
        animationSpec = infiniteRepeatable(
            animation = tween(1800, delayMillis = 600, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "alpha2"
    )

    val scale3 by infiniteTransition.animateFloat(
        initialValue = 1f,
        targetValue = 2.8f,
        animationSpec = infiniteRepeatable(
            animation = tween(1800, delayMillis = 1200, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "scale3"
    )
    val alpha3 by infiniteTransition.animateFloat(
        initialValue = 0.5f,
        targetValue = 0f,
        animationSpec = infiniteRepeatable(
            animation = tween(1800, delayMillis = 1200, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "alpha3"
    )

    // Bouncy pop animation for the checkmark
    var checkmarkSizeState by remember { mutableStateOf(0f) }
    val checkmarkScale by animateFloatAsState(
        targetValue = checkmarkSizeState,
        animationSpec = spring(
            dampingRatio = Spring.DampingRatioMediumBouncy,
            stiffness = Spring.StiffnessLow
        ),
        label = "checkmarkScale"
    )

    LaunchedEffect(Unit) {
        checkmarkSizeState = 1f
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(PhonePeSuccessGreen)
    ) {
        // Details Button in top right
        TextButton(
            onClick = onSkip,
            modifier = Modifier
                .align(Alignment.TopEnd)
                .padding(16.dp)
        ) {
            Text("Details", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 14.sp)
        }

        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            // Ripple layers surrounding center checkmark
            Box(
                contentAlignment = Alignment.Center,
                modifier = Modifier
                    .size(240.dp)
                    .padding(20.dp)
            ) {
                // Ripple Wave 1
                Box(
                    modifier = Modifier
                        .size(80.dp)
                        .scale(scale1)
                        .clip(CircleShape)
                        .background(Color.White.copy(alpha = alpha1))
                )
                // Ripple Wave 2
                Box(
                    modifier = Modifier
                        .size(80.dp)
                        .scale(scale2)
                        .clip(CircleShape)
                        .background(Color.White.copy(alpha = alpha2))
                )
                // Ripple Wave 3
                Box(
                    modifier = Modifier
                        .size(80.dp)
                        .scale(scale3)
                        .clip(CircleShape)
                        .background(Color.White.copy(alpha = alpha3))
                )

                // Central White Circle with Green Checkmark
                Box(
                    modifier = Modifier
                        .size(80.dp)
                        .scale(checkmarkScale)
                        .clip(CircleShape)
                        .background(Color.White),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = Icons.Default.Check,
                        contentDescription = "Success",
                        tint = PhonePeSuccessGreen,
                        modifier = Modifier.size(52.dp)
                    )
                }
            }

            Spacer(modifier = Modifier.height(32.dp))

            Text(
                text = "Payment Successful",
                color = Color.White,
                fontSize = 24.sp,
                fontWeight = FontWeight.Bold,
                textAlign = TextAlign.Center
            )

            Spacer(modifier = Modifier.height(16.dp))

            Text(
                text = "₹${amount.toInt()}",
                color = Color.White,
                fontSize = 38.sp,
                fontWeight = FontWeight.ExtraBold,
                textAlign = TextAlign.Center
            )

            Spacer(modifier = Modifier.height(8.dp))

            Text(
                text = "to $receiverName",
                color = Color.White.copy(alpha = 0.95f),
                fontSize = 18.sp,
                fontWeight = FontWeight.Medium,
                textAlign = TextAlign.Center
            )
        }
    }
}
