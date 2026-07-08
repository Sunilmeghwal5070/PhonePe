with open('/app/applet/app/src/main/java/com/example/ui/components/BankLogo.kt', 'r') as f:
    content = f.read()

import re

# Add PainterResource import
content = content.replace(
    'import androidx.compose.ui.layout.ContentScale',
    'import androidx.compose.ui.layout.ContentScale\nimport androidx.compose.ui.res.painterResource\nimport android.annotation.SuppressLint'
)

new_logic = """
@SuppressLint("DiscouragedApi")
@Composable
fun BankLogo(bankName: String, size: Dp = 40.dp, modifier: Modifier = Modifier) {
    val context = LocalContext.current
    
    val safeBankName = bankName.lowercase().replace(" ", "_").replace("-", "_")
    
    // Map common names to standard short codes for local images
    val imageCode = when {
        safeBankName.contains("state_bank") || safeBankName == "sbi" -> "sbi"
        safeBankName.contains("hdfc") -> "hdfc"
        safeBankName.contains("icici") -> "icici"
        safeBankName.contains("punjab") || safeBankName == "pnb" -> "pnb"
        safeBankName.contains("baroda") || safeBankName == "bob" -> "bob"
        safeBankName.contains("axis") -> "axis"
        safeBankName.contains("paytm") -> "paytm"
        safeBankName.contains("union") -> "union"
        safeBankName.contains("canara") -> "canara"
        safeBankName.contains("kotak") -> "kotak"
        safeBankName.contains("yes_bank") -> "yes"
        safeBankName.contains("indusind") -> "indusind"
        safeBankName.contains("idfc") -> "idfc"
        safeBankName.contains("india_post") -> "ippb"
        safeBankName.contains("airtel") -> "airtel"
        else -> safeBankName
    }
    
    // Expected file name: logo_sbi.png, logo_hdfc.png, etc. in res/drawable
    val expectedDrawableName = "logo_$imageCode"
    val resourceId = context.resources.getIdentifier(expectedDrawableName, "drawable", context.packageName)
    
    if (resourceId != 0) {
        // Local image found
        androidx.compose.foundation.Image(
            painter = painterResource(id = resourceId),
            contentDescription = bankName,
            contentScale = ContentScale.Fit,
            modifier = modifier
                .size(size)
                .clip(CircleShape)
                .background(Color.White)
                .border(1.dp, Color(0xFFEEEEEE), CircleShape)
        )
    } else {
        // Fallback to clearbit
        val domain = when (imageCode) {
            "sbi" -> "sbi.co.in"
            "hdfc" -> "hdfcbank.com"
            "icici" -> "icicibank.com"
            "pnb" -> "pnbindia.in"
            "bob" -> "bankofbaroda.in"
            "axis" -> "axisbank.com"
            "paytm" -> "paytmbank.com"
            "union" -> "unionbankofindia.co.in"
            "canara" -> "canarabank.com"
            "kotak" -> "kotak.com"
            "yes" -> "yesbank.in"
            "indusind" -> "indusind.com"
            "idfc" -> "idfcfirstbank.com"
            else -> null
        }
        
        if (domain != null) {
            val logoUrl = "https://logo.clearbit.com/$domain"
            AsyncImage(
                model = ImageRequest.Builder(LocalContext.current)
                    .data(logoUrl)
                    .crossfade(true)
                    .build(),
                contentDescription = bankName,
                contentScale = ContentScale.Fit,
                modifier = modifier
                    .size(size)
                    .clip(CircleShape)
                    .background(Color.White)
                    .border(1.dp, Color(0xFFEEEEEE), CircleShape)
                    .padding(4.dp)
            )
        } else {
            Box(
                modifier = modifier
                    .size(size)
                    .background(Color.White, CircleShape)
                    .border(1.dp, Color(0xFFEEEEEE), CircleShape),
                contentAlignment = Alignment.Center
            ) {
                Icon(Icons.Default.AccountBalance, contentDescription = null, tint = Color(0xFF1976D2), modifier = Modifier.size(size * 0.6f))
            }
        }
    }
}
"""

content = re.sub(
    r'@Composable\s*fun BankLogo\(bankName: String, size: Dp = 40.dp\) \{.*',
    new_logic,
    content,
    flags=re.DOTALL
)

with open('/app/applet/app/src/main/java/com/example/ui/components/BankLogo.kt', 'w') as f:
    f.write(content)

