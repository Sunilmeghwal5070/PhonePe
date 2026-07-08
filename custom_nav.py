import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

start_marker = '                NavigationBar('
end_marker = '            }\n        }\n    ) { innerPadding ->'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Markers not found")
    exit(1)

new_nav = """                Column(modifier = Modifier.fillMaxWidth().background(Color.White)) {
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
                                            navController.navigate(route) {
                                                popUpTo("home")
                                                launchSingleTop = true
                                                restoreState = true
                                            }
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
"""

new_content = content[:start_idx] + new_nav + content[end_idx:]

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(new_content)

print("Custom nav applied")
