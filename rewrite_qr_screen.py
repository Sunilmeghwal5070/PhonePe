import re

with open('app/src/main/java/com/example/ui/screens/QrScreen.kt', 'r') as f:
    text = f.read()

target = """    val primaryBank = bankAccounts.firstOrNull()
    val bankName = primaryBank?.bankName ?: "State Bank Of India"
    val last4 = primaryBank?.bankDesc?.takeLast(4) ?: "0000"
    val upiId = primaryBank?.upiIds?.firstOrNull() ?: "unknown@ybl"

    Scaffold("""

replacement = """    val pagerState = androidx.compose.foundation.pager.rememberPagerState(pageCount = { bankAccounts.size.coerceAtLeast(1) })

    Scaffold("""
text = text.replace(target, replacement)

target2 = """    ) { paddingValues ->
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
            
            Spacer(modifier = Modifier.height(32.dp))"""

replacement2 = """    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .background(Color.White),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            androidx.compose.foundation.pager.HorizontalPager(
                state = pagerState,
                modifier = Modifier.weight(1f)
            ) { page ->
                val currentBank = bankAccounts.getOrNull(page)
                val bankName = currentBank?.bankName ?: "State Bank Of India"
                val last4 = currentBank?.bankDesc?.takeLast(4) ?: "0000"
                val upiId = currentBank?.upiIds?.firstOrNull() ?: "unknown@ybl"
                
                Column(
                    modifier = Modifier.fillMaxWidth().fillMaxHeight(),
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
                    
                    if (page == 0) {
                        Text(
                            text = "Primary account for receiving money",
                            fontSize = 14.sp,
                            color = Color(0xFF388E3C)
                        )
                    } else {
                        Spacer(modifier = Modifier.height(20.dp))
                    }
                    
                    Spacer(modifier = Modifier.height(32.dp))"""

text = text.replace(target2, replacement2)

target3 = """            }
            
            Spacer(modifier = Modifier.weight(1f))
            
            // Bottom Banner"""

replacement3 = """            }
                } // End inner column
            } // End pager
            
            // Page Indicator
            if (bankAccounts.size > 1) {
                Row(
                    modifier = Modifier.padding(vertical = 16.dp),
                    horizontalArrangement = Arrangement.Center
                ) {
                    repeat(bankAccounts.size) { iteration ->
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
            } else {
                Spacer(modifier = Modifier.height(40.dp))
            }
            
            // Bottom Banner"""
text = text.replace(target3, replacement3)

with open('app/src/main/java/com/example/ui/screens/QrScreen.kt', 'w') as f:
    f.write(text)
