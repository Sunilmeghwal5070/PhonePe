import re

with open('/app/applet/app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt', 'r') as f:
    content = f.read()

new_ads_logic = """
            Spacer(modifier = Modifier.height(24.dp))
            
            // Ads Section with Auto-scroll
            val pagerState = androidx.compose.foundation.pager.rememberPagerState(pageCount = { 4 })
            
            LaunchedEffect(Unit) {
                while (true) {
                    kotlinx.coroutines.delay(3000) // 3 seconds delay
                    val nextPage = (pagerState.currentPage + 1) % 4
                    pagerState.animateScrollToPage(nextPage)
                }
            }
            
            androidx.compose.foundation.pager.HorizontalPager(
                state = pagerState,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(200.dp)
                    .padding(horizontal = 16.dp),
                pageSpacing = 16.dp
            ) { page ->
                val context = LocalContext.current
                val adResId = context.resources.getIdentifier("ad${page + 1}", "drawable", context.packageName)
                
                androidx.compose.foundation.layout.Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .clip(RoundedCornerShape(12.dp))
                        .background(Color(0xFFE0E0E0))
                ) {
                    if (adResId != 0) {
                        androidx.compose.foundation.Image(
                            painter = androidx.compose.ui.res.painterResource(id = adResId),
                            contentDescription = "Ad ${page + 1}",
                            modifier = Modifier.fillMaxSize(),
                            contentScale = androidx.compose.ui.layout.ContentScale.Crop
                        )
                    } else {
                        // Placeholder if image is not uploaded yet
                        androidx.compose.material3.Text(
                            text = "Ad ${page + 1}\n(Please add ad${page + 1}.png to res/drawable)",
                            modifier = Modifier.align(Alignment.Center),
                            textAlign = TextAlign.Center,
                            color = Color.Gray
                        )
                    }
                }
            }
            Spacer(modifier = Modifier.height(24.dp))
"""

content = re.sub(
    r'Spacer\(modifier = Modifier\.height\(24\.dp\)\)\s*Box\(\s*modifier = Modifier\s*\.fillMaxWidth\(\)\s*\.height\(300\.dp\)\s*\.background\(Color\(0xFFF5F5F5\)\)\s*\)',
    new_ads_logic.strip(),
    content,
    flags=re.DOTALL
)

with open('/app/applet/app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt', 'w') as f:
    f.write(content)

