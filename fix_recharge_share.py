import re

with open('app/src/main/java/com/example/ui/screens/RechargeFlowScreens.kt', 'r') as f:
    text = f.read()

# Add view
text = text.replace("    var paymentExpanded by remember { mutableStateOf(false) }", "    var paymentExpanded by remember { mutableStateOf(false) }\n    val context = androidx.compose.ui.platform.LocalContext.current\n    val view = androidx.compose.ui.platform.LocalView.current.rootView")

share_fn = """    fun shareTransaction() {
        try {
            val bitmap = android.graphics.Bitmap.createBitmap(view.width, view.height, android.graphics.Bitmap.Config.ARGB_8888)
            val canvas = android.graphics.Canvas(bitmap)
            view.draw(canvas)
            
            val file = java.io.File(context.cacheDir, "receipt_${System.currentTimeMillis()}.png")
            val out = java.io.FileOutputStream(file)
            bitmap.compress(android.graphics.Bitmap.CompressFormat.PNG, 100, out)
            out.flush()
            out.close()
            
            val uri = androidx.core.content.FileProvider.getUriForFile(context, "${context.packageName}.provider", file)
            val intent = android.content.Intent(android.content.Intent.ACTION_SEND).apply {
                type = "image/png"
                putExtra(android.content.Intent.EXTRA_STREAM, uri)
                addFlags(android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION)
            }
            context.startActivity(android.content.Intent.createChooser(intent, "Share Receipt Via"))
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
"""

if "fun shareTransaction()" not in text:
    text = text.replace("    Scaffold(", share_fn + "\n    Scaffold(")

# modify ActionItem to accept onClick
text = text.replace("fun ActionItem(icon: androidx.compose.ui.graphics.vector.ImageVector, text: String) {", "fun ActionItem(icon: androidx.compose.ui.graphics.vector.ImageVector, text: String, onClick: () -> Unit = {}) {")

# modify Column in ActionItem to have clickable
text = text.replace("Column(horizontalAlignment = Alignment.CenterHorizontally) {", "Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.clickable { onClick() }) {")

# add onClick to the actions
target = """                        ActionItem(icon = Icons.Default.Schedule, text = "View\\nHistory")
                        ActionItem(icon = Icons.AutoMirrored.Filled.CallMade, text = "Recharge\\nAgain")
                        ActionItem(icon = Icons.Default.CallSplit, text = "Split\\nExpense")
                        ActionItem(icon = Icons.Default.Share, text = "Share\\nReceipt")"""
replacement = """                        ActionItem(icon = Icons.Default.Schedule, text = "View\\nHistory", onClick = onDone)
                        ActionItem(icon = Icons.AutoMirrored.Filled.CallMade, text = "Recharge\\nAgain", onClick = onDone)
                        ActionItem(icon = Icons.Default.CallSplit, text = "Split\\nExpense")
                        ActionItem(icon = Icons.Default.Share, text = "Share\\nReceipt", onClick = { shareTransaction() })"""
text = text.replace(target, replacement)

with open('app/src/main/java/com/example/ui/screens/RechargeFlowScreens.kt', 'w') as f:
    f.write(text)
