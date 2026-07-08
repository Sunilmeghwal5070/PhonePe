import re

with open('/app/applet/app/src/main/java/com/example/ui/screens/AddBankAccountDetailsScreen.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'Text(bankName.take(1), fontWeight = FontWeight.Bold, color = Color(0xFF5f259f), fontSize = 20.sp)',
    'coil.compose.AsyncImage(model = getBankLogoUrl(bankName), contentDescription = bankName, modifier = Modifier.size(32.dp).clip(RoundedCornerShape(8.dp)), contentScale = androidx.compose.ui.layout.ContentScale.Fit)'
)

if 'import coil.compose.AsyncImage' not in content:
    content = content.replace('import androidx.compose.runtime.*', 'import androidx.compose.runtime.*\nimport coil.compose.AsyncImage\nimport androidx.compose.ui.draw.clip')

with open('/app/applet/app/src/main/java/com/example/ui/screens/AddBankAccountDetailsScreen.kt', 'w') as f:
    f.write(content)

