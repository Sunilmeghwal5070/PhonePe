import re

with open('/app/applet/app/src/main/java/com/example/ui/screens/BankAccountsScreen.kt', 'r') as f:
    content = f.read()

box_canvas_pattern = r'Box\(\s*modifier = Modifier\s*\.size\(40\.dp\)\s*\.border\(1\.dp,\s*Color\(0xFFEEEEEE\),\s*RoundedCornerShape\(8\.dp\)\),\s*contentAlignment = Alignment\.Center\s*\)\s*\{\s*Canvas.*?\}\s*\}'

replacement = '''Box(
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
                    }'''

content = re.sub(box_canvas_pattern, replacement, content, flags=re.DOTALL)

if 'import coil.compose.AsyncImage' not in content:
    content = content.replace('import androidx.compose.runtime.*', 'import androidx.compose.runtime.*\nimport coil.compose.AsyncImage\nimport androidx.compose.ui.draw.clip')

with open('/app/applet/app/src/main/java/com/example/ui/screens/BankAccountsScreen.kt', 'w') as f:
    f.write(content)

