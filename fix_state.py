import re

with open('app/src/main/java/com/example/ui/screens/ScannerScreen.kt', 'r') as f:
    text = f.read()

target = """    val launcher = rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
        hasCamPermission = granted
    }"""

replacement = """    val launcher = rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
        hasCamPermission = granted
    }
    
    val cameraRef = remember { mutableStateOf<androidx.camera.core.Camera?>(null) }
    var isTorchOn by remember { mutableStateOf(false) }

    val imagePickerLauncher = rememberLauncherForActivityResult(ActivityResultContracts.GetContent()) { uri: Uri? ->
        if (uri != null) {
            try {
                val image = InputImage.fromFilePath(context, uri)
                val scanner = BarcodeScanning.getClient()
                scanner.process(image)
                    .addOnSuccessListener { barcodes ->
                        var found = false
                        for (barcode in barcodes) {
                            if (barcode.valueType == Barcode.TYPE_URL || barcode.valueType == Barcode.TYPE_TEXT) {
                                val url = barcode.rawValue ?: continue
                                val cleanUrl = url.trim()
                                if (cleanUrl.lowercase().startsWith("upi://pay")) {
                                    val parsedUri = Uri.parse(cleanUrl)
                                    val name = parsedUri.getQueryParameter("pn") ?: "Unknown"
                                    val upi = parsedUri.getQueryParameter("pa") ?: "unknown@upi"
                                    onScanSuccess(name, upi)
                                    found = true
                                    break
                                }
                            }
                        }
                        if (!found) {
                            android.widget.Toast.makeText(context, "No valid UPI QR found", android.widget.Toast.LENGTH_SHORT).show()
                        }
                    }
                    .addOnFailureListener {
                        android.widget.Toast.makeText(context, "Failed to scan image", android.widget.Toast.LENGTH_SHORT).show()
                    }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }"""

text = text.replace(target, replacement)

with open('app/src/main/java/com/example/ui/screens/ScannerScreen.kt', 'w') as f:
    f.write(text)
