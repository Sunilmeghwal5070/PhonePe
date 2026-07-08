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
                    val routes = listOf("home", "search", "qr", "alerts", "history")
                    val labels = listOf("Home", "Search", "", "Alerts", "History")
                    val iconsFilled = listOf(
                        androidx.compose.material.icons.Icons.Filled.Home,
                        androidx.compose.material.icons.Icons.Filled.Search,
                        androidx.compose.material.icons.Icons.Filled.QrCodeScanner,
                        androidx.compose.material.icons.Icons.Filled.Notifications,
                        androidx.compose.material.icons.Icons.Filled.Schedule
                    )
                    val iconsOutlined = listOf(
                        androidx.compose.material.icons.Icons.Outlined.Home,
                        androidx.compose.material.icons.Icons.Outlined.Search,
                        androidx.compose.material.icons.Icons.Filled.QrCodeScanner,
                        androidx.compose.material.icons.Icons.Outlined.Notifications,
                        androidx.compose.material.icons.Icons.Outlined.Schedule
                    )

                    routes.forEachIndexed { index, route ->
                        val label = labels[index]
                        val iconFilled = iconsFilled[index]
                        val iconOutlined = iconsOutlined[index]
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
                                { Text(label, fontSize = 10.sp, fontWeight = if (selected) androidx.compose.ui.text.font.FontWeight.Bold else androidx.compose.ui.text.font.FontWeight.Medium) }
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
