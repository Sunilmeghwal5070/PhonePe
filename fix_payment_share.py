import re

with open('app/src/main/java/com/example/ui/screens/PaymentSuccessScreen.kt', 'r') as f:
    text = f.read()

# Add view
text = text.replace("    val context = LocalContext.current", "    val context = LocalContext.current\n    val view = androidx.compose.ui.platform.LocalView.current.rootView")

old_share = """    val onShare = {
        val shareMsg = \"\"\"
            *PhonePe Transaction Receipt*
            ----------------------------------
            Status: SUCCESS
            Paid To: $payeeName
            UPI ID: $upiId
            Amount: Rs. $amount
            Bank: $bankName
            ----------------------------------
            Shared via PhonePe
        \"\"\".trimIndent()
        val intent = Intent(Intent.ACTION_SEND).apply {
            type = "text/plain"
            putExtra(Intent.EXTRA_TEXT, shareMsg)
        }
        context.startActivity(Intent.createChooser(intent, "Share Receipt"))
    }"""

new_share = """    val onShare = {
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
    }"""

text = text.replace(old_share, new_share)

with open('app/src/main/java/com/example/ui/screens/PaymentSuccessScreen.kt', 'w') as f:
    f.write(text)
