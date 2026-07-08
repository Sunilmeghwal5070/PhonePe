import re

with open('/app/applet/app/src/main/java/com/example/ui/screens/BankAccountsScreen.kt', 'r') as f:
    content = f.read()

if 'import androidx.compose.foundation.text.BasicTextField' not in content:
    content = content.replace('import androidx.compose.ui.text.font.FontWeight', 'import androidx.compose.ui.text.font.FontWeight\nimport androidx.compose.foundation.text.BasicTextField\nimport androidx.compose.ui.text.TextStyle\nimport androidx.compose.runtime.mutableStateOf\nimport androidx.compose.runtime.remember\nimport androidx.compose.runtime.getValue\nimport androidx.compose.runtime.setValue')

state_block = """@Composable
fun BankAccountsScreen(
    onBack: () -> Unit,
    onNavigateToAccountDetails: () -> Unit,
    onNavigateToAddBankAccount: () -> Unit
) {
    var name by remember { mutableStateOf("Sunil") }"""

content = content.replace("""@Composable
fun BankAccountsScreen(
    onBack: () -> Unit,
    onNavigateToAccountDetails: () -> Unit,
    onNavigateToAddBankAccount: () -> Unit
) {""", state_block)

content = content.replace(
    'Text("Sunil", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.Black, modifier = Modifier.weight(1f))',
    'BasicTextField(value = name, onValueChange = { name = it }, textStyle = TextStyle(fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.Black), modifier = Modifier.weight(1f))'
)

with open('/app/applet/app/src/main/java/com/example/ui/screens/BankAccountsScreen.kt', 'w') as f:
    f.write(content)
