package com.example.ui.screens

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import kotlinx.coroutines.withContext
import com.example.BuildConfig

import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Key
import androidx.compose.material3.*
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.ui.PrefsManager
import com.example.ui.theme.PhonePePurple
import com.google.firebase.firestore.FirebaseFirestore

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ActivationScreen(prefsManager: PrefsManager, onActivated: () -> Unit) {
    var keyInput by remember { mutableStateOf("") }
    var userNameInput by remember { mutableStateOf("") }
    var errorMessage by remember { mutableStateOf("") }
    var isLoading by remember { mutableStateOf(false) }
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var freeTrialUrl by remember { mutableStateOf("https://gplinks.com/") }

    LaunchedEffect(Unit) {
        scope.launch {
            try {
                val apiKey = BuildConfig.FIREBASE_API_KEY
                val projectId = BuildConfig.FIREBASE_PROJECT_ID
                
                if (apiKey.isNotEmpty() && !apiKey.contains("YOUR_API_KEY")) {
                    val client = OkHttpClient()
                    val getUrl = "https://firestore.googleapis.com/v1/projects/$projectId/databases/(default)/documents/app_settings/urls?key=$apiKey"
                    val request = Request.Builder().url(getUrl).build()
                    
                    val response = withContext(Dispatchers.IO) {
                        client.newCall(request).execute()
                    }
                    
                    val responseBody = response.body?.string() ?: ""
                    if (response.isSuccessful) {
                        val json = JSONObject(responseBody)
                        val fields = json.optJSONObject("fields")
                        val urlObj = fields?.optJSONObject("url_shortener") 
                            ?: fields?.optJSONObject("urlShortener") 
                            ?: fields?.optJSONObject("freeTrialUrl") 
                            ?: fields?.optJSONObject("url")
                        val url = urlObj?.optString("stringValue") ?: ""
                        if (url.isNotEmpty()) {
                            freeTrialUrl = url
                        }
                    }
                }
            } catch (e: Exception) {}
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("App Activation", fontWeight = FontWeight.Bold, color = Color.White) },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = PhonePePurple)
            )
        },
        containerColor = Color(0xFFF5F5F5)
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Icon(Icons.Default.Key, contentDescription = null, tint = PhonePePurple, modifier = Modifier.size(80.dp))
            Spacer(modifier = Modifier.height(24.dp))
            
            Text("Enter Activation Key", fontSize = 24.sp, fontWeight = FontWeight.Bold, color = Color.Black)
            Spacer(modifier = Modifier.height(8.dp))
            Text("This app requires an activation key to proceed. A user can use a key only once.", fontSize = 14.sp, color = Color.Gray, textAlign = TextAlign.Center)
            
            Spacer(modifier = Modifier.height(32.dp))
            
                        OutlinedTextField(
                value = userNameInput,
                onValueChange = { 
                    userNameInput = it
                    if (errorMessage.isNotEmpty()) errorMessage = "" 
                },
                label = { Text("Your Name") },
                placeholder = { Text("Enter your full name") },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true,
                enabled = !isLoading,
                keyboardOptions = KeyboardOptions(
                    keyboardType = KeyboardType.Email,
                    autoCorrect = false
                )
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            OutlinedTextField(
                value = keyInput,
                onValueChange = { 
                    keyInput = it
                    if (errorMessage.isNotEmpty()) errorMessage = "" 
                },
                label = { Text("Activation Key") },
                placeholder = { Text("e.g. Ph-1299-RK") },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true,
                isError = errorMessage.isNotEmpty(),
                enabled = !isLoading,
                keyboardOptions = KeyboardOptions(
                    keyboardType = KeyboardType.Email,
                    autoCorrect = false
                )
            )
            
            if (errorMessage.isNotEmpty()) {
                Text(errorMessage, color = Color.Red, fontSize = 12.sp, modifier = Modifier.padding(top = 4.dp).align(Alignment.Start))
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            
            Button(
                onClick = {
                    if (userNameInput.isBlank()) {
                        errorMessage = "Please enter your name"
                        return@Button
                    }
                    if (keyInput.isBlank()) {
                        errorMessage = "Please enter a key"
                        return@Button
                    }
                    
                    isLoading = true
                    val isFirebaseInitialized = try {
                        com.google.firebase.FirebaseApp.getInstance() != null
                    } catch (e: Exception) {
                        false
                    }

                    if (isFirebaseInitialized) {
                        try {
                            val db = FirebaseFirestore.getInstance()
                            db.collection("activation_keys").document(keyInput).get()
                                .addOnSuccessListener { doc ->
                                    if (!doc.exists()) {
                                        errorMessage = "Key not found or invalid."
                                        isLoading = false
                                        return@addOnSuccessListener
                                    }
                                    val status = doc.getString("status")
                                    
                                    if (status == "UNUSED") {
                                        val type = doc.getString("type") ?: "PREMIUM"
                                        val validityHours = when (type) {
                                            "FREE_24" -> 24
                                            "FREE_48" -> 48
                                            else -> 28 * 24
                                        }
                                        val expiresAt = System.currentTimeMillis() + validityHours * 60 * 60 * 1000L
                                        
                                        doc.reference.update(
                                            mapOf(
                                                "status" to "ACTIVE",
                                                "activatedAt" to System.currentTimeMillis(),
                                                "expiresAt" to expiresAt,
                                                "userName" to userNameInput
                                            )
                                        ).addOnSuccessListener {
                                            prefsManager.saveActivation(keyInput, expiresAt, userNameInput)
                                            isLoading = false
                                            onActivated()
                                        }.addOnFailureListener {
                                            errorMessage = "Failed to activate key. Please try again."
                                            isLoading = false
                                        }
                                    } else {
                                        errorMessage = when (status) {
                                            "ACTIVE" -> "Key is already active on another device."
                                            "EXPIRED" -> "Key is expired."
                                            "BLOCKED" -> "Key is blocked by admin."
                                            else -> "Invalid key status."
                                        }
                                        isLoading = false
                                    }
                                }
                                .addOnFailureListener {
                                    errorMessage = "Error: ${it.message}"
                                    isLoading = false
                                }
                        } catch (e: Exception) {
                            errorMessage = "Firebase error: ${e.message}"
                            isLoading = false
                        }
                    } else {
                        // Fallback to local validation if Firebase is not configured
                        if (keyInput.matches(Regex("Ph-\\d{4}-[A-Z]{2}"))) {
                            val expiryTime = if (keyInput.endsWith("FR")) {
                                System.currentTimeMillis() + 24 * 60 * 60 * 1000L
                            } else {
                                System.currentTimeMillis() + 28L * 24 * 60 * 60 * 1000L
                            }
                            prefsManager.saveActivation(keyInput, expiryTime, userNameInput)
                            isLoading = false
                            onActivated()
                        } else {
                            errorMessage = "Invalid Key format. Please use a valid key."
                            isLoading = false
                        }
                    }
                },
                modifier = Modifier.fillMaxWidth().height(52.dp),
                colors = ButtonDefaults.buttonColors(containerColor = PhonePePurple),
                shape = RoundedCornerShape(26.dp),
                enabled = !isLoading
            ) {
                if (isLoading) {
                    CircularProgressIndicator(color = Color.White, modifier = Modifier.size(24.dp))
                } else {
                    Text("SUBMIT", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.White)
                }
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            
            Text("Don't have a key?", color = Color.Gray)
            TextButton(onClick = {
                val intent = Intent(Intent.ACTION_VIEW, Uri.parse(freeTrialUrl))
                context.startActivity(intent)
            }) {
                Text("Get Free 24-Hour Trial Key", color = PhonePePurple, fontWeight = FontWeight.Bold)
            }
        }
    }
}
