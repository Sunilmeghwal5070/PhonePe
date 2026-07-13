package com.example.ui.screens

import android.Manifest
import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.camera.core.CameraSelector
import androidx.camera.core.ImageAnalysis
import androidx.camera.core.Preview
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.camera.view.PreviewView
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.outlined.HelpOutline
import androidx.compose.material.icons.outlined.Image
import androidx.compose.material.icons.outlined.FlashlightOn
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.RoundRect
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.BlendMode
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.clipPath
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalLifecycleOwner
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.core.content.ContextCompat
import com.google.mlkit.vision.barcode.BarcodeScanning
import com.google.mlkit.vision.barcode.common.Barcode
import com.google.mlkit.vision.common.InputImage
import java.util.concurrent.Executors

import androidx.compose.ui.graphics.graphicsLayer

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ScannerScreen(onBack: () -> Unit, onScanSuccess: (String, String) -> Unit) {
    val context = LocalContext.current
    val lifecycleOwner = LocalLifecycleOwner.current
    var hasCamPermission by remember { mutableStateOf(ContextCompat.checkSelfPermission(context, Manifest.permission.CAMERA) == android.content.pm.PackageManager.PERMISSION_GRANTED) }

    val launcher = rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
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
    }

    LaunchedEffect(Unit) {
        if (!hasCamPermission) {
            launcher.launch(Manifest.permission.CAMERA)
        }
    }

    Box(modifier = Modifier.fillMaxSize().background(Color.Black)) {
        if (hasCamPermission) {
            AndroidView(
                factory = { ctx ->
                    val previewView = PreviewView(ctx)
                    val cameraProviderFuture = ProcessCameraProvider.getInstance(ctx)
                    val executor = Executors.newSingleThreadExecutor()

                    cameraProviderFuture.addListener({
                        val cameraProvider = cameraProviderFuture.get()
                        val preview = Preview.Builder().build().also {
                            it.setSurfaceProvider(previewView.surfaceProvider)
                        }

                        val imageAnalysis = ImageAnalysis.Builder()
                            .setBackpressureStrategy(ImageAnalysis.STRATEGY_KEEP_ONLY_LATEST)
                            .build()

                        val scanner = BarcodeScanning.getClient()

                        imageAnalysis.setAnalyzer(executor) { imageProxy ->
                            val mediaImage = imageProxy.image
                            if (mediaImage != null) {
                                val image = InputImage.fromMediaImage(mediaImage, imageProxy.imageInfo.rotationDegrees)
                                scanner.process(image)
                                    .addOnSuccessListener { barcodes ->
                                        for (barcode in barcodes) {
                                            if (barcode.valueType == Barcode.TYPE_URL || barcode.valueType == Barcode.TYPE_TEXT) {
                                                val url = barcode.rawValue ?: continue
                                                val cleanUrl = url.trim()
                                                if (cleanUrl.lowercase().startsWith("upi://pay")) {
                                                    val uri = Uri.parse(cleanUrl)
                                                    val name = uri.getQueryParameter("pn") ?: uri.getQueryParameter("pa") ?: "Unknown"
                                                    val upi = uri.getQueryParameter("pa") ?: uri.getQueryParameter("pn") ?: "unknown@upi"
                                                    imageAnalysis.clearAnalyzer()
                                                    onScanSuccess(name, upi)
                                                    break
                                                } else if (cleanUrl.contains("@")) {
                                                    imageAnalysis.clearAnalyzer()
                                                    onScanSuccess(cleanUrl, cleanUrl)
                                                    break
                                                }
                                            }
                                        }
                                    }
                                    .addOnCompleteListener {
                                        imageProxy.close()
                                    }
                            } else {
                                imageProxy.close()
                            }
                        }

                        try {
                            cameraProvider.unbindAll()
                            cameraProvider.bindToLifecycle(
                                lifecycleOwner,
                                CameraSelector.DEFAULT_BACK_CAMERA,
                                preview,
                                imageAnalysis
                            )
                        } catch (e: Exception) {
                            e.printStackTrace()
                        }
                    }, ContextCompat.getMainExecutor(ctx))

                    previewView
                },
                modifier = Modifier.fillMaxSize()
            )
        }

        // Overlay & UI
        Box(modifier = Modifier.fillMaxSize()) {
            Canvas(modifier = Modifier.fillMaxSize().graphicsLayer(alpha = 0.99f)) {
                val boxSize = 280.dp.toPx()
                val cornerRadius = 24.dp.toPx()
                val left = (size.width - boxSize) / 2
                val top = (size.height - boxSize) / 2 - 60.dp.toPx()

                // Draw semi-transparent dark background
                drawRect(color = Color(0x66000000), size = size)
                
                // Clear the center rounded rectangle
                val clearPath = Path().apply {
                    addRoundRect(
                        RoundRect(
                            left = left,
                            top = top,
                            right = left + boxSize,
                            bottom = top + boxSize,
                            cornerRadius = CornerRadius(cornerRadius, cornerRadius)
                        )
                    )
                }
                drawPath(path = clearPath, color = Color.Transparent, blendMode = BlendMode.Clear)

                // Draw purple corners
                val cornerLength = 40.dp.toPx()
                val strokeWidth = 4.dp.toPx()
                val cornerColor = Color(0xFF9032E6) // PhonePe Purple
                
                // Top-Left Corner
                val tlPath = Path().apply {
                    moveTo(left, top + cornerLength)
                    lineTo(left, top + cornerRadius)
                    quadraticBezierTo(left, top, left + cornerRadius, top)
                    lineTo(left + cornerLength, top)
                }
                drawPath(tlPath, cornerColor, style = Stroke(width = strokeWidth))

                // Top-Right Corner
                val trPath = Path().apply {
                    moveTo(left + boxSize - cornerLength, top)
                    lineTo(left + boxSize - cornerRadius, top)
                    quadraticBezierTo(left + boxSize, top, left + boxSize, top + cornerRadius)
                    lineTo(left + boxSize, top + cornerLength)
                }
                drawPath(trPath, cornerColor, style = Stroke(width = strokeWidth))

                // Bottom-Left Corner
                val blPath = Path().apply {
                    moveTo(left, top + boxSize - cornerLength)
                    lineTo(left, top + boxSize - cornerRadius)
                    quadraticBezierTo(left, top + boxSize, left + cornerRadius, top + boxSize)
                    lineTo(left + cornerLength, top + boxSize)
                }
                drawPath(blPath, cornerColor, style = Stroke(width = strokeWidth))

                // Bottom-Right Corner
                val brPath = Path().apply {
                    moveTo(left + boxSize, top + boxSize - cornerLength)
                    lineTo(left + boxSize, top + boxSize - cornerRadius)
                    quadraticBezierTo(left + boxSize, top + boxSize, left + boxSize - cornerRadius, top + boxSize)
                    lineTo(left + boxSize - cornerLength, top + boxSize)
                }
                drawPath(brPath, cornerColor, style = Stroke(width = strokeWidth))
            }

            // Top Bar
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 48.dp, start = 16.dp, end = 16.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                IconButton(onClick = onBack) {
                    Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.White)
                }
                Spacer(modifier = Modifier.width(8.dp))
                Column(modifier = Modifier.weight(1f)) {
                    Text("Scan any QR", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.SemiBold)
                    Text("PhonePe • Google Pay • BHIM • Paytm", color = Color(0xFFCCCCCC), fontSize = 12.sp)
                }
                IconButton(onClick = { }) {
                    Icon(Icons.Outlined.HelpOutline, contentDescription = "Help", tint = Color.White)
                }
            }

            // Buttons below scanner
            Row(
                modifier = Modifier
                    .align(Alignment.Center)
                    .offset(y = 160.dp)
                    .fillMaxWidth(),
                horizontalArrangement = Arrangement.Center
            ) {
                Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.padding(horizontal = 24.dp)) {
                    Box(
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
                    }
                    Spacer(modifier = Modifier.height(12.dp))
                    Text("Torch", color = Color.White, fontSize = 13.sp)
                }
            }

            // Bottom Logo
            Column(
                modifier = Modifier
                    .align(Alignment.BottomCenter)
                    .padding(bottom = 32.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                
                
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("BHIM", color = Color.White.copy(alpha = 0.7f), fontSize = 18.sp, fontWeight = FontWeight.Bold, fontStyle = androidx.compose.ui.text.font.FontStyle.Italic)
                    Text(" | ", color = Color.White.copy(alpha = 0.5f), fontSize = 18.sp)
                    Text("UPI", color = Color.White.copy(alpha = 0.7f), fontSize = 18.sp, fontWeight = FontWeight.Bold, fontStyle = androidx.compose.ui.text.font.FontStyle.Italic)
                }
                Text("BHARAT INTERFACE FOR MONEY     UNIFIED PAYMENTS INTERFACE", color = Color.White.copy(alpha = 0.3f), fontSize = 6.sp, letterSpacing = 1.sp)
            }
        }
    }
}
