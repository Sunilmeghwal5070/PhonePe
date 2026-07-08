import re

with open('app/src/main/java/com/example/ui/screens/ReceiptScreen.kt', 'r') as f:
    content = f.read()

start_marker = "@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun ReceiptScreen("
end_marker = "@Composable\nfun ProcessingScreen("

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Markers not found")
    exit(1)

new_receipt_screen = """@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ReceiptScreen(
    transactionId: Int,
    viewModel: PrankViewModel,
    onDone: () -> Unit
) {
    val context = LocalContext.current
    val clipboardManager = LocalClipboardManager.current
    
    // Select transaction and listen to state
    LaunchedEffect(transactionId) {
        viewModel.selectTransactionById(transactionId)
    }
    
    val tx by viewModel.selectedTransaction.collectAsState()
    
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
            val isOldTx = (System.currentTimeMillis() - currentTx.timestamp) > 60000 // 1 minute
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
        val shareMsg = \"\"\"
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
        \"\"\".trimIndent()
        
        val intent = Intent(Intent.ACTION_SEND).apply {
            type = "text/plain"
            putExtra(Intent.EXTRA_TEXT, shareMsg)
        }
        context.startActivity(Intent.createChooser(intent, "Share Receipt Via"))
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
                                    imageVector = Icons.AutoMirrored.Filled.ArrowBack,
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
                            Text("Received from", fontWeight = FontWeight.Bold, fontSize = 16.sp, color = Color.Black)
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
                                            imageVector = Icons.AutoMirrored.Filled.ArrowBack, // Rotate to look like CallReceived
                                            contentDescription = null,
                                            tint = Color.White,
                                            modifier = Modifier.size(20.dp).rotate(-45f)
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
                                    Text("Credited to", fontSize = 12.sp, color = Color.Gray)
                                    Spacer(modifier = Modifier.height(6.dp))
                                    Row(verticalAlignment = Alignment.CenterVertically) {
                                        Box(
                                            modifier = Modifier
                                                .size(32.dp)
                                                .border(1.dp, Color(0xFFEEEEEE), RoundedCornerShape(8.dp)),
                                            contentAlignment = Alignment.Center
                                        ) {
                                            Text("S", color = Color(0xFFe31837), fontWeight = FontWeight.Bold, fontSize = 18.sp)
                                        }
                                        Spacer(modifier = Modifier.width(12.dp))
                                        Text("Sunil", fontSize = 15.sp, color = Color.DarkGray)
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
                                ReceiptActionButton(icon = Icons.AutoMirrored.Filled.CallMade, label = "Send\nMoney", onClick = { onDone() })
                                ReceiptActionButton(icon = Icons.Default.AccountBalance, label = "Check\nBalance", onClick = {})
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
                            Icon(Icons.AutoMirrored.Filled.HelpOutline, contentDescription = null, tint = Color.DarkGray, modifier = Modifier.size(20.dp))
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
                            Text("UPI", fontWeight = FontWeight.Bold, fontStyle = androidx.compose.ui.text.font.FontStyle.Italic, fontSize = 18.sp, color = Color(0xFF666666))
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("|", color = Color(0xFF666666))
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("ICICI Bank", fontWeight = FontWeight.Bold, fontStyle = androidx.compose.ui.text.font.FontStyle.Italic, fontSize = 16.sp, color = Color(0xFFB31217))
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

"""

new_content = content[:start_idx] + new_receipt_screen + content[end_idx:]

with open('app/src/main/java/com/example/ui/screens/ReceiptScreen.kt', 'w') as f:
    f.write(new_content)

print("ReceiptScreen updated")
