import re

with open('app/src/main/java/com/example/ui/screens/AccountDetailsScreen.kt', 'r') as f:
    text = f.read()

target = """                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("CHECK BALANCE", color = Color(0xFF5f259f), fontWeight = FontWeight.Bold, fontSize = 14.sp, modifier = Modifier.clickable { onNavigateToCheckBalance() })
                    Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(16.dp))
                }
            }"""

replacement = """                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("CHECK BALANCE", color = Color(0xFF5f259f), fontWeight = FontWeight.Bold, fontSize = 14.sp, modifier = Modifier.clickable { onNavigateToCheckBalance() })
                    Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(16.dp))
                }
            }
            
            // Add Balance Card (Mock Ad)
            var showAdDialog by remember { mutableStateOf(false) }
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 4.dp),
                colors = CardDefaults.cardColors(containerColor = Color.White),
                shape = RoundedCornerShape(12.dp)
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable { showAdDialog = true }
                        .padding(16.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("ADD ₹500 BALANCE (WATCH AD)", color = Color(0xFF388E3C), fontWeight = FontWeight.Bold, fontSize = 14.sp)
                    Icon(Icons.Default.Add, contentDescription = null, tint = Color(0xFF388E3C), modifier = Modifier.size(16.dp))
                }
            }
            
            if (showAdDialog && account != null) {
                var adProgress by remember { mutableStateOf(5) }
                
                androidx.compose.runtime.LaunchedEffect(Unit) {
                    while (adProgress > 0) {
                        kotlinx.coroutines.delay(1000)
                        adProgress--
                    }
                    // Reward user
                    viewModel.updateBankAccount(account.copy(balance = account.balance + 500))
                    showAdDialog = false
                    android.widget.Toast.makeText(context, "₹500 added to your account!", android.widget.Toast.LENGTH_SHORT).show()
                }
                
                androidx.compose.ui.window.Dialog(onDismissRequest = { }) {
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(300.dp)
                            .padding(16.dp),
                        colors = CardDefaults.cardColors(containerColor = Color.Black),
                        shape = RoundedCornerShape(16.dp)
                    ) {
                        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                Text("Sponsor Ad", color = Color.White, fontSize = 24.sp, fontWeight = FontWeight.Bold)
                                Spacer(modifier = Modifier.height(16.dp))
                                Text("Please wait... $adProgress", color = Color.Yellow, fontSize = 18.sp)
                                Spacer(modifier = Modifier.height(32.dp))
                                Text("Unity Ads Mock", color = Color.Gray, fontSize = 12.sp)
                            }
                        }
                    }
                }
            }"""

text = text.replace(target, replacement)
text = text.replace("import androidx.compose.material.icons.filled.Edit", "import androidx.compose.material.icons.filled.Edit\nimport androidx.compose.material.icons.filled.Add")

with open('app/src/main/java/com/example/ui/screens/AccountDetailsScreen.kt', 'w') as f:
    f.write(text)
