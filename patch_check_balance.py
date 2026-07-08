import re

with open("app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt", "r") as f:
    content = f.read()

# Replace bankAccounts.forEach block
old_account_row = r"""                    BankLogo\(account\.bankName\)
                    
                    Spacer\(modifier = Modifier\.width\(16\.dp\)\)
                    
                    Column\(modifier = Modifier\.weight\(1f\)\) \{
                        Text\(account\.bankName, fontSize = 16\.sp, color = Color\.Black\)
                        Text\("Bank Account", color = Color\.Gray, fontSize = 14\.sp\)
                    \}"""

new_account_row = """                    BankLogo(account.bankName)
                    
                    Spacer(modifier = Modifier.width(16.dp))
                    
                    Column(modifier = Modifier.weight(1f)) {
                        Text(account.accountName, fontSize = 16.sp, color = Color.Black)
                        Text("Bank Account", color = Color.Gray, fontSize = 14.sp)
                    }"""

content = re.sub(old_account_row, new_account_row, content)

# Add Daily Mutual Fund Card before bankAccounts.forEach
old_column_start = r"""        Column\(
            modifier = Modifier
                \.fillMaxSize\(\)
                \.padding\(paddingValues\)
                \.verticalScroll\(rememberScrollState\(\)\)
        \) \{"""

new_column_start = """        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .verticalScroll(rememberScrollState())
        ) {
            // Daily Mutual Fund Card
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                shape = RoundedCornerShape(12.dp),
                colors = CardDefaults.cardColors(containerColor = Color.White),
                border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFF0F0F0))
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 12.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text("Daily Mutual Fund SIP @ ₹10!", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.Black)
                            Spacer(modifier = Modifier.width(4.dp))
                            Icon(Icons.AutoMirrored.Filled.ArrowForward, contentDescription = null, modifier = Modifier.size(16.dp).background(Color.Black, CircleShape).padding(2.dp), tint = Color.White)
                        }
                        Spacer(modifier = Modifier.height(4.dp))
                        Text("Invest now", color = Color.Gray, fontSize = 13.sp)
                    }
                    // Mutual Fund Jar Icon
                    Box(
                        modifier = Modifier
                            .size(48.dp)
                            .background(Color(0xFFE3F2FD), RoundedCornerShape(8.dp)),
                        contentAlignment = Alignment.Center
                    ) {
                        Text("₹10", color = Color(0xFFE91E63), fontWeight = FontWeight.Bold, fontSize = 12.sp)
                    }
                }
            }
"""

content = re.sub(old_column_start, new_column_start, content)

# Add RuPay Credit Card
old_add_new_payment = r"""            // Add new payment method"""
new_add_new_payment = """            HorizontalDivider(color = Color(0xFFF5F5F5), thickness = 1.dp, modifier = Modifier.padding(start = 72.dp))
            // RuPay Credit Card
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable { }
                    .padding(horizontal = 16.dp, vertical = 16.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(
                    imageVector = Icons.Default.CreditCard,
                    contentDescription = null,
                    tint = Color(0xFF1976D2),
                    modifier = Modifier.size(32.dp).padding(start = 4.dp, end = 4.dp)
                )
                
                Spacer(modifier = Modifier.width(16.dp))
                
                Column(modifier = Modifier.weight(1f)) {
                    Text("RuPay Credit Card", fontSize = 16.sp, color = Color.Black)
                }
                
                Text(
                    text = "Link Now",
                    color = Color(0xFF5f259f),
                    fontWeight = FontWeight.Bold,
                    fontSize = 14.sp
                )
            }
            
            HorizontalDivider(color = Color(0xFFF5F5F5), thickness = 1.dp, modifier = Modifier.padding(start = 72.dp))

            // Add new payment method"""

content = content.replace(old_add_new_payment, new_add_new_payment)

# Add Powered by UPI at the very bottom
old_end = r"""            Spacer\(modifier = Modifier\.height\(24\.dp\)\)
        \}
    \}
\}"""

new_end = """            Spacer(modifier = Modifier.height(24.dp))
            
            // Powered by UPI footer
            Column(
                modifier = Modifier.fillMaxWidth().padding(bottom = 32.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                coil.compose.AsyncImage(
                    model = coil.request.ImageRequest.Builder(androidx.compose.ui.platform.LocalContext.current)
                        .data("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/UPI-Logo-vector.svg/1024px-UPI-Logo-vector.svg.png")
                        .crossfade(true)
                        .build(),
                    contentDescription = "UPI",
                    modifier = Modifier.height(24.dp),
                    contentScale = androidx.compose.ui.layout.ContentScale.Fit
                )
            }
        }
    }
}"""
content = re.sub(old_end, new_end, content)

with open("app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt", "w") as f:
    f.write(content)
