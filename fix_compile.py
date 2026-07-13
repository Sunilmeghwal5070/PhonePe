import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    text = f.read()

# Fix double Toast import
text = text.replace("import android.widget.Toast\nimport androidx.activity.enableEdgeToEdge", "import androidx.activity.enableEdgeToEdge")

# Fix double context declaration
text = text.replace("    val allTransactions by prankViewModel.allTransactions.collectAsState()\n    val context = androidx.compose.ui.platform.LocalContext.current", "    val allTransactions by prankViewModel.allTransactions.collectAsState()")

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(text)
