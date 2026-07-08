package com.example

import android.app.Application
import android.os.Bundle
import android.net.Uri
import java.net.URLEncoder
import java.net.URLDecoder
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import android.widget.Toast
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
import com.example.ui.screens.*
import com.example.ui.theme.MyApplicationTheme
import com.example.ui.theme.PhonePeDarkPurple
import com.example.ui.theme.PhonePeLightPurple
import com.example.ui.theme.PhonePePurple

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
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

    var showSplash by remember { mutableStateOf(true) }

    if (showSplash) {
        SplashScreen(onTimeout = { showSplash = false })
        return
    }

    Scaffold(
        modifier = Modifier.fillMaxSize(),
        bottomBar = {
            if (showBottomBar) {
                Column(modifier = Modifier.fillMaxWidth().background(Color.White).navigationBarsPadding()) {
                    HorizontalDivider(thickness = 1.dp, color = Color(0xFFF0F0F0))
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(64.dp),
                        horizontalArrangement = Arrangement.SpaceEvenly,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        val routes = listOf("home", "search", "qr", "alerts", "history")
                        val labels = listOf("Home", "Search", "", "Alerts", "History")
                        val iconsFilled = listOf(
                            Icons.Filled.Home,
                            Icons.Filled.Search,
                            Icons.Filled.QrCodeScanner,
                            Icons.Filled.Notifications,
                            Icons.Filled.Schedule
                        )
                        val iconsOutlined = listOf(
                            Icons.Outlined.Home,
                            Icons.Outlined.Search,
                            Icons.Filled.QrCodeScanner,
                            Icons.Outlined.Notifications,
                            Icons.Outlined.Schedule
                        )

                        routes.forEachIndexed { index, route ->
                            val label = labels[index]
                            val isSelected = currentRoute == route
                            val icon = if (isSelected) iconsFilled[index] else iconsOutlined[index]
                            val tint = if (isSelected) Color.Black else Color.Gray

                            if (route == "qr") {
                                Box(
                                    modifier = Modifier
                                        .weight(1f)
                                        .fillMaxHeight()
                                        .clickable {
                                            val permissions = if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.TIRAMISU) {
                                                arrayOf(android.Manifest.permission.CAMERA, android.Manifest.permission.READ_MEDIA_IMAGES)
                                            } else {
                                                arrayOf(android.Manifest.permission.CAMERA, android.Manifest.permission.READ_EXTERNAL_STORAGE)
                                            }
                                            permissionLauncher.launch(permissions)
                                        },
                                    contentAlignment = Alignment.Center
                                ) {
                                    Box(
                                        modifier = Modifier
                                            .size(46.dp)
                                            .clip(CircleShape)
                                            .background(Color(0xFF5f259f)), // PhonePe Purple
                                        contentAlignment = Alignment.Center
                                    ) {
                                        Icon(
                                            imageVector = Icons.Filled.QrCodeScanner,
                                            contentDescription = "QR Scanner",
                                            tint = Color.White,
                                            modifier = Modifier.size(24.dp)
                                        )
                                    }
                                }
                            } else {
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
                        }
                    }
                }
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
                    onScanComplete = { navController.navigate("pay_amount") }
                )
            }

            
            
            composable("mobile_recharge") {
                com.example.ui.screens.MobileRechargeScreen(
                    onBack = { navController.popBackStack() },
                    onContactSelect = { contact ->
                        navController.navigate("recharge_plan/${java.net.URLEncoder.encode(contact.name, "UTF-8")}/${contact.number}")
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
                    viewModel = prankViewModel,
                    onBack = { navController.popBackStack() },
                    onSuccess = { 
                        navController.navigate("recharge_processing/$amount/$bankId/${java.net.URLEncoder.encode(name, "UTF-8")}") {
                            popUpTo("recharge_plan") { inclusive = false }
                        }
                    }
                )
            }
            
            composable(
                "recharge_processing/{amount}/{bankId}/{name}",
                arguments = listOf(
                    androidx.navigation.navArgument("amount") { type = androidx.navigation.NavType.StringType },
                    androidx.navigation.navArgument("bankId") { type = androidx.navigation.NavType.StringType },
                    androidx.navigation.navArgument("name") { type = androidx.navigation.NavType.StringType }
                )
            ) { backStackEntry ->
                val amount = backStackEntry.arguments?.getString("amount") ?: "0"
                val bankId = backStackEntry.arguments?.getString("bankId") ?: "1"
                val name = backStackEntry.arguments?.getString("name") ?: ""
                com.example.ui.screens.RechargeProcessingScreen(
                    name = name,
                    amount = amount,
                    onSuccess = { transactionId ->
                        navController.navigate("recharge_success/$amount/$transactionId/${java.net.URLEncoder.encode(name, "UTF-8")}") {
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
                    amount = amount,
                    name = name,
                    transactionId = transactionId,
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
                        navController.navigate("chat/${java.net.URLEncoder.encode(contactName, "UTF-8")}")
                    }
                )
            }
            
            composable("select_contact") {
                SelectContactScreen(
                    onBack = { navController.popBackStack() },
                    onContactSelect = { contact ->
                        navController.navigate("chat/${java.net.URLEncoder.encode(contact.name, "UTF-8")}")
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
                        navController.navigate("pay_amount_prefilled/$amount/${java.net.URLEncoder.encode(name, "UTF-8")}")
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
                    prefilledName = name,
                    prefilledAmount = amount,
                    onBack = { navController.popBackStack() },
                    onProceed = { amt, bankAccount -> 
                        navController.navigate("pay_pin/$amt/${bankAccount.id}/${java.net.URLEncoder.encode(name, "UTF-8")}")
                    }
                )
            }

            composable("my_qr") {
                QrScreen()
            }
            composable("alerts") {
                AlertsScreen()
            }
            
            
            composable("pay_amount") {
                PayAmountScreen(
                    viewModel = prankViewModel,
                    onBack = { navController.popBackStack() },
                    onProceed = { amount, bankAccount -> 
                        navController.navigate("pay_pin/$amount/${bankAccount.id}/Karishna%20Karishna")
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
                val name = java.net.URLDecoder.decode(backStackEntry.arguments?.getString("name") ?: "Karishna Karishna", "UTF-8")
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
                            navController.navigate("pay_processing/$amount/$bankId/${java.net.URLEncoder.encode(name, "UTF-8")}") {
                                popUpTo("pay_amount") { inclusive = true }
                            }
                        } else {
                            Toast.makeText(context, "Incorrect UPI PIN", Toast.LENGTH_SHORT).show()
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
                val name = java.net.URLDecoder.decode(backStackEntry.arguments?.getString("name") ?: "Karishna Karishna", "UTF-8")
                val bankAccounts by prankViewModel.bankAccounts.collectAsState()
                val selectedBank = bankAccounts.find { it.id == bankId }
                
                PaymentProcessingScreen(
                    onProcessingComplete = {
                        // Insert transaction
                        prankViewModel.insertTransaction(
                            name = name,
                            phone = "9876543210",
                            upiId = "krishna88750@axl",
                            amount = amount.toDoubleOrNull() ?: 100.0,
                            status = "SUCCESS",
                            bankName = selectedBank?.bankName ?: "State Bank of India",
                            bankLast4 = selectedBank?.bankDesc?.takeLast(4) ?: "0365",
                            customTxId = "",
                            customUtr = "",
                            timestamp = System.currentTimeMillis(),
                            onSuccess = { insertedId ->
                                navController.navigate("pay_success/$amount/$insertedId/${java.net.URLEncoder.encode(name, "UTF-8")}") {
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
                val name = java.net.URLDecoder.decode(backStackEntry.arguments?.getString("name") ?: "Karishna Karishna", "UTF-8")
                
                PaymentSuccessScreen(
                    amount = amount,
                    payeeName = name,
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
                CheckBalanceScreen(viewModel = prankViewModel, onBack = { navController.popBackStack() })
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
                EditDetailsScreen(viewModel = prankViewModel, onBack = { navController.popBackStack() })
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
                    onBack = { navController.popBackStack() },
                    onNavigateToEditDetails = { navController.navigate("edit_details") },
                    onNavigateToAccountDetails = { navController.navigate("bank_accounts") }
                )
            }
        }
    }
}
