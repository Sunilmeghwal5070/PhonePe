import re

with open("app/src/main/java/com/example/ui/screens/PaymentSuccessScreen.kt", "r") as f:
    content = f.read()

# Add bankName parameter
pattern_params = r"""fun PaymentSuccessScreen\(\s*amount: String,\s*payeeName: String = "Karishna Karishna",\s*upiId: String = "krishna88750@axl",\s*onDone: \(\) -> Unit,\s*onViewDetails: \(\) -> Unit\s*\) \{"""
replacement_params = """fun PaymentSuccessScreen(
    amount: String,
    payeeName: String = "Karishna Karishna",
    upiId: String = "krishna88750@axl",
    bankName: String = "State Bank of India",
    onDone: () -> Unit,
    onViewDetails: () -> Unit
) {"""
content = re.sub(pattern_params, replacement_params, content)

# Add bank logo inside Card
pattern_card = r"""HorizontalDivider\(thickness = 1\.dp, color = Color\(0xFFEEEEEE\)\)\s*Row\(\s*modifier = Modifier\.fillMaxWidth\(\)\.padding\(top = 16\.dp\),"""
replacement_card = """HorizontalDivider(thickness = 1.dp, color = Color(0xFFEEEEEE))
                
                Row(
                    modifier = Modifier.fillMaxWidth().padding(vertical = 12.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        com.example.ui.components.BankLogo(bankName = bankName, size = 24.dp)
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(bankName, fontSize = 14.sp, color = Color.Gray)
                    }
                }
                
                HorizontalDivider(thickness = 1.dp, color = Color(0xFFEEEEEE))
                
                Row(
                    modifier = Modifier.fillMaxWidth().padding(top = 16.dp),"""
content = re.sub(pattern_card, replacement_card, content)

# Add powered by UPI and ICICI below the done button
pattern_footer = r"""TextButton\(\s*onClick = onDone,\s*modifier = Modifier\.padding\(bottom = 32\.dp\)\s*\)\s*\{\s*Text\("Done", color = Color\(0xFF512DA8\), fontWeight = FontWeight\.Bold, fontSize = 18\.sp\)\s*\}\s*\}\s*\}"""
replacement_footer = """TextButton(
            onClick = onDone,
            modifier = Modifier.padding(bottom = 16.dp)
        ) {
            Text("Done", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 18.sp)
        }
        
        Column(
            modifier = Modifier.fillMaxWidth().padding(bottom = 32.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text("Powered by", fontSize = 12.sp, color = Color.White.copy(alpha = 0.7f))
            Spacer(modifier = Modifier.height(8.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
                coil.compose.AsyncImage(
                    model = coil.request.ImageRequest.Builder(androidx.compose.ui.platform.LocalContext.current)
                        .data("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/UPI-Logo-vector.svg/1024px-UPI-Logo-vector.svg.png")
                        .crossfade(true)
                        .build(),
                    contentDescription = "UPI",
                    modifier = Modifier.height(20.dp),
                    colorFilter = androidx.compose.ui.graphics.ColorFilter.tint(Color.White),
                    contentScale = androidx.compose.ui.layout.ContentScale.Fit
                )
                Spacer(modifier = Modifier.width(8.dp))
                Text("|", color = Color.White.copy(alpha = 0.7f))
                Spacer(modifier = Modifier.width(8.dp))
                coil.compose.AsyncImage(
                    model = coil.request.ImageRequest.Builder(androidx.compose.ui.platform.LocalContext.current)
                        .data("https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/ICICI_Bank_Logo.svg/512px-ICICI_Bank_Logo.svg.png")
                        .crossfade(true)
                        .build(),
                    contentDescription = "ICICI Bank",
                    modifier = Modifier.height(20.dp),
                    contentScale = androidx.compose.ui.layout.ContentScale.Fit
                )
            }
        }
    }
}"""
content = re.sub(pattern_footer, replacement_footer, content)

with open("app/src/main/java/com/example/ui/screens/PaymentSuccessScreen.kt", "w") as f:
    f.write(content)
