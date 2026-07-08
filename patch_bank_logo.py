import re

def replace_logo(filepath, pattern, replacement):
    with open(filepath, 'r') as f:
        content = f.read()
    if 'import com.example.ui.components.BankLogo' not in content:
        content = content.replace('import androidx.compose.material3.*', 'import androidx.compose.material3.*\nimport com.example.ui.components.BankLogo')
    
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    with open(filepath, 'w') as f:
        f.write(content)

# BankAccountsScreen.kt
p1 = r'''Box\(\s*modifier = Modifier\s*\.size\(40\.dp\)\s*\.border\(1\.dp, Color\(0xFFEEEEEE\), CircleShape\),\s*contentAlignment = Alignment\.Center\s*\)\s*\{\s*Icon\(Icons\.Default\.AccountBalance, contentDescription = null, tint = Color\(0xFF1976D2\), modifier = Modifier\.size\(24\.dp\)\)\s*\}'''
r1 = '''BankLogo(account.bankName)'''
replace_logo('/app/applet/app/src/main/java/com/example/ui/screens/BankAccountsScreen.kt', p1, r1)

# CheckBalanceScreen.kt
p2 = r'''Box\(\s*modifier = Modifier\s*\.size\(40\.dp\)\s*\.border\(1\.dp, Color\(0xFFEEEEEE\), CircleShape\),\s*contentAlignment = Alignment\.Center\s*\)\s*\{\s*Icon\(Icons\.Default\.AccountBalance, contentDescription = null, tint = Color\(0xFF1976D2\), modifier = Modifier\.size\(24\.dp\)\)\s*\}'''
r2 = '''BankLogo(account.bankName)'''
replace_logo('/app/applet/app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt', p2, r2)

