import re

with open('app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt', 'r') as f:
    content = f.read()

new_success_screen = """@OptIn(ExperimentalFoundationApi::class)
@Composable
fun SuccessScreen(accountId: String?, viewModel: PrankViewModel, onBack: () -> Unit) {
    val bankAccounts by viewModel.bankAccounts.collectAsState()
    val account = bankAccounts.find { it.id == accountId }
    androidx.activity.compose.BackHandler { onBack() }
    
    var isEditing by remember { mutableStateOf(false) }
    var editedBalance by remember { mutableStateOf(account?.balance?.toString() ?: "1297.0") }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.White)
    ) {
        // Main Content Area
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f)
                .verticalScroll(rememberScrollState()),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Spacer(modifier = Modifier.height(48.dp))
            
            // Green Check Circle
            Box(
                modifier = Modifier
                    .size(52.dp)
                    .background(Color(0xFF4CAF50), CircleShape),
                contentAlignment = Alignment.Center
            ) {
                Icon(Icons.Default.Check, contentDescription = "Success", tint = Color.White, modifier = Modifier.size(32.dp))
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            
            // Balance check successful text
            Text(
                text = "Balance check successful",
                fontSize = 22.sp,
                color = Color(0xFF333333),
                fontWeight = FontWeight.SemiBold
            )
            
            Spacer(modifier = Modifier.height(32.dp))
            
            // Bank Info
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.Center,
                modifier = Modifier.fillMaxWidth()
            ) {
                if (account != null) {
                    com.example.ui.components.BankLogo(bankName = account.bankName, size = 24.dp)
                } else {
                    Box(modifier = Modifier.size(24.dp).background(Color.LightGray, CircleShape))
                }
                Spacer(modifier = Modifier.width(8.dp))
                Text(
                    text = account?.bankDesc ?: "Union Bank Of India - 0365",
                    fontSize = 16.sp,
                    color = Color(0xFF555555)
                )
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            
            // Available Balance Label
            Text(
                text = "Available Balance",
                fontSize = 14.sp,
                color = Color.Gray
            )
            
            Spacer(modifier = Modifier.height(8.dp))
            
            // Balance Amount
            if (isEditing) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("₹", fontSize = 32.sp, fontWeight = FontWeight.Bold, color = Color.Black)
                    Spacer(modifier = Modifier.width(4.dp))
                    OutlinedTextField(
                        value = editedBalance,
                        onValueChange = { editedBalance = it },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        modifier = Modifier.width(180.dp),
                        textStyle = androidx.compose.ui.text.TextStyle(fontSize = 32.sp, fontWeight = FontWeight.Bold),
                        singleLine = true
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Button(
                        onClick = { 
                            isEditing = false
                            val newBal = editedBalance.toDoubleOrNull() ?: 1297.0
                            account?.let { viewModel.updateBankAccount(it.copy(balance = newBal)) }
                        },
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF5f259f))
                    ) {
                        Text("Save")
                    }
                }
            } else {
                val displayBalance = account?.balance?.let { if (it % 1.0 == 0.0) it.toInt().toString() else String.format("%.2f", it) } ?: "589.53"
                Text(
                    text = "₹$displayBalance",
                    fontSize = 42.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color(0xFF222222),
                    modifier = Modifier.combinedClickable(
                        onClick = {},
                        onLongClick = { isEditing = true }
                    )
                )
            }
            
            Spacer(modifier = Modifier.height(48.dp))
            
            // BRAND IN FOCUS divider
            Row(
                modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                HorizontalDivider(modifier = Modifier.weight(1f), color = Color(0xFFEEEEEE))
                Text(
                    text = "BRAND IN FOCUS",
                    fontSize = 12.sp,
                    color = Color.Gray,
                    letterSpacing = 1.sp,
                    modifier = Modifier.padding(horizontal = 12.dp)
                )
                HorizontalDivider(modifier = Modifier.weight(1f), color = Color(0xFFEEEEEE))
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            
            // Brand icons
            Row(
                modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                BrandIcon("Story TV", Color(0xFF8A2BE2))
                BrandIcon("Best Dramas", Color(0xFF9370DB))
                BrandIcon("Top Shows", Color(0xFF9370DB))
                BrandIcon("Hit Movies", Color(0xFF9370DB))
            }
            
            Spacer(modifier = Modifier.height(32.dp))
            
            // Ad Banner
            Card(
                modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp),
                shape = RoundedCornerShape(12.dp),
                colors = CardDefaults.cardColors(containerColor = Color(0xFFF9F9F9)),
                border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFEEEEEE)),
                elevation = CardDefaults.cardElevation(0.dp)
            ) {
                Row(
                    modifier = Modifier.padding(16.dp).fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Box(
                        modifier = Modifier.size(32.dp).background(Color(0xFFFFE4E1), RoundedCornerShape(8.dp)),
                        contentAlignment = Alignment.Center
                    ) {
                        Text("₹10", color = Color(0xFFE91E63), fontSize = 12.sp, fontWeight = FontWeight.Bold)
                    }
                    Spacer(modifier = Modifier.width(16.dp))
                    Text(
                        text = "Daily Mutual Funds SIP @ ₹10",
                        fontSize = 14.sp,
                        color = Color(0xFF333333),
                        fontWeight = FontWeight.Medium
                    )
                }
            }
            
            Spacer(modifier = Modifier.height(32.dp))
        }
        
        // Done Button at bottom
        Button(
            onClick = onBack,
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 24.dp, vertical = 24.dp)
                .height(52.dp),
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFF5F5F5)),
            shape = RoundedCornerShape(26.dp),
            elevation = ButtonDefaults.buttonElevation(0.dp)
        ) {
            Text("DONE", color = Color(0xFF5f259f), fontSize = 16.sp, fontWeight = FontWeight.Bold, letterSpacing = 0.5.sp)
        }
    }
}

@Composable
fun BrandIcon(label: String, color: Color) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Box(
            modifier = Modifier.size(56.dp).background(color, RoundedCornerShape(16.dp)),
            contentAlignment = Alignment.Center
        ) {
            Icon(Icons.Default.PlayArrow, contentDescription = label, tint = Color.White, modifier = Modifier.size(28.dp))
        }
        Spacer(modifier = Modifier.height(8.dp))
        Text(label, fontSize = 12.sp, color = Color.Gray, textAlign = TextAlign.Center)
    }
}
"""

content = re.sub(r'@OptIn\(ExperimentalFoundationApi::class\)\n@Composable\nfun SuccessScreen\(accountId: String\?, viewModel: PrankViewModel, onBack: \(\) -> Unit\).*', new_success_screen, content, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt', 'w') as f:
    f.write(content)
