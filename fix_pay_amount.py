import re

with open('app/src/main/java/com/example/ui/screens/PayAmountScreen.kt', 'r') as f:
    text = f.read()

target = """                Card(
                    colors = CardDefaults.cardColors(containerColor = Color(0xFFF5F5F5)),
                    shape = RoundedCornerShape(12.dp)
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("Recommended", color = Color.Gray, fontSize = 12.sp)
                        Spacer(modifier = Modifier.height(8.dp))
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            // Bank Logo Placeholder
                            com.example.ui.components.BankLogo(selectedBank.bankName, 32.dp)
                            Spacer(modifier = Modifier.width(12.dp))
                            Column(modifier = Modifier.weight(1f)) {
                                Text(selectedBank.accountName, fontSize = 16.sp)
                                Text("•• ${selectedBank.bankDesc.takeLast(4)} UPI", color = Color.Gray, fontSize = 14.sp)
                            }
                            Text("₹$amount", fontWeight = FontWeight.Bold, fontSize = 16.sp)
                            Spacer(modifier = Modifier.width(8.dp))
                            Icon(Icons.Default.CheckCircle, contentDescription = null, tint = Color(0xFF388E3C))
                        }
                    }
                }"""

replacement = """                var currentSelectedBank by remember { mutableStateOf(selectedBank) }
                
                Card(
                    colors = CardDefaults.cardColors(containerColor = Color(0xFFF5F5F5)),
                    shape = RoundedCornerShape(12.dp)
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("Accounts", color = Color.Gray, fontSize = 12.sp)
                        Spacer(modifier = Modifier.height(8.dp))
                        
                        bankAccounts.forEach { bank ->
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .clickable { currentSelectedBank = bank }
                                    .padding(vertical = 8.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                com.example.ui.components.BankLogo(bank.bankName, 32.dp)
                                Spacer(modifier = Modifier.width(12.dp))
                                Column(modifier = Modifier.weight(1f)) {
                                    Text(bank.accountName, fontSize = 16.sp)
                                    Text("•• ${bank.bankDesc.takeLast(4)} UPI", color = Color.Gray, fontSize = 14.sp)
                                }
                                Text("₹$amount", fontWeight = FontWeight.Bold, fontSize = 16.sp)
                                Spacer(modifier = Modifier.width(8.dp))
                                if (currentSelectedBank.id == bank.id) {
                                    Icon(Icons.Default.CheckCircle, contentDescription = null, tint = Color(0xFF388E3C))
                                } else {
                                    Box(modifier = Modifier.size(24.dp))
                                }
                            }
                        }
                    }
                }"""

text = text.replace(target, replacement)
text = text.replace("onProceed(amount, selectedBank)", "onProceed(amount, currentSelectedBank)")
# Also need to make sure currentSelectedBank is passed

with open('app/src/main/java/com/example/ui/screens/PayAmountScreen.kt', 'w') as f:
    f.write(text)
