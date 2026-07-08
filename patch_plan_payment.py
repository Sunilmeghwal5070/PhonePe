import re

with open('/app/applet/app/src/main/java/com/example/ui/screens/RechargeScreens.kt', 'r') as f:
    content = f.read()

# Add a new state for payment bottom sheet
content = content.replace(
    'var selectedPlan by remember { mutableStateOf<RechargePlan?>(null) }',
    'var selectedPlan by remember { mutableStateOf<RechargePlan?>(null) }\n    var showPaymentSheet by remember { mutableStateOf(false) }'
)

# Update the button to show payment sheet
content = content.replace(
    'onProceedToPay(selectedPlan!!.price)\n                        selectedPlan = null',
    'showPaymentSheet = true'
)

# Add the payment sheet
payment_sheet_code = """
    if (showPaymentSheet && selectedPlan != null) {
        val total = selectedPlan!!.price
        val bankAccounts by viewModel.bankAccounts.collectAsState()
        val defaultAccount = bankAccounts.firstOrNull()
        
        ModalBottomSheet(
            onDismissRequest = { showPaymentSheet = false },
            containerColor = Color.White,
            shape = RoundedCornerShape(topStart = 16.dp, topEnd = 16.dp)
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column {
                        Text("Total Payable", fontSize = 16.sp, fontWeight = FontWeight.Bold)
                        Text("Show breakup", fontSize = 14.sp, color = Color(0xFF5f259f), fontWeight = FontWeight.Bold)
                    }
                    Text("₹$total", fontSize = 24.sp, fontWeight = FontWeight.Bold)
                    IconButton(onClick = { showPaymentSheet = false }) {
                        Icon(Icons.Default.Close, contentDescription = "Close")
                    }
                }
                
                Spacer(modifier = Modifier.height(16.dp))
                
                if (defaultAccount != null) {
                    Card(
                        modifier = Modifier.fillMaxWidth(),
                        colors = CardDefaults.cardColors(containerColor = Color(0xFFF5F5F5)),
                        shape = RoundedCornerShape(8.dp)
                    ) {
                        Row(
                            modifier = Modifier.padding(16.dp).fillMaxWidth(),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            com.example.ui.components.BankLogo(bankName = defaultAccount.bankName, modifier = Modifier.size(32.dp))
                            Spacer(modifier = Modifier.width(16.dp))
                            Column(modifier = Modifier.weight(1f)) {
                                Text(defaultAccount.accountName, fontSize = 16.sp, fontWeight = FontWeight.Medium)
                                Text("•• ${defaultAccount.bankDesc.takeLast(4)} UPI", fontSize = 14.sp, color = Color.Gray)
                            }
                            Text("₹$total", fontSize = 16.sp, fontWeight = FontWeight.Bold)
                            Spacer(modifier = Modifier.width(8.dp))
                            Icon(Icons.Default.CheckCircle, contentDescription = null, tint = Color(0xFF4CAF50))
                        }
                    }
                }
                
                Spacer(modifier = Modifier.height(12.dp))
                
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(containerColor = Color(0xFFF5F5F5)),
                    shape = RoundedCornerShape(8.dp)
                ) {
                    Row(
                        modifier = Modifier.padding(16.dp).fillMaxWidth(),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Box(
                            modifier = Modifier.size(32.dp).background(Color.LightGray, RoundedCornerShape(4.dp))
                        )
                        Spacer(modifier = Modifier.width(16.dp))
                        Column(modifier = Modifier.weight(1f)) {
                            Text("PhonePe Wallet", fontSize = 16.sp, color = Color.Gray)
                            Text("Usable balance: ₹0", fontSize = 14.sp, color = Color.Gray)
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(Icons.Default.ErrorOutline, contentDescription = null, tint = Color.Red, modifier = Modifier.size(14.dp))
                                Spacer(modifier = Modifier.width(4.dp))
                                Text("Insufficient balance", fontSize = 14.sp, color = Color.Red)
                            }
                        }
                    }
                }
                
                Spacer(modifier = Modifier.height(24.dp))
                
                Button(
                    onClick = { 
                        showPaymentSheet = false
                        selectedPlan?.let { onProceedToPay(it.price) }
                        selectedPlan = null 
                    },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(50.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF5f259f)),
                    shape = RoundedCornerShape(8.dp)
                ) {
                    Text("Pay ₹$total", color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                }
                Spacer(modifier = Modifier.height(16.dp))
            }
        }
    }
"""

content = content + "\n" + payment_sheet_code

# We need to place this before the last closing brace of RechargePlanScreen. Let's do it cleaner.
