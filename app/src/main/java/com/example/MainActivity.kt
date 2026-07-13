package com.example

import android.app.Application

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import kotlinx.coroutines.withContext
import android.os.Bundle
import com.google.firebase.firestore.FirebaseFirestore
import android.widget.Toast
import com.google.firebase.FirebaseApp
import android.net.Uri
import java.net.URLEncoder
import java.net.URLDecoder
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.outlined.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.foundation.clickable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.navArgument
import com.example.ui.PrankViewModel
import com.example.ui.PrankViewModelFactory
import com.example.ui.PrefsManager
import com.example.ui.screens.*
import com.example.ui.theme.MyApplicationTheme
import com.example.ui.theme.PhonePeDarkPurple
import com.example.ui.theme.PhonePeLightPurple
import com.example.ui.theme.PhonePePurple

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        com.example.ui.NotificationHelper.createNotificationChannel(this)
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.TIRAMISU) {
            if (androidx.core.content.ContextCompat.checkSelfPermission(this, android.Manifest.permission.POST_NOTIFICATIONS) != android.content.pm.PackageManager.PERMISSION_GRANTED) {
                androidx.core.app.ActivityCompat.requestPermissions(this, arrayOf(android.Manifest.permission.POST_NOTIFICATIONS), 101)
            }
        }
        
        com.example.ui.NotificationHelper.createNotificationChannel(this)
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.TIRAMISU) {
            if (androidx.core.content.ContextCompat.checkSelfPermission(this, android.Manifest.permission.POST_NOTIFICATIONS) != android.content.pm.PackageManager.PERMISSION_GRANTED) {
                androidx.core.app.ActivityCompat.requestPermissions(this, arrayOf(android.Manifest.permission.POST_NOTIFICATIONS), 101)
            }
        }
        
        try {
            if (com.google.firebase.FirebaseApp.getApps(this).isEmpty()) {
                val apiKey = BuildConfig.FIREBASE_API_KEY
                val appId = BuildConfig.FIREBASE_APP_ID
                val projectId = BuildConfig.FIREBASE_PROJECT_ID
                
                if (apiKey.isNotEmpty() && appId.isNotEmpty() && projectId.isNotEmpty() && !apiKey.contains("YOUR_API_KEY")) {
                    val options = com.google.firebase.FirebaseOptions.Builder()
                        .setApiKey(apiKey)
                        .setApplicationId(appId)
                        .setProjectId(projectId)
                        .build()
                    com.google.firebase.FirebaseApp.initializeApp(this, options)
                }
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }

        com.example.ui.UnityAdsManager.initialize(this)
        enableEdgeToEdge()
        setContent {
            MyApplicationTheme {
                MainAppLayout()
            }
        }
    }
}

@Composable
fun MainAppLayout() {
    val navController = rememberNavController()
    val context = LocalContext.current
    val application = context.applicationContext as Application
    
    // Initialize our PrankViewModel using custom factory
    val prankViewModel: PrankViewModel = viewModel(
        factory = PrankViewModelFactory(application)
    )

    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentRoute = navBackStackEntry?.destination?.route

    val permissionLauncher = androidx.activity.compose.rememberLauncherForActivityResult(
        androidx.activity.result.contract.ActivityResultContracts.RequestMultiplePermissions()
    ) { _ ->
        navController.navigate("qr") {
            popUpTo("home")
            launchSingleTop = true
            restoreState = true
        }
    }

    // Bottom Navigation only visible on Home, Search, QR, Alerts, and History screens

    val showBottomBar = currentRoute in listOf("home", "search", "qr", "alerts", "history")
    
    val isShakeEnabled by prankViewModel.isShakeEnabled.collectAsState()
    if (isShakeEnabled) {
        ShakeEffect {
            if (currentRoute != "qr") {
                navController.navigate("qr") {
                    popUpTo("home")
                    launchSingleTop = true
                    restoreState = true
                }
            }
        }
    }


    val prefsManager = remember { PrefsManager(context) }
    
    var showSplash by remember { mutableStateOf(true) }
    var isActivated by remember { mutableStateOf(prefsManager.isActivated()) }

    var isVerifying by remember { mutableStateOf(isActivated) }

    if (showSplash) {
        SplashScreen(onTimeout = { showSplash = false })
        return
    }

    if (isVerifying) {
        Box(modifier = Modifier.fillMaxSize().background(Color(0xFFF5F5F5)), contentAlignment = Alignment.Center) {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                CircularProgressIndicator(color = Color(0xFF5f259f))
                Spacer(modifier = Modifier.height(16.dp))
                Text("Verifying Key...", color = Color.Gray)
            }
        }

        LaunchedEffect(Unit) {
            kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.IO) {
                try {
                    val key = prefsManager.getActivationKey()
                    val apiKey = BuildConfig.FIREBASE_API_KEY
                    val projectId = BuildConfig.FIREBASE_PROJECT_ID
                    
                    if (key != null && apiKey.isNotEmpty() && !apiKey.contains("YOUR_API_KEY")) {
                        val client = okhttp3.OkHttpClient()
                        val getUrl = "https://firestore.googleapis.com/v1/projects/$projectId/databases/(default)/documents/activation_keys/$key?key=$apiKey"
                        val request = okhttp3.Request.Builder().url(getUrl).build()
                        
                        val response = client.newCall(request).execute()
                        val responseBody = response.body?.string() ?: ""
                        
                        if (response.isSuccessful) {
                            val json = org.json.JSONObject(responseBody)
                            val fields = json.optJSONObject("fields")
                            if (fields != null) {
                                val statusObj = fields.optJSONObject("status")
                                val status = statusObj?.optString("stringValue") ?: ""
                                if (status == "BLOCKED" || status == "EXPIRED") {
                                    prefsManager.saveActivation("", 0L)
                                    isActivated = false
                                }
                            } else {
                                prefsManager.saveActivation("", 0L)
                                isActivated = false
                            }
                        }
                    }
                } catch (e: Exception) {
                } finally {
                    isVerifying = false
                }
            }
        }
        return
    }

    if (!isActivated) {
        ActivationScreen(
            prefsManager = prefsManager,
            onActivated = { 
                isActivated = true 
                isVerifying = false
            }
        )
        return
    }
    
    val bankAccounts by prankViewModel.bankAccounts.collectAsState()
    val allTransactions by prankViewModel.allTransactions.collectAsState()

    var showDeactivationDialog by remember { mutableStateOf<String?>(null) }
    
    if (showDeactivationDialog != null) {
        androidx.compose.material3.AlertDialog(
            onDismissRequest = { 
                showDeactivationDialog = null
                prefsManager.saveActivation("", 0L)
                isActivated = false
            },
            title = { androidx.compose.material3.Text("Access Revoked") },
            text = { androidx.compose.material3.Text(showDeactivationDialog!!) },
            confirmButton = {
                androidx.compose.material3.TextButton(onClick = {
                    showDeactivationDialog = null
                    prefsManager.saveActivation("", 0L)
                    isActivated = false
                }) {
                    androidx.compose.material3.Text("OK")
                }
            }
        )
    }

    LaunchedEffect(isActivated) {
        if (isActivated) {
            val key = prefsManager.getActivationKey()
            if (!key.isNullOrEmpty()) {
                try {
                    if (FirebaseApp.getInstance() != null) {
                        val db = FirebaseFirestore.getInstance()
                        val registration = db.collection("activation_keys").document(key).addSnapshotListener { snapshot, error ->
                            if (error != null) return@addSnapshotListener
                            if (snapshot != null && snapshot.exists()) {
                                val status = snapshot.getString("status")
                                if (status == "BLOCKED" || status == "EXPIRED") {
                                    showDeactivationDialog = if (status == "BLOCKED") {
                                        "Your activation key has been blocked by the administrator."
                                    } else {
                                        "Your activation key has expired."
                                    }
                                }
                            }
                        }
                    }
                } catch(e: Exception) {}
            }
        }
    }
    

    Scaffold(
        bottomBar = {
            if (currentRoute in listOf("home", "search", "qr", "alerts", "history")) {
                Column(modifier = Modifier.background(Color.White).navigationBarsPadding()) {
                    Divider(color = Color(0xFFEEEEEE), thickness = 1.dp)
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(64.dp)
                            .background(Color.White),
                        horizontalArrangement = Arrangement.SpaceAround,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                    val items = listOf(
                        Triple("home", "Home", Icons.Default.Home),
                        Triple("search", "Search", Icons.Default.Search)
                    )
                    
                    items.forEach { (route, label, icon) ->
                        val isSelected = currentRoute == route
                        val tint = if (isSelected) PhonePePurple else Color.Gray
                        
                        Column(
                            modifier = Modifier
                                .weight(1f)
                                .fillMaxHeight()
                                .clickable {
                                    if (!isSelected) {
                                        navController.navigate(route) {
                                            popUpTo("home")
                                            launchSingleTop = true
                                            restoreState = true
                                        }
                                    }
                                },
                            horizontalAlignment = Alignment.CenterHorizontally,
                            verticalArrangement = Arrangement.Center
                        ) {
                            Icon(
                                imageVector = icon,
                                contentDescription = label,
                                tint = tint,
                                modifier = Modifier.size(26.dp)
                            )
                            Spacer(modifier = Modifier.height(2.dp))
                            Text(
                                text = label,
                                color = tint,
                                fontSize = 11.sp,
                                fontWeight = if (isSelected) androidx.compose.ui.text.font.FontWeight.Bold else androidx.compose.ui.text.font.FontWeight.Medium
                            )
                        }
                    }
                    
                    // Center QR Button
                    Column(
                        modifier = Modifier
                            .weight(1f)
                            .fillMaxHeight()
                            .clickable {
                                if (currentRoute != "qr") {
                                    navController.navigate("qr") {
                                        popUpTo("home")
                                        launchSingleTop = true
                                        restoreState = true
                                    }
                                }
                            },
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.Center
                    ) {
                        Box(
                            modifier = Modifier
                                .size(48.dp)
                                .background(PhonePePurple, CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = Icons.Default.QrCodeScanner,
                                contentDescription = "QR Scanner",
                                tint = Color.White,
                                modifier = Modifier.size(28.dp)
                            )
                        }
                    }
                    
                    // Alerts and History
                    val rightItems = listOf(
                        Triple("alerts", "Alerts", Icons.Outlined.Notifications),
                        Triple("history", "History", Icons.Default.History)
                    )
                    
                    rightItems.forEach { (route, label, icon) ->
                        val isSelected = currentRoute == route
                        val tint = if (isSelected) PhonePePurple else Color.Gray
                        
                        Column(
                            modifier = Modifier
                                .weight(1f)
                                .fillMaxHeight()
                                .clickable {
                                    if (!isSelected) {
                                        navController.navigate(route) {
                                            popUpTo("home")
                                            launchSingleTop = true
                                            restoreState = true
                                        }
                                    }
                                },
                            horizontalAlignment = Alignment.CenterHorizontally,
                            verticalArrangement = Arrangement.Center
                        ) {
                            Box {
                                Icon(
                                    imageVector = icon,
                                    contentDescription = label,
                                    tint = tint,
                                    modifier = Modifier.size(26.dp)
                                )
                                if (route == "alerts") {
                                    Box(
                                        modifier = Modifier
                                            .align(Alignment.TopEnd)
                                            .offset(x = 4.dp, y = (-2).dp)
                                            .size(14.dp)
                                            .background(Color(0xFF388E3C), CircleShape),
                                        contentAlignment = Alignment.Center
                                    ) {
                                        Text("1", color = Color.White, fontSize = 9.sp, fontWeight = androidx.compose.ui.text.font.FontWeight.Bold)
                                    }
                                }
                            }
                            Spacer(modifier = Modifier.height(2.dp))
                            Text(
                                text = label,
                                color = tint,
                                fontSize = 11.sp,
                                fontWeight = if (isSelected) androidx.compose.ui.text.font.FontWeight.Bold else androidx.compose.ui.text.font.FontWeight.Medium
                            )
                        }
                    }
                }
                } // End Column for navigation bars padding
            }
        }
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = "home",
            modifier = Modifier.padding(innerPadding)
        ) {

            composable("home") {
                HomeScreen(
                    viewModel = prankViewModel,
                    onCreatePrank = {
                        navController.navigate("create")
                    },
                    onNavigateToReceipt = { transactionId ->
                        navController.navigate("receipt/$transactionId")
                    },
                    onNavigateToQr = {
                        navController.navigate("my_qr")
                    },
                    onNavigateToCheckBalance = {
                        navController.navigate("check_balance")
                    },
                    onNavigateToProfile = {
                        navController.navigate("profile")
                    },
                    onNavigateToContactList = {
                        navController.navigate("contact_list")
                    },
                    onNavigateToMobileRecharge = {
                        navController.navigate("mobile_recharge")
                    }
                )
            }

            composable("search") {
                SearchScreen(
                    onCreatePrank = {
                        navController.navigate("create")
                    }
                )
            }

            composable("qr") {
                ScannerScreen(
                    onBack = { navController.popBackStack() },
                    onScanSuccess = { name, upi ->
                        prankViewModel.selectedPayeeUpi = upi
                        navController.navigate("pay_amount/${Uri.encode(name)}")
                    }
                )
            }

            
            
            composable("mobile_recharge") {
                com.example.ui.screens.MobileRechargeScreen(
                    onBack = { navController.popBackStack() },
                    onContactSelect = { contact ->
                        navController.navigate("recharge_plan/${Uri.encode(contact.name)}/${contact.number}")
                    }
                )
            }
            
            composable(
                "recharge_plan/{name}/{number}",
                arguments = listOf(
                    androidx.navigation.navArgument("name") { type = androidx.navigation.NavType.StringType },
                    androidx.navigation.navArgument("number") { type = androidx.navigation.NavType.StringType }
                )
            ) { backStackEntry ->
                val name = backStackEntry.arguments?.getString("name") ?: ""
                val number = backStackEntry.arguments?.getString("number") ?: ""
                com.example.ui.screens.RechargePlanScreen(
                    name = name,
                    number = number,
                    viewModel = prankViewModel,
                    onBack = { navController.popBackStack() },
                    onProceedToPay = { amount ->
                        navController.navigate("recharge_pay_pin/$amount/1/$name")
                    }
                )
            }
            
            composable(
                "recharge_pay_pin/{amount}/{bankId}/{name}",
                arguments = listOf(
                    androidx.navigation.navArgument("amount") { type = androidx.navigation.NavType.StringType },
                    androidx.navigation.navArgument("bankId") { type = androidx.navigation.NavType.StringType },
                    androidx.navigation.navArgument("name") { type = androidx.navigation.NavType.StringType }
                )
            ) { backStackEntry ->
                val amount = backStackEntry.arguments?.getString("amount") ?: "0"
                val bankId = backStackEntry.arguments?.getString("bankId") ?: "1"
                val name = backStackEntry.arguments?.getString("name") ?: ""
                com.example.ui.screens.RechargePinScreen(
                    amount = amount,
                    bankId = bankId,
                    name = name,
                    viewModel = prankViewModel,
                    onBack = { navController.popBackStack() },
                    onSuccess = { txId ->
                        navController.navigate("recharge_processing/$amount/$txId/${Uri.encode(name)}") {
                            popUpTo("recharge_plan") { inclusive = false }
                        }
                    }
                )
            }
            
            composable(
                "recharge_processing/{amount}/{transactionId}/{name}",
                arguments = listOf(
                    androidx.navigation.navArgument("amount") { type = androidx.navigation.NavType.StringType },
                    androidx.navigation.navArgument("transactionId") { type = androidx.navigation.NavType.IntType },
                    androidx.navigation.navArgument("name") { type = androidx.navigation.NavType.StringType }
                )
            ) { backStackEntry ->
                val amount = backStackEntry.arguments?.getString("amount") ?: "0"
                val transactionId = backStackEntry.arguments?.getInt("transactionId") ?: 0
                val name = backStackEntry.arguments?.getString("name") ?: ""
                com.example.ui.screens.RechargeProcessingScreen(
                    name = name,
                    amount = amount,
                    onSuccess = { 
                        navController.navigate("recharge_success/$amount/$transactionId/${Uri.encode(name)}") {
                            popUpTo("mobile_recharge") { inclusive = false }
                        }
                    }
                )
            }
            
            composable(
                "recharge_success/{amount}/{transactionId}/{name}",
                arguments = listOf(
                    androidx.navigation.navArgument("amount") { type = androidx.navigation.NavType.StringType },
                    androidx.navigation.navArgument("transactionId") { type = androidx.navigation.NavType.IntType },
                    androidx.navigation.navArgument("name") { type = androidx.navigation.NavType.StringType }
                )
            ) { backStackEntry ->
                val amount = backStackEntry.arguments?.getString("amount") ?: "0"
                val name = backStackEntry.arguments?.getString("name") ?: ""
                val transactionId = backStackEntry.arguments?.getInt("transactionId") ?: 0
                com.example.ui.screens.RechargeSuccessScreen(
                    transactionId = transactionId,
                    viewModel = prankViewModel,
                    onDone = {
                        navController.navigate("home") {
                            popUpTo("home") { inclusive = true }
                        }
                    }
                )
            }
            
            composable("contact_list") {

                SendMoneyScreen(
                    viewModel = prankViewModel,
                    onBack = { navController.popBackStack() },
                    onNewPayment = { navController.navigate("select_contact") },
                    onContactSelect = { contactName ->
                        navController.navigate("chat/${Uri.encode(contactName)}")
                    }
                )
            }
            
            composable("select_contact") {
                SelectContactScreen(
                    onBack = { navController.popBackStack() },
                    onContactSelect = { contact ->
                        navController.navigate("chat/${Uri.encode(contact.name)}")
                    }
                )
            }
            
            composable(
                "chat/{contactName}",
                arguments = listOf(navArgument("contactName") { type = NavType.StringType })
            ) { backStackEntry ->
                val contactName = backStackEntry.arguments?.getString("contactName") ?: ""
                ChatScreen(
                    contactName = contactName,
                    viewModel = prankViewModel,
                    onBack = { navController.popBackStack() },
                    onPayAmount = { amount, name ->
                        // Navigate to pay flow with pre-filled name and amount
                        navController.navigate("pay_amount_prefilled/$amount/${Uri.encode(name)}")
                    }
                )
            }
            
            composable(
                "pay_amount_prefilled/{amount}/{name}",
                arguments = listOf(
                    navArgument("amount") { type = NavType.StringType },
                    navArgument("name") { type = NavType.StringType }
                )
            ) { backStackEntry ->
                val amount = backStackEntry.arguments?.getString("amount") ?: ""
                val name = backStackEntry.arguments?.getString("name") ?: ""
                // Use PayAmountScreen but with prefilled data?
                // Wait, PayAmountScreen currently doesn't take amount/name as args. Let's fix that.
                // We'll modify PayAmountScreen to accept prefilled name
                PayAmountScreen(
                    viewModel = prankViewModel,
                    payeeName = name,
                    prefilledAmount = amount,
                    onBack = { navController.popBackStack() },
                    onProceed = { amt, bankAccount -> 
                        navController.navigate("pay_pin/$amt/${bankAccount.id}/${Uri.encode(name)}")
                    }
                )
            }

            composable("my_qr") {
                QrScreen(viewModel = prankViewModel, onBack = { navController.popBackStack() })
            }
            composable("alerts") {
                AlertsScreen()
            }
            
            
            composable(
                "pay_amount/{name}",
                arguments = listOf(
                    androidx.navigation.navArgument("name") { type = androidx.navigation.NavType.StringType }
                )
            ) { backStackEntry ->
                val name = backStackEntry.arguments?.getString("name") ?: "Karishna Karishna"
                
                PayAmountScreen(
                    viewModel = prankViewModel,
                    payeeName = name,
                    upiId = prankViewModel.selectedPayeeUpi,
                    onBack = { navController.popBackStack() },
                    onProceed = { amount, bankAccount -> 
                        navController.navigate("pay_pin/$amount/${bankAccount.id}/${Uri.encode(name)}")
                    }
                )
            }
            
            composable(
                "pay_pin/{amount}/{bankId}/{name}",
                arguments = listOf(
                    navArgument("amount") { type = NavType.StringType },
                    navArgument("bankId") { type = NavType.StringType },
                    navArgument("name") { type = NavType.StringType }
                )
            ) { backStackEntry ->
                val amount = backStackEntry.arguments?.getString("amount") ?: "0"
                val bankId = backStackEntry.arguments?.getString("bankId") ?: ""
                val name = backStackEntry.arguments?.getString("name") ?: "Karishna Karishna"
                val bankAccounts by prankViewModel.bankAccounts.collectAsState()
                val selectedBank = bankAccounts.find { it.id == bankId }
                
                var enteredPin by remember { mutableStateOf("") }
                val context = LocalContext.current
                
                PinEntryScreen(
                    bankName = selectedBank?.bankName ?: "Bank",
                    actionText = "Sending: ₹$amount",
                    pin = enteredPin,
                    onPinChange = { enteredPin = it },
                    onSubmit = {
                        val correctPin = selectedBank?.pin ?: "1234"
                        if (enteredPin == correctPin) {
                            enteredPin = ""
                            navController.navigate("pay_processing/$amount/$bankId/${Uri.encode(name)}") {
                                popUpTo("pay_amount") { inclusive = true }
                            }
                        } else {
                            Toast.makeText(context, "Incorrect UPI PIN (Default is 1234)", Toast.LENGTH_SHORT).show()
                            enteredPin = ""
                        }
                    }
                )
            }
            
            composable(
                "pay_processing/{amount}/{bankId}/{name}",
                arguments = listOf(
                    navArgument("amount") { type = NavType.StringType },
                    navArgument("bankId") { type = NavType.StringType },
                    navArgument("name") { type = NavType.StringType }
                )
            ) { backStackEntry ->
                val amount = backStackEntry.arguments?.getString("amount") ?: "0"
                val bankId = backStackEntry.arguments?.getString("bankId") ?: ""
                val name = backStackEntry.arguments?.getString("name") ?: "Karishna Karishna"
                val bankAccounts by prankViewModel.bankAccounts.collectAsState()
                val selectedBank = bankAccounts.find { it.id == bankId }
                
                PaymentProcessingScreen(
                    onProcessingComplete = {
                        // Insert transaction
                        val parsedAmount = amount.toDoubleOrNull() ?: 100.0
                        val resolvedBankName = selectedBank?.bankName ?: "State Bank of India"
                        val resolvedBankLast4 = selectedBank?.bankDesc?.takeLast(4) ?: "0365"
                        
                        com.example.ui.NotificationHelper.showBankSmsNotification(
                            context = context,
                            amount = parsedAmount,
                            bankLast4 = resolvedBankLast4,
                            payeeName = name,
                            bankName = resolvedBankName
                        )
                        
                        prankViewModel.insertTransaction(
                            name = name,
                            phone = "9876543210",
                            upiId = "krishna88750@axl",
                            amount = parsedAmount,
                            status = "SUCCESS",
                            bankName = resolvedBankName,
                            bankLast4 = resolvedBankLast4,
                            customTxId = "",
                            customUtr = "",
                            timestamp = System.currentTimeMillis(),
                            onSuccess = { insertedId ->
                                navController.navigate("pay_success/$amount/$insertedId/${Uri.encode(name)}") {
                                    popUpTo("home")
                                }
                            }
                        )
                    }
                )
            }
            
            composable(
                "pay_success/{amount}/{transactionId}/{name}",
                arguments = listOf(
                    navArgument("amount") { type = NavType.StringType },
                    navArgument("transactionId") { type = NavType.IntType },
                    navArgument("name") { type = NavType.StringType }
                )
            ) { backStackEntry ->
                val amount = backStackEntry.arguments?.getString("amount") ?: "0"
                val txId = backStackEntry.arguments?.getInt("transactionId") ?: 0
                val name = backStackEntry.arguments?.getString("name") ?: "Karishna Karishna"
                
                val allTxs by prankViewModel.allTransactions.collectAsState()
                val currentTx = allTxs.find { it.id == txId }
                
                PaymentSuccessScreen(
                    amount = amount,
                    payeeName = name,
                    upiId = prankViewModel.selectedPayeeUpi,
                    bankName = currentTx?.senderBankName ?: "State Bank of India",
                    onDone = {
                        navController.navigate("home") {
                            popUpTo("home") { inclusive = true }
                        }
                    },
                    onViewDetails = {
                        navController.navigate("receipt/$txId?skipAnimation=true") {
                            popUpTo("home")
                        }
                    }
                )
            }

            composable("create") {
                CreatePrankScreen(
                    viewModel = prankViewModel,
                    onBack = {
                        navController.popBackStack()
                    },
                    onNavigateToReceipt = { transactionId ->
                        navController.navigate("receipt/$transactionId") {
                            // Pop the "create" screen so pressing back on receipt returns to home
                            popUpTo("home")
                        }
                    }
                )
            }
            
            composable(
                route = "receipt/{transactionId}?skipAnimation={skipAnimation}",
                arguments = listOf(
                    navArgument("transactionId") { type = NavType.IntType },
                    navArgument("skipAnimation") { type = NavType.BoolType; defaultValue = false }
                )
            ) { backStackEntry ->
                val transactionId = backStackEntry.arguments?.getInt("transactionId") ?: 0
                val skipAnimation = backStackEntry.arguments?.getBoolean("skipAnimation") ?: false
                ReceiptScreen(
                    transactionId = transactionId,
                    skipAnimation = skipAnimation,
                    viewModel = prankViewModel,
                    onDone = {
                        navController.navigate("home") {
                            popUpTo("home") { inclusive = true }
                        }
                    },
                    onNavigateToCheckBalance = {
                        navController.navigate("check_balance")
                    }
                )
            }
            
            composable("check_balance") {
                CheckBalanceScreen(viewModel = prankViewModel,
                    onBack = { navController.popBackStack() })
            }
            composable("history") {
                HistoryScreen(
                    viewModel = prankViewModel,
                    onNavigateToReceipt = { transactionId ->
                        navController.navigate("receipt/$transactionId")
                    }
                )
            }
            composable("edit_details") {
                EditDetailsScreen(viewModel = prankViewModel,
                    onBack = { navController.popBackStack() })
            }
            composable("bank_accounts") {
                BankAccountsScreen(
                    viewModel = prankViewModel,
                    onBack = { navController.popBackStack() },
                    onNavigateToAccountDetails = { id, isEditMode -> 
                        navController.navigate("account_details/$id/$isEditMode") 
                    },
                    onNavigateToAddBankAccount = { navController.navigate("add_bank_account") }
                )
            }
            composable("add_bank_account") {
                AddBankAccountScreen(
                    onBack = { navController.popBackStack() },
                    onNavigateToAddBankAccountDetails = { bankName ->
                        navController.navigate("add_bank_account_details/$bankName")
                    }
                )
            }
            composable(
                "add_bank_account_details/{bankName}",
                arguments = listOf(navArgument("bankName") { type = NavType.StringType })
            ) { backStackEntry ->
                val bankName = backStackEntry.arguments?.getString("bankName") ?: "Bank"
                AddBankAccountDetailsScreen(
                    bankName = bankName,
                    viewModel = prankViewModel,
                    onBack = { navController.popBackStack() },
                    onSave = {
                        navController.navigate("bank_accounts") {
                            popUpTo("bank_accounts") { inclusive = false }
                        }
                    }
                )
            }
            composable(
                "account_details/{id}/{isEditMode}",
                arguments = listOf(
                    navArgument("id") { type = NavType.StringType },
                    navArgument("isEditMode") { type = NavType.BoolType }
                )
            ) { backStackEntry ->
                val id = backStackEntry.arguments?.getString("id") ?: ""
                val isEditMode = backStackEntry.arguments?.getBoolean("isEditMode") ?: false
                AccountDetailsScreen(
                    accountId = id,
                    isEditable = isEditMode,
                    viewModel = prankViewModel,
                    onBack = { navController.popBackStack() },
                    onNavigateToCheckBalance = { navController.navigate("check_balance") }
                )
            }
            composable("profile") {
                ProfileScreen(
                    viewModel = prankViewModel,
                    prefsManager = prefsManager,
                    onBack = { navController.popBackStack() },
                    onNavigateToEditDetails = { navController.navigate("edit_details") },
                    onNavigateToAccountDetails = { navController.navigate("bank_accounts") }
                )
            }
        }
        }
    }


@Composable
fun ShakeEffect(onShake: () -> Unit) {
    val context = LocalContext.current
    val currentOnShake by rememberUpdatedState(onShake)
    
    DisposableEffect(context) {
        val sensorManager = context.getSystemService(android.content.Context.SENSOR_SERVICE) as android.hardware.SensorManager
        val accelerometer = sensorManager.getDefaultSensor(android.hardware.Sensor.TYPE_ACCELEROMETER)
        
        val shakeDetector = com.example.ShakeDetector {
            currentOnShake()
        }
        
        if (accelerometer != null) {
            sensorManager.registerListener(shakeDetector, accelerometer, android.hardware.SensorManager.SENSOR_DELAY_UI)
        }
        
        onDispose {
            sensorManager.unregisterListener(shakeDetector)
        }
    }
}
