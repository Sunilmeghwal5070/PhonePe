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

new_nav = """                NavigationBar(
                    containerColor = Color.White,
                    tonalElevation = 8.dp
                ) {
                    val items = listOf(
                        Triple("home", "Home", listOf(androidx.compose.material.icons.filled.Home, androidx.compose.material.icons.outlined.Home)),
                        Triple("search", "Search", listOf(androidx.compose.material.icons.filled.Search, androidx.compose.material.icons.outlined.Search)),
                        Triple("qr", "", listOf(androidx.compose.material.icons.filled.QrCodeScanner, androidx.compose.material.icons.filled.QrCodeScanner)),
                        Triple("alerts", "Alerts", listOf(androidx.compose.material.icons.filled.Notifications, androidx.compose.material.icons.outlined.Notifications)),
                        Triple("history", "History", listOf(androidx.compose.material.icons.filled.Schedule, androidx.compose.material.icons.outlined.Schedule))
                    )

                    items.forEach { item ->
                        val route = item.first
                        val label = item.second
                        val iconFilled = item.third[0]
                        val iconOutlined = item.third[1]
                        val selected = currentRoute == route

                        NavigationBarItem(
                            selected = selected,
                            onClick = {
                                if (!selected) {
                                    navController.navigate(route) {
                                        popUpTo("home") { saveState = true }
                                        launchSingleTop = true
                                        restoreState = true
                                    }
                                }
                            },
                            icon = {
                                if (route == "qr") {
                                    Box(
                                        modifier = Modifier
                                            .size(42.dp)
                                            .clip(CircleShape)
                                            .background(Color(0xFF5f259f)) // PhonePe Purple
                                            .testTag("qr_scanner_fab"),
                                        contentAlignment = Alignment.Center
                                    ) {
                                        Icon(
                                            imageVector = iconFilled,
                                            contentDescription = "My QR",
                                            tint = Color.White,
                                            modifier = Modifier.size(22.dp)
                                        )
                                    }
                                } else {
                                    Icon(
                                        imageVector = if (selected) iconFilled else iconOutlined,
                                        contentDescription = label,
                                        modifier = Modifier.size(24.dp)
                                    )
                                }
                            },
                            label = if (label.isNotEmpty()) {
                                { Text(label, fontSize = 10.sp, fontWeight = if (selected) FontWeight.Bold else FontWeight.Medium) }
                            } else null,
                            alwaysShowLabel = label.isNotEmpty(),
                            colors = NavigationBarItemDefaults.colors(
                                selectedIconColor = Color.Black,
                                selectedTextColor = Color.Black,
                                indicatorColor = Color.Transparent,
                                unselectedIconColor = Color.Gray,
                                unselectedTextColor = Color.Gray
                            )
                        )
                    }
                }
"""

new_content = content[:start_idx] + new_nav + content[end_idx:]

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(new_content)

print("Nav updated")
