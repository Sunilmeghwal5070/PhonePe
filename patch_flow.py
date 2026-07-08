import re

def fix_file(path):
    with open(path, 'r') as f:
        content = f.read()

    # Add import
    if 'import androidx.compose.runtime.collectAsState' not in content:
        content = content.replace('import androidx.compose.runtime.*', 'import androidx.compose.runtime.*\nimport androidx.compose.runtime.collectAsState')

    # Change transactions to allTransactions
    content = content.replace('viewModel.transactions.collectAsState()', 'viewModel.allTransactions.collectAsState()')

    with open(path, 'w') as f:
        f.write(content)

fix_file('/app/applet/app/src/main/java/com/example/ui/screens/ChatScreen.kt')
fix_file('/app/applet/app/src/main/java/com/example/ui/screens/SendMoneyScreen.kt')
