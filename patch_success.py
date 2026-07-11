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
            .background(Color(0xFFF9F9F9))
    ) {
        // Main Content Area
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f)
                .verticalScroll(rememberScrollState()),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Spacer(modifier = Modifier.height(72.dp))
            
            // Green Check Circle
            Box(
                modifier = Modifier
                    .size(48.dp)
                    .background(Color(0xFF4CAF50), CircleShape),
                contentAlignment = Alignment.Center
            ) {
                Icon(Icons.Default.Check, contentDescription = "Success", tint = Color.White, modifier = Modifier.size(32.dp))
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            
            // Balance check successful text
            Text(
                text = "Balance check successful",
                fontSize = 18.sp,
                color = Color(0xFF444444),
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
                    com.example.ui.components.BankLogo(bankName = account.bankName, size = 18.dp)
                } else {
                    Box(modifier = Modifier.size(18.dp).background(Color.LightGray, CircleShape))
                }
                Spacer(modifier = Modifier.width(8.dp))
                Text(
                    text = account?.bankDesc ?: "Union Bank Of India - 0365",
                    fontSize = 15.sp,
                    color = Color(0xFF555555)
                )
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            
            // Available Balance Label
            Text(
                text = "Available Balance",
                fontSize = 13.sp,
                color = Color.Gray
            )
            
            Spacer(modifier = Modifier.height(8.dp))
            
            // Balance Amount
            if (isEditing) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("₹", fontSize = 36.sp, fontWeight = FontWeight.Normal, color = Color.Black)
                    Spacer(modifier = Modifier.width(4.dp))
                    OutlinedTextField(
                        value = editedBalance,
                        onValueChange = { editedBalance = it },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        modifier = Modifier.width(180.dp),
                        textStyle = androidx.compose.ui.text.TextStyle(fontSize = 36.sp, fontWeight = FontWeight.Normal),
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
                    fontWeight = FontWeight.Medium,
                    color = Color(0xFF111111),
                    modifier = Modifier.combinedClickable(
                        onClick = {},
                        onLongClick = { isEditing = true }
                    )
                )
            }
            
            Spacer(modifier = Modifier.height(64.dp))
            
            // BRAND IN FOCUS divider
            Row(
                modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                HorizontalDivider(modifier = Modifier.weight(1f), color = Color(0xFFE0E0E0))
                Text(
                    text = "BRAND IN FOCUS",
                    fontSize = 11.sp,
                    color = Color.Gray,
                    letterSpacing = 1.sp,
                    modifier = Modifier.padding(horizontal = 12.dp)
                )
                HorizontalDivider(modifier = Modifier.weight(1f), color = Color(0xFFE0E0E0))
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            
            // Brand icons
            Row(
                modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                BrandIcon("Story TV", Color(0xFF581c4e))
                BrandIcon("Best\nDramas", Color(0xFF581c4e))
                BrandIcon("Top Shows", Color(0xFF581c4e))
                BrandIcon("Hit Movies", Color(0xFF581c4e))
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            
            // Ad Banner
            Card(
                modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp),
                shape = RoundedCornerShape(12.dp),
                colors = CardDefaults.cardColors(containerColor = Color.White),
                border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFE5E5E5)),
                elevation = CardDefaults.cardElevation(0.dp)
            ) {
                Row(
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 12.dp).fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Box(
                        modifier = Modifier.size(36.dp).background(Color(0xFFfce4ec), RoundedCornerShape(8.dp)),
                        contentAlignment = Alignment.Center
                    ) {
                        Text("₹10", color = Color(0xFFc2185b), fontSize = 12.sp, fontWeight = FontWeight.Bold)
                    }
                    Spacer(modifier = Modifier.width(16.dp))
                    Text(
                        text = "Daily Mutual Funds SIP @ ₹10",
                        fontSize = 14.sp,
                        color = Color(0xFF333333),
                        fontWeight = FontWeight.Medium
                    )
                    Spacer(modifier = Modifier.weight(1f))
                    Icon(Icons.Default.ChevronRight, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(20.dp))
                }
            }
            
            Spacer(modifier = Modifier.height(32.dp))
        }
        
        // Done Button at bottom
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 16.dp),
            contentAlignment = Alignment.Center
        ) {
            Button(
                onClick = onBack,
                modifier = Modifier
                    .fillMaxWidth(0.9f)
                    .height(48.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFF0F0F0)),
                shape = RoundedCornerShape(24.dp),
                elevation = ButtonDefaults.buttonElevation(0.dp)
            ) {
                Text("DONE", color = Color(0xFF5f259f), fontSize = 15.sp, fontWeight = FontWeight.Bold, letterSpacing = 0.5.sp)
            }
        }
    }
}

@Composable
fun BrandIcon(label: String, color: Color) {
    Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.width(64.dp)) {
        Box(
            modifier = Modifier.size(52.dp).background(color, RoundedCornerShape(12.dp)),
            contentAlignment = Alignment.Center
        ) {
            // Need specific icons for each, using generic ones
            Icon(
                imageVector = when {
                    label.contains("Story") -> Icons.Default.Tv
                    label.contains("Drama") -> Icons.Default.TheaterComedy
                    label.contains("Shows") -> Icons.Default.Star
                    else -> Icons.Default.Movie
                },
                contentDescription = label,
                tint = Color.White,
                modifier = Modifier.size(24.dp)
            )
        }
        Spacer(modifier = Modifier.height(8.dp))
        Text(label, fontSize = 11.sp, color = Color.Gray, textAlign = TextAlign.Center, lineHeight = 14.sp)
    }
}
"""

content = re.sub(r'@OptIn\(ExperimentalFoundationApi::class\)\n@Composable\nfun SuccessScreen\(accountId: String\?, viewModel: PrankViewModel, onBack: \(\) -> Unit\).*', new_success_screen, content, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt', 'w') as f:
    f.write(content)
