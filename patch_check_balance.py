import re

with open('/app/applet/app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt', 'r') as f:
    content = f.read()

# Make CheckBalanceScreen accept PrankViewModel
content = content.replace(
'''@OptIn(ExperimentalMaterial3Api::class, ExperimentalAnimationApi::class)
@Composable
fun CheckBalanceScreen(onBack: () -> Unit) {
    var currentState by remember { mutableStateOf(CheckBalanceState.LIST) }''',
'''import com.example.ui.PrankViewModel
import com.example.ui.BankAccount
import androidx.compose.runtime.collectAsState
import android.widget.Toast
import androidx.compose.ui.platform.LocalContext

@OptIn(ExperimentalMaterial3Api::class, ExperimentalAnimationApi::class)
@Composable
fun CheckBalanceScreen(
    viewModel: PrankViewModel,
    onBack: () -> Unit
) {
    val bankAccounts by viewModel.bankAccounts.collectAsState()
    var selectedAccount by remember { mutableStateOf<BankAccount?>(null) }
    var currentState by remember { mutableStateOf(CheckBalanceState.LIST) }''')

# Now inside the AnimatedContent block
# Modify CheckBalanceState.LIST to pass bankAccounts and callback
content = content.replace(
'''            CheckBalanceState.LIST -> {
                BalanceListScreen(
                    onBack = onBack,
                    onAccountClick = { currentState = CheckBalanceState.PIN }
                )
            }''',
'''            CheckBalanceState.LIST -> {
                BalanceListScreen(
                    bankAccounts = bankAccounts,
                    onBack = onBack,
                    onAccountClick = { account -> 
                        selectedAccount = account
                        currentState = CheckBalanceState.PIN
                    }
                )
            }''')

# Modify PinEntryScreen block to check pin
content = content.replace(
'''            CheckBalanceState.PIN -> {
                PinEntryScreen(
                    pin = enteredPin,
                    onPinChange = { newPin -> enteredPin = newPin },
                    onSubmit = { 
                        currentState = CheckBalanceState.LOADING
                    }
                )
            }''',
'''            CheckBalanceState.PIN -> {
                val context = LocalContext.current
                PinEntryScreen(
                    pin = enteredPin,
                    onPinChange = { newPin -> enteredPin = newPin },
                    onSubmit = { 
                        if (enteredPin == selectedAccount?.pin) {
                            currentState = CheckBalanceState.LOADING
                        } else {
                            Toast.makeText(context, "Incorrect UPI PIN", Toast.LENGTH_SHORT).show()
                            enteredPin = ""
                        }
                    }
                )
            }''')

# Modify SuccessScreen to show selectedAccount's balance
content = content.replace(
'''            CheckBalanceState.SUCCESS -> {
                SuccessScreen(
                    onBack = { 
                        currentState = CheckBalanceState.LIST
                        enteredPin = ""
                    }
                )
            }''',
'''            CheckBalanceState.SUCCESS -> {
                SuccessScreen(
                    account = selectedAccount,
                    onBack = { 
                        currentState = CheckBalanceState.LIST
                        enteredPin = ""
                        selectedAccount = null
                    }
                )
            }''')

# Now redefine BalanceListScreen
old_balance_list = re.search(r'@OptIn\(ExperimentalMaterial3Api::class\)\n@Composable\nfun BalanceListScreen.*?// PhonePe Wallet', content, flags=re.DOTALL).group(0)
new_balance_list = '''@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun BalanceListScreen(
    bankAccounts: List<BankAccount>,
    onBack: () -> Unit,
    onAccountClick: (BankAccount) -> Unit
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Check Balance", fontWeight = FontWeight.Bold, fontSize = 20.sp) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    IconButton(onClick = { }) {
                        Icon(Icons.AutoMirrored.Filled.HelpOutline, contentDescription = "Help")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = Color.White
                )
            )
        },
        containerColor = Color.White
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .verticalScroll(rememberScrollState())
        ) {
            bankAccounts.forEach { account ->
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable { onAccountClick(account) }
                        .padding(horizontal = 16.dp, vertical = 12.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Box(
                        modifier = Modifier
                            .size(40.dp)
                            .border(1.dp, Color(0xFFEEEEEE), CircleShape),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(Icons.Default.AccountBalance, contentDescription = null, tint = Color(0xFF1976D2), modifier = Modifier.size(24.dp))
                    }
                    
                    Spacer(modifier = Modifier.width(16.dp))
                    
                    Column(modifier = Modifier.weight(1f)) {
                        Text(account.bankName, fontSize = 16.sp, color = Color.Black)
                        Text("Bank Account", color = Color.Gray, fontSize = 14.sp)
                    }
                    
                    Icon(
                        imageVector = Icons.AutoMirrored.Filled.KeyboardArrowRight,
                        contentDescription = null,
                        tint = Color.Gray
                    )
                }
                HorizontalDivider(color = Color(0xFFF5F5F5), thickness = 1.dp, modifier = Modifier.padding(start = 72.dp))
            }
            // PhonePe Wallet'''
content = content.replace(old_balance_list, new_balance_list)

# Now redefine SuccessScreen
old_success = re.search(r'@Composable\nfun SuccessScreen\(onBack: \(\) -> Unit\) \{.*?Text\("₹10", fontSize = 42\.sp, color = Color\.Black\)', content, flags=re.DOTALL).group(0)
new_success = '''@Composable
fun SuccessScreen(account: BankAccount?, onBack: () -> Unit) {
    androidx.activity.compose.BackHandler { onBack() }
    
    Column(
        modifier = Modifier.fillMaxSize().background(Color.White),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(modifier = Modifier.height(48.dp))
        
        Box(
            modifier = Modifier.size(120.dp).background(Color(0xFF388E3C), CircleShape),
            contentAlignment = Alignment.Center
        ) {
            Icon(Icons.Default.Check, contentDescription = "Success", tint = Color.White, modifier = Modifier.size(80.dp))
        }
        
        Spacer(modifier = Modifier.height(32.dp))
        
        Text(
            text = "Available Balance fetched\nsuccessful",
            fontSize = 22.sp,
            fontWeight = FontWeight.Bold,
            color = Color.Black,
            textAlign = TextAlign.Center,
            modifier = Modifier.padding(horizontal = 24.dp)
        )
        
        Spacer(modifier = Modifier.height(24.dp))
        
        Row(verticalAlignment = Alignment.CenterVertically) {
            Canvas(modifier = Modifier.size(24.dp)) {
                val path1 = Path().apply {
                    moveTo(size.width * 0.2f, size.height * 0.8f)
                    lineTo(size.width * 0.5f, size.height * 0.2f)
                    lineTo(size.width * 0.8f, size.height * 0.8f)
                    close()
                }
                drawPath(path1, color = Color(0xFF1976D2), style = Stroke(width = 2.dp.toPx()))
                
                val path2 = Path().apply {
                    moveTo(size.width * 0.2f, size.height * 0.4f)
                    lineTo(size.width * 0.5f, size.height * 1.0f)
                    lineTo(size.width * 0.8f, size.height * 0.4f)
                    close()
                }
                drawPath(path2, color = Color(0xFFFFC107), style = Stroke(width = 2.dp.toPx()))
            }
            Spacer(modifier = Modifier.width(12.dp))
            Text(account?.bankDesc ?: "Bank", fontSize = 18.sp, color = Color.Black)
        }
        
        Spacer(modifier = Modifier.height(24.dp))
        
        Text("Available Balance", fontSize = 14.sp, color = Color.Gray)
        Spacer(modifier = Modifier.height(8.dp))
        Text(account?.balance ?: "Balance: ₹----", fontSize = 42.sp, color = Color.Black)'''
content = content.replace(old_success, new_success)

# Fix duplicate import
content = content.replace('@OptIn(ExperimentalMaterial3Api::class, ExperimentalAnimationApi::class)\n@Composable\nimport', 'import')

with open('/app/applet/app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt', 'w') as f:
    f.write(content)
