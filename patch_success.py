import re

with open('/app/applet/app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt', 'r') as f:
    content = f.read()

# Add ExperimentalFoundationApi and import combinedClickable
if 'import androidx.compose.foundation.ExperimentalFoundationApi' not in content:
    content = content.replace('import androidx.compose.foundation.clickable', 'import androidx.compose.foundation.clickable\nimport androidx.compose.foundation.ExperimentalFoundationApi\nimport androidx.compose.foundation.combinedClickable')

# Add Keyboard imports
if 'import androidx.compose.foundation.text.KeyboardOptions' not in content:
    content = content.replace('import androidx.compose.runtime.collectAsState', 'import androidx.compose.runtime.collectAsState\nimport androidx.compose.foundation.text.KeyboardOptions\nimport androidx.compose.ui.text.input.KeyboardType')

# Update SuccessScreen signature
content = content.replace('fun SuccessScreen(account: BankAccount?, onBack: () -> Unit) {', '@OptIn(ExperimentalFoundationApi::class)\n@Composable\nfun SuccessScreen(account: BankAccount?, viewModel: PrankViewModel, onBack: () -> Unit) {')

# Update SuccessScreen call
content = content.replace('SuccessScreen(\n                    account = selectedAccount,\n                    onBack = {', 'SuccessScreen(\n                    account = selectedAccount,\n                    viewModel = viewModel,\n                    onBack = {')


# Update balance display
target_balance = 'Text("₹${account?.balance ?: "1297.0"}", fontSize = 42.sp, color = Color.Black)'

replacement_balance = """        var isEditing by remember { mutableStateOf(false) }
        var editedBalance by remember { mutableStateOf(account?.balance?.toString() ?: "1297.0") }

        if (isEditing) {
            OutlinedTextField(
                value = editedBalance,
                onValueChange = { editedBalance = it },
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                modifier = Modifier.width(200.dp),
                textStyle = androidx.compose.ui.text.TextStyle(fontSize = 24.sp, textAlign = TextAlign.Center)
            )
            Spacer(modifier = Modifier.height(8.dp))
            Button(onClick = { 
                isEditing = false
                val newBal = editedBalance.toDoubleOrNull() ?: 1297.0
                account?.let { viewModel.updateBankAccount(it.copy(balance = newBal)) }
            }) {
                Text("Save")
            }
        } else {
            Text(
                "₹${account?.balance ?: "1297.0"}", 
                fontSize = 42.sp, 
                color = Color.Black,
                modifier = Modifier.combinedClickable(
                    onClick = {},
                    onLongClick = { isEditing = true }
                )
            )
        }"""

content = content.replace(target_balance, replacement_balance)
content = content.replace('@Composable\n@OptIn(ExperimentalFoundationApi::class)\n@Composable', '@OptIn(ExperimentalFoundationApi::class)\n@Composable')

with open('/app/applet/app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt', 'w') as f:
    f.write(content)
