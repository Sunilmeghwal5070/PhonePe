import re

with open('app/src/main/java/com/example/ui/screens/QrScreen.kt', 'r') as f:
    text = f.read()

# Make sure HorizontalPager is imported
import_target = "import kotlin.random.Random"
import_replacement = "import kotlin.random.Random\nimport androidx.compose.foundation.pager.HorizontalPager\nimport androidx.compose.foundation.pager.rememberPagerState"
text = text.replace(import_target, import_replacement)

# Replace the single QR UI with a HorizontalPager
target_ui = """    Scaffold(
        topBar = {"""

replacement_ui = """    val pagerState = rememberPagerState(pageCount = { bankAccounts.size })

    Scaffold(
        topBar = {"""
text = text.replace(target_ui, replacement_ui)

target_column = """    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .background(Color.White),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Spacer(modifier = Modifier.height(24.dp))
            
            // Bank Logo
            Box(
                modifier = Modifier
                    .size(48.dp)
                    .border(1.dp, Color(0xFFE0E0E0), RoundedCornerShape(12.dp)),
                contentAlignment = Alignment.Center
            ) {
                coil.compose.AsyncImage(
                    model = getBankLogoUrl(bankName),
                    contentDescription = "Bank Logo",
                    modifier = Modifier.fillMaxSize().padding(6.dp),
                    contentScale = androidx.compose.ui.layout.ContentScale.Fit
                )
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            
            Text(
                text = "$bankName - $last4",
                fontSize = 20.sp,
                fontWeight = FontWeight.Bold,
                color = Color.Black
            )
            
            Spacer(modifier = Modifier.height(8.dp))
            
            Text(
                text = "Primary account for receiving money",
                fontSize = 14.sp,
                color = Color(0xFF388E3C)
            )
            
            Spacer(modifier = Modifier.height(32.dp))
            
            // Large QR Code"""

replacement_column = """    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .background(Color.White),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            HorizontalPager(
                state = pagerState,
                modifier = Modifier.weight(1f)
            ) { page ->
                val currentBank = bankAccounts.getOrNull(page)
                val currentBankName = currentBank?.bankName ?: "State Bank Of India"
                val currentLast4 = currentBank?.bankDesc?.takeLast(4) ?: "0000"
                val currentUpiId = currentBank?.upiIds?.firstOrNull() ?: "unknown@ybl"

                Column(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Spacer(modifier = Modifier.height(24.dp))
                    
                    // Bank Logo
                    Box(
                        modifier = Modifier
                            .size(48.dp)
                            .border(1.dp, Color(0xFFE0E0E0), RoundedCornerShape(12.dp)),
                        contentAlignment = Alignment.Center
                    ) {
                        coil.compose.AsyncImage(
                            model = getBankLogoUrl(currentBankName),
                            contentDescription = "Bank Logo",
                            modifier = Modifier.fillMaxSize().padding(6.dp),
                            contentScale = androidx.compose.ui.layout.ContentScale.Fit
                        )
                    }
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    Text(
                        text = "$currentBankName - $currentLast4",
                        fontSize = 20.sp,
                        fontWeight = FontWeight.Bold,
                        color = Color.Black
                    )
                    
                    Spacer(modifier = Modifier.height(8.dp))
                    
                    if (page == 0) {
                        Text(
                            text = "Primary account for receiving money",
                            fontSize = 14.sp,
                            color = Color(0xFF388E3C)
                        )
                    } else {
                        Spacer(modifier = Modifier.height(20.dp))
                    }
                    
                    Spacer(modifier = Modifier.height(32.dp))
                    
                    // Large QR Code"""

text = text.replace(target_column, replacement_column)


target_bottom = """            Spacer(modifier = Modifier.weight(1f))
            
            // Bottom Banner"""

replacement_bottom = """                } // End Column inside Pager
            } // End HorizontalPager

            // Page Indicator
            Row(
                modifier = Modifier.padding(vertical = 16.dp),
                horizontalArrangement = Arrangement.Center
            ) {
                repeat(pagerState.pageCount) { iteration ->
                    val color = if (pagerState.currentPage == iteration) Color.DarkGray else Color.LightGray
                    Box(
                        modifier = Modifier
                            .padding(4.dp)
                            .clip(CircleShape)
                            .background(color)
                            .size(8.dp)
                    )
                }
            }
            
            // Bottom Banner"""

# Wait, upiId is used further down. We need to replace upiId with currentUpiId within the pager content.
# Also the action buttons use upiId. So they must be inside the Pager!
pass
