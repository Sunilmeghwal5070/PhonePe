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
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.FlashOn
import androidx.compose.material.icons.filled.Image
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalLifecycleOwner
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.core.content.ContextCompat
import com.google.mlkit.vision.barcode.BarcodeScanning
import com.google.mlkit.vision.barcode.common.Barcode
import com.google.mlkit.vision.common.InputImage
import java.util.concurrent.Executors

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ScannerScreen(onBack: () -> Unit, onScanSuccess: (String, String) -> Unit) {
    val context = LocalContext.current
    val lifecycleOwner = LocalLifecycleOwner.current
    var hasCamPermission by remember { mutableStateOf(ContextCompat.checkSelfPermission(context, Manifest.permission.CAMERA) == android.content.pm.PackageManager.PERMISSION_GRANTED) }

    val launcher = rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
        hasCamPermission = granted
    }

    LaunchedEffect(Unit) {
        if (!hasCamPermission) {
            launcher.launch(Manifest.permission.CAMERA)
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Scan any QR code", color = Color.White) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = Color.White)
                    }
                },
                actions = {
                    IconButton(onClick = { }) {
                        Icon(Icons.Default.FlashOn, contentDescription = "Flash", tint = Color.White)
                    }
                    IconButton(onClick = { }) {
                        Icon(Icons.Default.Image, contentDescription = "Gallery", tint = Color.White)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.Transparent)
            )
        },
        containerColor = Color.Black
    ) { paddingValues ->
        Box(modifier = Modifier.fillMaxSize().padding(paddingValues)) {
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
                                                    if (url.startsWith("upi://pay")) {
                                                        val uri = Uri.parse(url)
                                                        val name = uri.getQueryParameter("pn") ?: "Unknown"
                                                        val upi = uri.getQueryParameter("pa") ?: "unknown@upi"
                                                        // Stop analysis after first success to prevent multiple triggers
                                                        imageAnalysis.clearAnalyzer()
                                                        onScanSuccess(name, upi)
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
            } else {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Text("Camera permission required", color = Color.White)
                }
            }

            // Scanner Overlay
            Canvas(modifier = Modifier.fillMaxSize()) {
                val boxSize = 250.dp.toPx()
                val cornerLength = 40.dp.toPx()
                val strokeWidth = 4.dp.toPx()
                
                val left = (size.width - boxSize) / 2
                val top = (size.height - boxSize) / 2
                
                // Draw semi-transparent background outside the scanner box
                drawRect(color = Color(0x88000000), size = size)
                drawRect(color = Color.Transparent, topLeft = Offset(left, top), size = Size(boxSize, boxSize), blendMode = androidx.compose.ui.graphics.BlendMode.Clear)

                // Top-Left Corner
                drawLine(Color.White, Offset(left, top), Offset(left + cornerLength, top), strokeWidth)
                drawLine(Color.White, Offset(left, top), Offset(left, top + cornerLength), strokeWidth)

                // Top-Right Corner
                drawLine(Color.White, Offset(left + boxSize, top), Offset(left + boxSize - cornerLength, top), strokeWidth)
                drawLine(Color.White, Offset(left + boxSize, top), Offset(left + boxSize, top + cornerLength), strokeWidth)

                // Bottom-Left Corner
                drawLine(Color.White, Offset(left, top + boxSize), Offset(left + cornerLength, top + boxSize), strokeWidth)
                drawLine(Color.White, Offset(left, top + boxSize), Offset(left, top + boxSize - cornerLength), strokeWidth)

                // Bottom-Right Corner
                drawLine(Color.White, Offset(left + boxSize, top + boxSize), Offset(left + boxSize - cornerLength, top + boxSize), strokeWidth)
                drawLine(Color.White, Offset(left + boxSize, top + boxSize), Offset(left + boxSize, top + boxSize - cornerLength), strokeWidth)
            }
            
            Column(
                modifier = Modifier.align(Alignment.BottomCenter).padding(bottom = 64.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Text("Scan any QR code to pay", color = Color.White, fontSize = 16.sp)
                Spacer(modifier = Modifier.height(16.dp))
                // FAKE SCAN BUTTON for Emulator
                Button(onClick = { onScanSuccess("Sunil Meghwal", "sunil@ybl") }) {
                    Text("Simulate Scan (Emulator)")
                }
            }
        }
    }
}
