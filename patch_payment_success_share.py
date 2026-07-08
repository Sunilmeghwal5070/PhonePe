import re

with open("app/src/main/java/com/example/ui/screens/PaymentSuccessScreen.kt", "r") as f:
    content = f.read()

# Add imports
if "import android.graphics.Bitmap" not in content:
    content = content.replace("import androidx.compose.ui.platform.LocalContext", "import androidx.compose.ui.platform.LocalContext\nimport androidx.compose.ui.platform.LocalView\nimport android.graphics.Bitmap\nimport androidx.core.content.FileProvider\nimport android.content.Intent\nimport java.io.File\nimport java.io.FileOutputStream")

# Add sharing logic
logic = """
    val view = LocalView.current
    val onShare = {
        try {
            val bitmap = Bitmap.createBitmap(view.width, view.height, Bitmap.Config.ARGB_8888)
            val canvas = android.graphics.Canvas(bitmap)
            view.draw(canvas)
            
            val file = File(context.cacheDir, "receipt.png")
            val stream = FileOutputStream(file)
            bitmap.compress(Bitmap.CompressFormat.PNG, 100, stream)
            stream.close()
            
            val uri = FileProvider.getUriForFile(context, "${context.packageName}.provider", file)
            val intent = Intent(Intent.ACTION_SEND).apply {
                type = "image/png"
                putExtra(Intent.EXTRA_STREAM, uri)
                addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            }
            context.startActivity(Intent.createChooser(intent, "Share Receipt"))
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
"""

if "val infiniteTransition =" in content:
    content = content.replace("val infiniteTransition =", logic + "\n    val infiniteTransition =")

content = content.replace('onClick = { /* Share Receipt */ }', 'onClick = onShare')

with open("app/src/main/java/com/example/ui/screens/PaymentSuccessScreen.kt", "w") as f:
    f.write(content)
