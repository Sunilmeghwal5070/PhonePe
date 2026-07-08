import re
with open('app/src/main/java/com/example/ui/screens/HistoryScreen.kt', 'r') as f:
    content = f.read()

# Fix the broken classes
content = content.replace("import com.example.ui.ViewModel", "import com.example.ui.PrankViewModel")
content = content.replace("import com.example.data.Transaction", "import com.example.data.PrankTransaction")
content = content.replace("viewModel: ViewModel", "viewModel: PrankViewModel")
content = content.replace("List<Transaction>", "List<PrankTransaction>")
content = content.replace("tx: Transaction", "tx: PrankTransaction")
content = content.replace("fun ItemRow(", "fun PrankItemRow(")
content = content.replace("ItemRow(tx", "PrankItemRow(tx")
# What about "Recent Transactions" in HomeScreen? We replaced Prank there too but carefully.

with open('app/src/main/java/com/example/ui/screens/HistoryScreen.kt', 'w') as f:
    f.write(content)
