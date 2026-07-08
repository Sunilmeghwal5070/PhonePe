import re

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    content = f.read()

start_marker = '// 2. Beautiful "Trade with 5x leverage" Grid Ad Banner'
end_marker = '// 3. Money Transfers Grid'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Markers not found")
    exit(1)

new_banner = """// 2. Beautiful "Trade with 5x leverage" Grid Ad Banner (Matches screenshot 1 perfectly!)
        item {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(180.dp)
                    .background(Color(0xFF2E0854)) // Rich deep dark indigo-purple background
            ) {
                // Animated Lens Distortion effect for grid
                val infiniteTransition = rememberInfiniteTransition(label = "lens")
                val animProgress by infiniteTransition.animateFloat(
                    initialValue = -0.2f,
                    targetValue = 1.2f,
                    animationSpec = infiniteRepeatable(
                        animation = tween(3500, easing = LinearEasing),
                        repeatMode = RepeatMode.Restart
                    ),
                    label = "lensProgress"
                )
                
                // Radial echo effect
                val echoRadius by infiniteTransition.animateFloat(
                    initialValue = 0f,
                    targetValue = 600f,
                    animationSpec = infiniteRepeatable(
                        animation = tween(2500, easing = LinearOutSlowInEasing),
                        repeatMode = RepeatMode.Restart
                    ),
                    label = "echoRadius"
                )
                val echoAlpha by infiniteTransition.animateFloat(
                    initialValue = 0.6f,
                    targetValue = 0f,
                    animationSpec = infiniteRepeatable(
                        animation = tween(2500, easing = LinearOutSlowInEasing),
                        repeatMode = RepeatMode.Restart
                    ),
                    label = "echoAlpha"
                )

                // Background grid lines drawn dynamically with distortion
                Canvas(modifier = Modifier.fillMaxSize()) {
                    val gridSpacing = 24.dp.toPx()
                    val gridColor = Color(0xFF4B1D8C).copy(alpha = 0.6f)
                    
                    val center = Offset(size.width * animProgress, size.height / 2f)
                    val radius = 100.dp.toPx()
                    val maxBulge = 24.dp.toPx()

                    fun bulgePoint(x: Float, y: Float): Offset {
                        val dx = x - center.x
                        val dy = y - center.y
                        val dist = kotlin.math.sqrt(dx * dx + dy * dy)
                        if (dist < radius && dist > 0f) {
                            val bulgeAmount = maxBulge * kotlin.math.sin((1f - dist / radius) * (Math.PI / 2).toFloat()).toFloat()
                            return Offset(
                                x + (dx / dist) * bulgeAmount,
                                y + (dy / dist) * bulgeAmount
                            )
                        }
                        return Offset(x, y)
                    }

                    // Draw radial echo effect
                    drawCircle(
                        color = Color.White.copy(alpha = echoAlpha),
                        radius = echoRadius,
                        center = Offset(size.width / 2f, size.height / 2f),
                        style = Stroke(width = 4f)
                    )
                    drawCircle(
                        color = Color(0xFFCCFF00).copy(alpha = echoAlpha * 0.5f),
                        radius = echoRadius * 0.8f,
                        center = Offset(size.width / 2f, size.height / 2f),
                        style = Stroke(width = 8f)
                    )

                    var x = 0f
                    while (x < size.width) {
                        val path = androidx.compose.ui.graphics.Path()
                        var y = 0f
                        val step = 10f
                        var first = true
                        while (y <= size.height + step) {
                            val p = bulgePoint(x, y)
                            if (first) {
                                path.moveTo(p.x, p.y)
                                first = false
                            } else {
                                path.lineTo(p.x, p.y)
                            }
                            y += step
                        }
                        drawPath(path, color = gridColor, style = Stroke(width = 1f))
                        x += gridSpacing
                    }
                    
                    var yOffset = 0f
                    while (yOffset < size.height) {
                        val path = androidx.compose.ui.graphics.Path()
                        var cx = 0f
                        val step = 10f
                        var first = true
                        while (cx <= size.width + step) {
                            val p = bulgePoint(cx, yOffset)
                            if (first) {
                                path.moveTo(p.x, p.y)
                                first = false
                            } else {
                                path.lineTo(p.x, p.y)
                            }
                            cx += step
                        }
                        drawPath(path, color = gridColor, style = Stroke(width = 1f))
                        yOffset += gridSpacing
                    }
                    
                    drawCircle(
                        color = Color(0xFF7E38D1).copy(alpha = 0.3f),
                        radius = radius * 0.8f,
                        center = center
                    )
                }

                // Banner Content
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(14.dp),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.SpaceBetween
                ) {
                    
                    // Formula Block Animation State
                    var animationStep by remember { mutableIntStateOf(0) }
                    LaunchedEffect(Unit) {
                        while (true) {
                            animationStep = 0
                            delay(1000)
                            animationStep = 1 // show =
                            delay(800)
                            animationStep = 2 // show 500
                            delay(800)
                            animationStep = 3 // shine text
                            delay(2000)
                        }
                    }

                    // Shine effect progress
                    val shimmerProgress by animateFloatAsState(
                        targetValue = if (animationStep >= 3) 2f else -0.5f,
                        animationSpec = tween(durationMillis = 1500, easing = LinearEasing),
                        label = "shimmer"
                    )

                    // Headline
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.Center,
                        modifier = Modifier
                            .graphicsLayer { compositingStrategy = androidx.compose.ui.graphics.CompositingStrategy.Offscreen }
                            .drawWithContent {
                                drawContent()
                                val width = size.width
                                val startX = shimmerProgress * width
                                val brush = Brush.linearGradient(
                                    colors = listOf(Color.Transparent, Color.White, Color.Transparent),
                                    start = Offset(startX, 0f),
                                    end = Offset(startX + width * 0.3f, 0f)
                                )
                                drawRect(brush = brush, blendMode = androidx.compose.ui.graphics.BlendMode.SrcAtop)
                            }
                    ) {
                        Text(
                            text = "Trade with ",
                            color = Color.White,
                            fontSize = 20.sp,
                            fontWeight = FontWeight.ExtraBold,
                            fontFamily = FontFamily.SansSerif
                        )
                        Text(
                            text = "5x leverage",
                            color = Color(0xFFCCFF00), // Lime Green
                            fontSize = 20.sp,
                            fontWeight = FontWeight.ExtraBold,
                            fontFamily = FontFamily.SansSerif
                        )
                    }

                    // Formula Block
                    Row(
                        modifier = Modifier
                            .animateContentSize()
                            .padding(horizontal = 8.dp)
                            .border(1.dp, Color(0xFF5f259f).copy(alpha = 0.8f), RoundedCornerShape(12.dp))
                            .background(Color(0xFF1E033A).copy(alpha = 0.8f))
                            .padding(horizontal = 14.dp, vertical = 10.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.Center
                    ) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Text("₹100", color = Color.White, fontSize = 24.sp, fontWeight = FontWeight.ExtraBold)
                            Text("balance", color = Color.LightGray, fontSize = 11.sp)
                        }

                        androidx.compose.animation.AnimatedVisibility(
                            visible = animationStep >= 1,
                            enter = androidx.compose.animation.fadeIn() + androidx.compose.animation.expandHorizontally()
                        ) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Spacer(modifier = Modifier.width(16.dp))
                                Text("=", color = Color(0xFFCCFF00), fontSize = 28.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                        
                        androidx.compose.animation.AnimatedVisibility(
                            visible = animationStep >= 2,
                            enter = androidx.compose.animation.fadeIn() + androidx.compose.animation.expandHorizontally()
                        ) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Spacer(modifier = Modifier.width(16.dp))
                                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                    Text("₹500", color = Color.White, fontSize = 24.sp, fontWeight = FontWeight.ExtraBold)
                                    Text("in buying power", color = Color.LightGray, fontSize = 11.sp)
                                }
                            }
                        }
                    }

                    // Call to Action
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.Center,
                        modifier = Modifier
                            .clip(RoundedCornerShape(12.dp))
                            .clickable {
                                // Add click event if needed
                            }
                    ) {
                        Text(
                            text = "Switch to ",
                            color = Color.White,
                            fontSize = 15.sp,
                            fontWeight = FontWeight.Bold
                        )
                        Text(
                            text = "share",
                            color = Color.White,
                            fontSize = 15.sp,
                            fontWeight = FontWeight.ExtraBold
                        )
                        Box(
                            modifier = Modifier
                                .padding(horizontal = 4.dp)
                                .size(6.dp)
                                .clip(CircleShape)
                                .background(Color(0xFF00E676))
                        )
                        Text(
                            text = "market",
                            color = Color(0xFF00E676),
                            fontSize = 15.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                }
            }
        }
        
        """

new_content = content[:start_idx] + new_banner + content[end_idx:]

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(new_content)
print("Updated successfully")
