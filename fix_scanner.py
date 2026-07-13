import re

with open('app/src/main/java/com/example/ui/screens/ScannerScreen.kt', 'r') as f:
    text = f.read()

target_top = """import androidx.compose.ui.geometry.RoundRect
import androidx.compose.ui.graphics.BlendMode
import androidx.compose.ui.graphics.Color"""

replacement_top = """import androidx.compose.ui.geometry.RoundRect
import androidx.compose.ui.graphics.BlendMode
import androidx.compose.ui.graphics.Color
import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import com.google.mlkit.vision.common.InputImage
import java.io.IOException"""

text = text.replace(target_top, replacement_top)

target_camera = """                                imageAnalysis
                            )
                        } catch (e: Exception) {
                            e.printStackTrace()
                        }
                    }, ContextCompat.getMainExecutor(ctx))
                    previewView
                },
                modifier = Modifier.fillMaxSize()
            )"""

replacement_camera = """                                imageAnalysis
                            )
                            cameraRef.value = camera
                        } catch (e: Exception) {
                            e.printStackTrace()
                        }
                    }, ContextCompat.getMainExecutor(ctx))
                    previewView
                },
                modifier = Modifier.fillMaxSize()
            )"""

text = text.replace(target_camera, replacement_camera)

target_state = """    var hasCamPermission by remember { mutableStateOf(
        ContextCompat.checkSelfPermission(context, Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED
    ) }
    val launcher = rememberLauncherForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { isGranted ->
        hasCamPermission = isGranted
    }"""

replacement_state = """    var hasCamPermission by remember { mutableStateOf(
        ContextCompat.checkSelfPermission(context, Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED
    ) }
    val launcher = rememberLauncherForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { isGranted ->
        hasCamPermission = isGranted
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
                            Toast.makeText(context, "No valid UPI QR found", Toast.LENGTH_SHORT).show()
                        }
                    }
                    .addOnFailureListener {
                        Toast.makeText(context, "Failed to scan image", Toast.LENGTH_SHORT).show()
                    }
            } catch (e: IOException) {
                e.printStackTrace()
            }
        }
    }"""

text = text.replace(target_state, replacement_state)

target_buttons = """                    Box(
                        modifier = Modifier
                            .size(52.dp)
                            .background(Color(0x66000000), CircleShape)
                            .clickable { },
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(Icons.Outlined.Image, contentDescription = "Upload QR", tint = Color.White)
                    }
                    Spacer(modifier = Modifier.height(12.dp))
                    Text("Upload QR", color = Color.White, fontSize = 13.sp)
                }
                
                Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.padding(horizontal = 24.dp)) {
                    Box(
                        modifier = Modifier
                            .size(52.dp)
                            .background(Color(0x66000000), CircleShape)
                            .clickable { },
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(Icons.Outlined.FlashlightOn, contentDescription = "Torch", tint = Color.White)
                    }"""

replacement_buttons = """                    Box(
                        modifier = Modifier
                            .size(52.dp)
                            .background(Color(0x66000000), CircleShape)
                            .clickable { imagePickerLauncher.launch("image/*") },
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(Icons.Outlined.Image, contentDescription = "Upload QR", tint = Color.White)
                    }
                    Spacer(modifier = Modifier.height(12.dp))
                    Text("Upload QR", color = Color.White, fontSize = 13.sp)
                }
                
                Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.padding(horizontal = 24.dp)) {
                    Box(
                        modifier = Modifier
                            .size(52.dp)
                            .background(if (isTorchOn) Color(0x99FFFFFF) else Color(0x66000000), CircleShape)
                            .clickable {
                                isTorchOn = !isTorchOn
                                cameraRef.value?.cameraControl?.enableTorch(isTorchOn)
                            },
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(Icons.Outlined.FlashlightOn, contentDescription = "Torch", tint = if (isTorchOn) Color.Black else Color.White)
                    }"""

text = text.replace(target_buttons, replacement_buttons)

with open('app/src/main/java/com/example/ui/screens/ScannerScreen.kt', 'w') as f:
    f.write(text)
