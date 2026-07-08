with open('app/src/main/java/com/example/ui/screens/RechargeFlowScreens.kt', 'r') as f:
    content = f.read()

content = content.replace("currentTx.customTxId", "currentTx.transactionId")
content = content.replace("currentTx.senderBankLast4", "currentTx.senderBankAccountLast4")
content = content.replace("currentTx.customUtr", "currentTx.utr")

imports = """import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.animation.AnimatedVisibility"""

if "import androidx.compose.animation.AnimatedVisibility" not in content:
    content = content.replace("import androidx.compose.animation.AnimatedContent", imports + "\\nimport androidx.compose.animation.AnimatedContent")

with open('app/src/main/java/com/example/ui/screens/RechargeFlowScreens.kt', 'w') as f:
    f.write(content)
