import re

with open('/app/applet/app/src/main/java/com/example/ui/screens/BankAccountsScreen.kt', 'r') as f:
    content = f.read()

content = content.replace('fun BankAccountsScreen(\n    onBack: () -> Unit,\n    onNavigateToAccountDetails: () -> Unit,\n    onNavigateToAddBankAccount: () -> Unit\n) {',
'''import com.example.ui.PrankViewModel
import androidx.compose.runtime.collectAsState
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun BankAccountsScreen(
    viewModel: PrankViewModel,
    onBack: () -> Unit,
    onNavigateToAccountDetails: (String, Boolean) -> Unit,
    onNavigateToAddBankAccount: () -> Unit
) {
    val bankAccounts by viewModel.bankAccounts.collectAsState()
    var isEditMode by remember { mutableStateOf(false) }''')

content = content.replace('IconButton(onClick = { }) {\n                        Icon(Icons.AutoMirrored.Filled.HelpOutline, contentDescription = "Help")',
'''IconButton(onClick = { isEditMode = !isEditMode }) {
                        Icon(Icons.AutoMirrored.Filled.HelpOutline, contentDescription = "Help", tint = if (isEditMode) Color(0xFF5f259f) else Color.Black)''')

old_card = '''Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp)
                    .clickable { onNavigateToAccountDetails() },
                colors = CardDefaults.cardColors(containerColor = Color.White),
                shape = RoundedCornerShape(12.dp),
                elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    // Union Bank Logo
                    Box(
                        modifier = Modifier
                            .size(40.dp)
                            .border(1.dp, Color(0xFFEEEEEE), RoundedCornerShape(8.dp)),
                        contentAlignment = Alignment.Center
                    ) {
                        coil.compose.AsyncImage(
                            model = getBankLogoUrl("Union Bank"),
                            contentDescription = "Union Bank",
                            modifier = Modifier.size(32.dp).clip(RoundedCornerShape(8.dp)),
                            contentScale = androidx.compose.ui.layout.ContentScale.Fit
                        )
                    }
                    
                    Spacer(modifier = Modifier.width(16.dp))
                    
                    Text("John", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.Black, modifier = Modifier.weight(1f))
                    
                    Box(
                        modifier = Modifier
                            .background(Color(0xFF388E3C), RoundedCornerShape(12.dp))
                            .padding(horizontal = 8.dp, vertical = 4.dp)
                    ) {
                        Text("Primary", color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                    }
                    
                    Spacer(modifier = Modifier.width(16.dp))
                    
                    Icon(Icons.Default.KeyboardArrowRight, contentDescription = null, tint = Color.Gray)
                }
            }'''

new_card = '''LazyColumn(modifier = Modifier.fillMaxWidth().weight(1f)) {
                items(bankAccounts) { account ->
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 16.dp, vertical = 8.dp)
                            .clickable { onNavigateToAccountDetails(account.id, isEditMode) },
                        colors = CardDefaults.cardColors(containerColor = Color.White),
                        shape = RoundedCornerShape(12.dp),
                        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
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
                                    .border(1.dp, Color(0xFFEEEEEE), RoundedCornerShape(8.dp)),
                                contentAlignment = Alignment.Center
                            ) {
                                coil.compose.AsyncImage(
                                    model = getBankLogoUrl(account.bankName),
                                    contentDescription = account.bankName,
                                    modifier = Modifier.size(32.dp).clip(RoundedCornerShape(8.dp)),
                                    contentScale = androidx.compose.ui.layout.ContentScale.Fit
                                )
                            }
                            
                            Spacer(modifier = Modifier.width(16.dp))
                            
                            Text(account.accountName, fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.Black, modifier = Modifier.weight(1f))
                            
                            if (bankAccounts.indexOf(account) == 0) {
                                Box(
                                    modifier = Modifier
                                        .background(Color(0xFF388E3C), RoundedCornerShape(12.dp))
                                        .padding(horizontal = 8.dp, vertical = 4.dp)
                                ) {
                                    Text("Primary", color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                                }
                            }
                            
                            Spacer(modifier = Modifier.width(16.dp))
                            
                            Icon(Icons.AutoMirrored.Filled.KeyboardArrowRight, contentDescription = null, tint = Color.Gray)
                        }
                    }
                }
            }'''

content = content.replace(old_card, new_card)
content = content.replace('@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nimport', 'import')

with open('/app/applet/app/src/main/java/com/example/ui/screens/BankAccountsScreen.kt', 'w') as f:
    f.write(content)
