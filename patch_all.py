import re

# Fix MainActivity.kt
with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    main_content = f.read()

main_content = main_content.replace(
'''            composable("check_balance") {
                CheckBalanceScreen(onBack = { navController.popBackStack() })
            }''',
'''            composable("check_balance") {
                CheckBalanceScreen(viewModel = prankViewModel, onBack = { navController.popBackStack() })
            }''')

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(main_content)

# Fix CreatePrankScreen.kt
with open('/app/applet/app/src/main/java/com/example/ui/screens/CreatePrankScreen.kt', 'r') as f:
    prank_content = f.read()

if 'import android.widget.Toast' not in prank_content:
    prank_content = prank_content.replace('import androidx.compose.ui.platform.LocalContext', 'import androidx.compose.ui.platform.LocalContext\nimport android.widget.Toast')

with open('/app/applet/app/src/main/java/com/example/ui/screens/CreatePrankScreen.kt', 'w') as f:
    f.write(prank_content)

# Fix CheckBalanceScreen.kt
with open('/app/applet/app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt', 'r') as f:
    cb_content = f.read()

# Move imports
cb_content = cb_content.replace('''enum class CheckBalanceState {
    LIST,
    PIN,
    LOADING,
    SUCCESS
}

import com.example.ui.PrankViewModel
import com.example.ui.BankAccount
import androidx.compose.runtime.collectAsState
import android.widget.Toast
import androidx.compose.ui.platform.LocalContext''', 
'''import com.example.ui.PrankViewModel
import com.example.ui.BankAccount
import androidx.compose.runtime.collectAsState
import android.widget.Toast
import androidx.compose.ui.platform.LocalContext

enum class CheckBalanceState {
    LIST,
    PIN,
    LOADING,
    SUCCESS
}''')

# Fix literal newline in string
cb_content = cb_content.replace('''text = "Available Balance fetched
successful",''', '''text = "Available Balance fetched\\nsuccessful",''')

with open('/app/applet/app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt', 'w') as f:
    f.write(cb_content)

