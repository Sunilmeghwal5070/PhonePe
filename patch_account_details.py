import re

with open('/app/applet/app/src/main/java/com/example/ui/screens/AccountDetailsScreen.kt', 'r') as f:
    content = f.read()

# Add viewModel, accountId, isEditable
content = content.replace('fun AccountDetailsScreen(\n    onBack: () -> Unit,\n    onNavigateToCheckBalance: () -> Unit\n) {',
'''import com.example.ui.PrankViewModel
import androidx.compose.runtime.collectAsState

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AccountDetailsScreen(
    accountId: String,
    isEditable: Boolean,
    viewModel: PrankViewModel,
    onBack: () -> Unit,
    onNavigateToCheckBalance: () -> Unit
) {
    val bankAccounts by viewModel.bankAccounts.collectAsState()
    val account = bankAccounts.find { it.id == accountId }
    
    var name by remember { mutableStateOf(account?.accountName ?: "John Doe") }
    var bankDesc by remember { mutableStateOf(account?.bankDesc ?: "Bank") }
    var accType by remember { mutableStateOf(account?.type ?: ": Saving Account") }
    var branch by remember { mutableStateOf(account?.branch ?: ": MAIN") }
    var ifsc by remember { mutableStateOf(account?.ifsc ?: ": IFSC") }
    var balance by remember { mutableStateOf(account?.balance ?: "Balance: ₹----") }
''')

# Now we need to change TopAppBar actions to add a SAVE button if isEditable
top_bar = '''TopAppBar(
                title = { Text("Account Details", fontWeight = FontWeight.Bold, fontSize = 20.sp) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    IconButton(onClick = { }) {
                        Icon(Icons.AutoMirrored.Filled.HelpOutline, contentDescription = "Help")
                    }
                },'''
new_top_bar = '''TopAppBar(
                title = { Text("Account Details", fontWeight = FontWeight.Bold, fontSize = 20.sp) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    if (isEditable) {
                        TextButton(onClick = {
                            account?.let {
                                viewModel.updateBankAccount(it.copy(
                                    accountName = name,
                                    bankDesc = bankDesc,
                                    type = accType,
                                    branch = branch,
                                    ifsc = ifsc,
                                    balance = balance
                                ))
                            }
                            onBack()
                        }) {
                            Text("SAVE", color = Color(0xFF5f259f), fontWeight = FontWeight.Bold)
                        }
                    } else {
                        IconButton(onClick = { }) {
                            Icon(Icons.AutoMirrored.Filled.HelpOutline, contentDescription = "Help")
                        }
                    }
                },'''
content = content.replace(top_bar, new_top_bar)

# Now we need to replace texts with BasicTextFields
content = content.replace(
    'Text("John", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color.Black)',
    'BasicTextField(value = name, onValueChange = { name = it }, textStyle = TextStyle(fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color.Black), enabled = isEditable)'
)
content = content.replace(
    'Text("Union Bank Of India - 0365", fontSize = 14.sp, color = Color.Gray)',
    'BasicTextField(value = bankDesc, onValueChange = { bankDesc = it }, textStyle = TextStyle(fontSize = 14.sp, color = Color.Gray), enabled = isEditable)'
)

content = content.replace(
    'Text(":  Saving Account", fontSize = 14.sp, color = Color.Gray)',
    'BasicTextField(value = accType, onValueChange = { accType = it }, textStyle = TextStyle(fontSize = 14.sp, color = Color.Gray), enabled = isEditable)'
)
content = content.replace(
    'Text(":  MUMBAI MAIN", fontSize = 14.sp, color = Color.Gray)',
    'BasicTextField(value = branch, onValueChange = { branch = it }, textStyle = TextStyle(fontSize = 14.sp, color = Color.Gray), enabled = isEditable)'
)
content = content.replace(
    'Text(":  UBIN0000000", fontSize = 14.sp, color = Color.Gray)',
    'BasicTextField(value = ifsc, onValueChange = { ifsc = it }, textStyle = TextStyle(fontSize = 14.sp, color = Color.Gray), enabled = isEditable)'
)
content = content.replace(
    'Text("Balance: ₹----", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.Black)',
    'BasicTextField(value = balance, onValueChange = { balance = it }, textStyle = TextStyle(fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.Black), enabled = isEditable)'
)

# Replace static bank logo url with dynamic
content = content.replace(
    'getBankLogoUrl("Union Bank")',
    'getBankLogoUrl(account?.bankName ?: "Bank")'
)

# And fix UPI IDs iteration
content = content.replace('''UpiIdRow("9876543210-2@axl", true)
                    UpiIdRow("9876543210-2@ybl", true)
                    UpiIdRow("9876543210-2@ibl", false)
                    UpiIdRow("johndoe123@ibl", true)
                    UpiIdRow("johndoe123@axl", false)
                    UpiIdRow("johndoe123@ybl", false)''', '''account?.upiIds?.forEachIndexed { index, upiId ->
                        UpiIdRow(upiId, isActivate = (index % 2 == 0))
                    }''')


# Fix duplicate @OptIn and import
content = content.replace('@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nimport', 'import')


with open('/app/applet/app/src/main/java/com/example/ui/screens/AccountDetailsScreen.kt', 'w') as f:
    f.write(content)
