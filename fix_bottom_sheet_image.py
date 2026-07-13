import re

with open('app/src/main/java/com/example/ui/screens/PayAmountScreen.kt', 'r') as f:
    text = f.read()

target = """Box(modifier = Modifier.size(32.dp).border(1.dp, Color(0xFFE0E0E0), RoundedCornerShape(8.dp)), contentAlignment = Alignment.Center) { coil.compose.AsyncImage(model = getBankLogoUrl(bank.bankName), contentDescription = null, modifier = Modifier.fillMaxSize().padding(4.dp), contentScale = androidx.compose.ui.layout.ContentScale.Fit) }"""

replacement = """Box(modifier = Modifier.size(32.dp).border(1.dp, Color(0xFFE0E0E0), RoundedCornerShape(8.dp)), contentAlignment = Alignment.Center) { coil.compose.AsyncImage(model = coil.request.ImageRequest.Builder(androidx.compose.ui.platform.LocalContext.current).data(getBankLogoUrl(bank.bankName)).crossfade(true).build(), contentDescription = null, modifier = Modifier.fillMaxSize().padding(4.dp), contentScale = androidx.compose.ui.layout.ContentScale.Fit) }"""

text = text.replace(target, replacement)
text = text.replace("currentSelectedBank.id == bank.id", "currentSelectedBank?.id == bank.id")

with open('app/src/main/java/com/example/ui/screens/PayAmountScreen.kt', 'w') as f:
    f.write(text)
