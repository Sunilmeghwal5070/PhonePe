import re

with open('app/src/main/java/com/example/ui/screens/RechargeFlowScreens.kt', 'r') as f:
    content = f.read()

# Fix properties
content = content.replace("currentTx.customTxId", "currentTx.transactionId")
content = content.replace("currentTx.senderBankLast4", "currentTx.senderBankAccountLast4")
content = content.replace("currentTx.customUtr", "currentTx.utr")

# Add imports
imports = """import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.animation.AnimatedVisibility
"""

if "import androidx.compose.animation.AnimatedVisibility" not in content:
    content = content.replace("import androidx.compose.animation.core.*", "import androidx.compose.animation.core.*\n" + imports)


# Oh wait, `PrankViewModel.insertTransaction` signature!
# I passed customTxId and customUtr, but does it expect customTxId or transactionId?
# Let's check `PrankViewModel.kt` insertTransaction signature.
