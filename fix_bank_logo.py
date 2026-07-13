import re

with open('app/src/main/java/com/example/ui/screens/PayAmountScreen.kt', 'r') as f:
    text = f.read()

text = text.replace("com.example.ui.components.BankLogo(bank.bankName, 32.dp)", """Box(modifier = Modifier.size(32.dp).border(1.dp, Color(0xFFE0E0E0), RoundedCornerShape(8.dp)), contentAlignment = Alignment.Center) { coil.compose.AsyncImage(model = getBankLogoUrl(bank.bankName), contentDescription = null, modifier = Modifier.fillMaxSize().padding(4.dp), contentScale = androidx.compose.ui.layout.ContentScale.Fit) }""")
text = text.replace("com.example.ui.components.BankLogo(selectedBank.bankName, 32.dp)", """Box(modifier = Modifier.size(32.dp).border(1.dp, Color(0xFFE0E0E0), RoundedCornerShape(8.dp)), contentAlignment = Alignment.Center) { coil.compose.AsyncImage(model = getBankLogoUrl(selectedBank.bankName), contentDescription = null, modifier = Modifier.fillMaxSize().padding(4.dp), contentScale = androidx.compose.ui.layout.ContentScale.Fit) }""")


with open('app/src/main/java/com/example/ui/screens/PayAmountScreen.kt', 'w') as f:
    f.write(text)
