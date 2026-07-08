package com.example.ui.screens

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.provider.ContactsContract
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat
import com.example.ui.PrankViewModel
import kotlinx.coroutines.delay
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.material3.TabRowDefaults.tabIndicatorOffset
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MobileRechargeScreen(
    onBack: () -> Unit,
    onContactSelect: (Contact) -> Unit
) {
    val context = LocalContext.current
    var hasPermission by remember {
        mutableStateOf(
            ContextCompat.checkSelfPermission(
                context,
                Manifest.permission.READ_CONTACTS
            ) == PackageManager.PERMISSION_GRANTED
        )
    }

    var contacts by remember { mutableStateOf<List<Contact>>(emptyList()) }
    var searchQuery by remember { mutableStateOf("") }

    val permissionLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestPermission()
    ) { isGranted ->
        hasPermission = isGranted
        if (isGranted) {
            contacts = fetchContacts(context)
        }
    }

    LaunchedEffect(hasPermission) {
        if (hasPermission) {
            contacts = fetchContacts(context)
        } else {
            permissionLauncher.launch(Manifest.permission.READ_CONTACTS)
        }
    }

    val isPhoneNumber = searchQuery.replace(" ", "").all { it.isDigit() } && searchQuery.replace(" ", "").length >= 4
    val filteredContacts = if (searchQuery.isBlank()) {
        contacts
    } else {
        val matches = contacts.filter { it.name.contains(searchQuery, ignoreCase = true) || it.number.contains(searchQuery) }.toMutableList()
        if (isPhoneNumber && matches.none { it.number.replace("\\D".toRegex(), "") == searchQuery.replace(" ", "") }) {
            matches.add(0, Contact(name = "Recharge to " + searchQuery, number = searchQuery))
        }
        matches
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Mobile Recharge", fontWeight = FontWeight.Bold, fontSize = 18.sp) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    IconButton(onClick = { }) {
                        Icon(Icons.Default.HelpOutline, contentDescription = "Help")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.White)
            )
        },
        containerColor = Color(0xFFF5F5F5)
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
            // Banner
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                shape = RoundedCornerShape(12.dp),
                colors = CardDefaults.cardColors(containerColor = Color(0xFF7B1FA2))
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text("Get flat ₹30 cashback", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 18.sp)
                    Text("Recharge your mobile with Mastercard Cards on PhonePe", color = Color.White, fontSize = 12.sp)
                }
            }

            // Search Bar
            OutlinedTextField(
                value = searchQuery,
                onValueChange = { searchQuery = it },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp),
                placeholder = { Text("Search by Number or Name", color = Color.Gray) },
                leadingIcon = { Icon(Icons.Default.Search, contentDescription = "Search") },
                shape = RoundedCornerShape(24.dp),
                colors = OutlinedTextFieldDefaults.colors(
                    focusedContainerColor = Color.White,
                    unfocusedContainerColor = Color.White,
                    focusedBorderColor = Color(0xFF5f259f),
                    unfocusedBorderColor = Color.LightGray
                ),
                singleLine = true
            )
            
            Spacer(modifier = Modifier.height(16.dp))

            // Quick Data Top-up
            Text("Quick Data Top-up", fontWeight = FontWeight.Bold, modifier = Modifier.padding(horizontal = 16.dp), fontSize = 14.sp)
            Spacer(modifier = Modifier.height(8.dp))
            LazyRow(contentPadding = PaddingValues(horizontal = 16.dp)) {
                item {
                    DataCard("VI", "1.5 GB for ₹26")
                    Spacer(modifier = Modifier.width(8.dp))
                }
                item {
                    DataCard("Jio", "1 GB for ₹19")
                }
            }
            
            Spacer(modifier = Modifier.height(16.dp))

            // Contacts List
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .weight(1f),
                colors = CardDefaults.cardColors(containerColor = Color.White),
                shape = RoundedCornerShape(topStart = 16.dp, topEnd = 16.dp)
            ) {
                LazyColumn {
                    if (filteredContacts.isNotEmpty()) {
                        item {
                            Text("ALL CONTACTS", color = Color.Gray, fontSize = 12.sp, modifier = Modifier.padding(16.dp), letterSpacing = 1.sp)
                        }
                        items(filteredContacts.take(50)) { contact ->
                            ContactItem(contact = contact, onClick = { onContactSelect(contact) })
                        }
                    } else if (hasPermission) {
                        item {
                            Text("No contacts found", modifier = Modifier.padding(16.dp), color = Color.Gray)
                        }
                    } else {
                        item {
                            Text("Permission needed to show contacts", modifier = Modifier.padding(16.dp), color = Color.Gray)
                        }
                    }
                    
                    item {
                        Text(
                            "By proceeding further, you allow PhonePe to fetch your current and future plan expiry information and remind you",
                            color = Color.Gray, fontSize = 12.sp, modifier = Modifier.padding(16.dp)
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun DataCard(operator: String, details: String) {
    Card(
        colors = CardDefaults.cardColors(containerColor = Color.White),
        shape = RoundedCornerShape(8.dp),
        border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFEEEEEE))
    ) {
        Row(
            modifier = Modifier.padding(12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier
                    .size(24.dp)
                    .clip(CircleShape)
                    .background(if (operator == "Jio") Color(0xFF1976D2) else Color.Red),
                contentAlignment = Alignment.Center
            ) {
                Text(operator.take(1), color = Color.White, fontWeight = FontWeight.Bold, fontSize = 12.sp)
            }
            Spacer(modifier = Modifier.width(8.dp))
            Text(details, fontSize = 14.sp, fontWeight = FontWeight.Bold)
            Spacer(modifier = Modifier.width(8.dp))
            Icon(Icons.Default.ArrowForward, contentDescription = null, tint = Color(0xFF5f259f), modifier = Modifier.size(16.dp))
        }
    }
}

@Composable
fun ContactItem(contact: Contact, onClick: () -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick)
            .padding(horizontal = 16.dp, vertical = 12.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Box(
            modifier = Modifier
                .size(40.dp)
                .background(Color(0xFFE8EAF6), CircleShape),
            contentAlignment = Alignment.Center
        ) {
            Text(
                contact.name.take(2).uppercase(),
                color = Color(0xFF3F51B5),
                fontWeight = FontWeight.Bold
            )
        }
        Spacer(modifier = Modifier.width(16.dp))
        Column(modifier = Modifier.weight(1f)) {
            Text(contact.name, fontSize = 16.sp, fontWeight = FontWeight.Medium)
            Text(contact.number, fontSize = 14.sp, color = Color.Gray)
        }
        Icon(Icons.Default.MoreVert, contentDescription = "More", tint = Color.Gray)
    }
}

data class RechargePlan(
    val price: String,
    val validity: String,
    val data: String,
    val description: String,
    val category: String
)

val dummyPlans = listOf(
    RechargePlan("29", "2 Days", "2 GB", "Data Pack", "Data Packs"),
    RechargePlan("349", "28 Days", "Unlimited 5G + 2GB/day", "Jio Special benefits: True 5G Unlimited Plan + JioHotstar Mobile + Pro Google...", "Popular"),
    RechargePlan("200", "28 Days", "Unlimited 5G + 30 GB", "Mega OTT Pass- 15 Premium OTT apps", "Popular"),
    RechargePlan("899", "90 Days", "Unlimited 5G + 2GB/day", "Jio Special benefits...", "True 5G Unlimited"),
    RechargePlan("3599", "365 Days", "Unlimited 5G + 2.5GB/day", "Annual Plan with Jio Special benefits...", "True 5G Unlimited"),
    RechargePlan("399", "28 Days", "Unlimited 5G + 2.5GB/Day", "Gaming+JioHotstar+Hollywood", "Popular")
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RechargePlanScreen(
    name: String,
    number: String,
    viewModel: PrankViewModel,
    onBack: () -> Unit,
    onProceedToPay: (String) -> Unit
) {
    var selectedTab by remember { mutableStateOf(0) }
    val tabs = listOf("Popular", "True 5G Unlimited", "Data Packs")
    var selectedPlan by remember { mutableStateOf<RechargePlan?>(null) }
    
    val currentCategory = tabs[selectedTab]
    val filteredPlans = dummyPlans.filter { it.category == currentCategory }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Select a recharge plan", fontWeight = FontWeight.Bold, fontSize = 18.sp) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    IconButton(onClick = { }) {
                        Icon(Icons.Default.HelpOutline, contentDescription = "Help")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color.White)
            )
        },
        containerColor = Color(0xFFF5F5F5)
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
            // Header Info
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(Color.White)
                    .padding(16.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Box(
                    modifier = Modifier
                        .size(40.dp)
                        .background(Color(0xFF1976D2), CircleShape),
                    contentAlignment = Alignment.Center
                ) {
                    Text("Jio", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                }
                Spacer(modifier = Modifier.width(16.dp))
                Column {
                    Text("$name • $number", fontSize = 16.sp, fontWeight = FontWeight.Medium)
                    Row {
                        Text("Jio Prepaid • Rajasthan", fontSize = 14.sp, color = Color.Gray)
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("Change", fontSize = 14.sp, color = Color(0xFF5f259f), fontWeight = FontWeight.Bold)
                    }
                }
            }

            // Search and Filters
            Column(modifier = Modifier.background(Color.White)) {
                OutlinedTextField(
                    value = "",
                    onValueChange = {},
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 8.dp),
                    placeholder = { Text("Search a plan, eg 349, 5G, etc.") },
                    leadingIcon = { Icon(Icons.Default.Search, contentDescription = null) },
                    shape = RoundedCornerShape(24.dp)
                )

                ScrollableTabRow(
                    selectedTabIndex = selectedTab,
                    containerColor = Color.White,
                    edgePadding = 16.dp,
                    indicator = { tabPositions ->
                        if (selectedTab < tabPositions.size) {
                            TabRowDefaults.Indicator(
                                modifier = Modifier.tabIndicatorOffset(tabPositions[selectedTab]),
                                color = Color(0xFF5f259f)
                            )
                        }
                    }
                ) {
                    tabs.forEachIndexed { index, title ->
                        Tab(
                            selected = selectedTab == index,
                            onClick = { selectedTab = index },
                            text = { 
                                Text(
                                    title, 
                                    fontWeight = if (selectedTab == index) FontWeight.Bold else FontWeight.Normal,
                                    color = if (selectedTab == index) Color(0xFF5f259f) else Color.Gray
                                ) 
                            }
                        )
                    }
                }
            }
            
            // Plans List
            LazyColumn(modifier = Modifier.weight(1f)) {
                items(filteredPlans) { plan ->
                    PlanCard(plan = plan, onClick = { selectedPlan = plan })
                }
            }
        }
    }
    
    // Bottom Sheet for Plan Details
    if (selectedPlan != null) {
        ModalBottomSheet(
            onDismissRequest = { selectedPlan = null },
            containerColor = Color.White,
            shape = RoundedCornerShape(topStart = 16.dp, topEnd = 16.dp)
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text("₹${selectedPlan!!.price} Plan Details", fontSize = 20.sp, fontWeight = FontWeight.Bold)
                    IconButton(onClick = { selectedPlan = null }) {
                        Icon(Icons.Default.Close, contentDescription = "Close")
                    }
                }
                
                Spacer(modifier = Modifier.height(16.dp))
                
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    Column {
                        Text("Validity", color = Color.Gray, fontSize = 14.sp)
                        Text(selectedPlan!!.validity, fontSize = 16.sp, fontWeight = FontWeight.Medium)
                    }
                    Column {
                        Text("Data", color = Color.Gray, fontSize = 14.sp)
                        Text(selectedPlan!!.data, fontSize = 16.sp, fontWeight = FontWeight.Medium)
                    }
                }
                
                Spacer(modifier = Modifier.height(24.dp))
                Text("Additional Benefits", fontSize = 16.sp, fontWeight = FontWeight.Bold)
                Spacer(modifier = Modifier.height(16.dp))
                
                BenefitRow(Icons.Default.WifiTethering, "Unlimited True 5G Data", "Unlimited 5G data to watch live Cricket...")
                Spacer(modifier = Modifier.height(16.dp))
                BenefitRow(Icons.Default.Star, "JioHotstar Mobile", "Enjoy Live T20 Cricket, sports...")
                
                Spacer(modifier = Modifier.height(32.dp))
                Button(
                    onClick = { 
                        onProceedToPay(selectedPlan!!.price)
                        selectedPlan = null 
                    },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(50.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF5f259f)),
                    shape = RoundedCornerShape(8.dp)
                ) {
                    Text("PROCEED WITH ₹${selectedPlan!!.price}", color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                }
                Spacer(modifier = Modifier.height(16.dp))
            }
        }
    }
}

@Composable
fun BenefitRow(icon: androidx.compose.ui.graphics.vector.ImageVector, title: String, desc: String) {
    Row {
        Icon(icon, contentDescription = null, tint = Color(0xFF1976D2), modifier = Modifier.size(24.dp))
        Spacer(modifier = Modifier.width(16.dp))
        Column {
            Text(title, fontSize = 16.sp, fontWeight = FontWeight.Medium)
            Text(desc, fontSize = 14.sp, color = Color.Gray)
        }
    }
}

@Composable
fun PlanCard(plan: RechargePlan, onClick: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp)
            .clickable(onClick = onClick),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        elevation = CardDefaults.cardElevation(2.dp),
        shape = RoundedCornerShape(8.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text("₹${plan.price}", fontSize = 24.sp, fontWeight = FontWeight.Bold)
                Icon(Icons.Default.KeyboardArrowRight, contentDescription = null, tint = Color.Gray)
            }
            Spacer(modifier = Modifier.height(12.dp))
            Row(
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text("Validity", color = Color.Gray, fontSize = 12.sp)
                    Text(plan.validity, fontSize = 14.sp, fontWeight = FontWeight.Medium)
                }
                Column(modifier = Modifier.weight(1f)) {
                    Text("Data", color = Color.Gray, fontSize = 12.sp)
                    Text(plan.data, fontSize = 14.sp, fontWeight = FontWeight.Medium)
                }
            }
            Spacer(modifier = Modifier.height(12.dp))
            Text(plan.description, color = Color.Gray, fontSize = 12.sp)
            Spacer(modifier = Modifier.height(8.dp))
            Text("Details", color = Color(0xFF5f259f), fontWeight = FontWeight.Bold, fontSize = 14.sp)
        }
    }
}
