import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    text = f.read()

# I want to find the whole BottomNavigationBar composable
# Let's just match from "@Composable\nfun BottomNavigationBar" until the next composable or end.
pattern = re.compile(r'@Composable\nfun BottomNavigationBar.*?(?=@Composable|$)', re.DOTALL)
match = pattern.search(text)
if match:
    old_code = match.group(0)
    new_code = """@Composable
fun BottomNavigationBar(navController: NavHostController, currentRoute: String?) {
    NavigationBar(
        containerColor = Color.White,
        contentColor = PhonePeTextMuted,
        tonalElevation = 8.dp
    ) {
        val items = listOf(
            Triple("home", "Home", Icons.Default.Home),
            Triple("search", "Search", Icons.Default.Search)
        )
        val rightItems = listOf(
            Triple("alerts", "Alerts", Icons.Outlined.Notifications),
            Triple("history", "History", Icons.Default.History)
        )

        items.forEach { (route, label, icon) ->
            NavigationBarItem(
                selected = currentRoute == route,
                onClick = {
                    if (currentRoute != route) {
                        navController.navigate(route) {
                            popUpTo("home")
                            launchSingleTop = true
                        }
                    }
                },
                icon = { Icon(icon, contentDescription = label) },
                label = { Text(label, fontSize = 10.sp) },
                colors = NavigationBarItemDefaults.colors(
                    selectedIconColor = PhonePePurple,
                    unselectedIconColor = PhonePeTextMuted,
                    selectedTextColor = PhonePePurple,
                    unselectedTextColor = PhonePeTextMuted,
                    indicatorColor = Color.Transparent
                )
            )
        }

        // Center QR Button
        NavigationBarItem(
            selected = currentRoute == "qr",
            onClick = {
                navController.navigate("qr") {
                    popUpTo("home")
                    launchSingleTop = true
                }
            },
            icon = {
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
                        modifier = Modifier.size(24.dp)
                    )
                }
            },
            label = null, // No label for center button
            colors = NavigationBarItemDefaults.colors(
                indicatorColor = Color.Transparent
            )
        )

        rightItems.forEach { (route, label, icon) ->
            NavigationBarItem(
                selected = currentRoute == route,
                onClick = {
                    if (currentRoute != route) {
                        navController.navigate(route) {
                            popUpTo("home")
                            launchSingleTop = true
                        }
                    }
                },
                icon = {
                    if (route == "alerts") {
                        BadgedBox(
                            badge = {
                                Box(
                                    modifier = Modifier
                                        .size(10.dp)
                                        .background(PhonePeSuccessGreen, CircleShape)
                                        .border(1.dp, Color.White, CircleShape),
                                    contentAlignment = Alignment.Center
                                ) {
                                    Text("1", color = Color.White, fontSize = 6.sp, fontWeight = FontWeight.Bold)
                                }
                            }
                        ) {
                            Icon(icon, contentDescription = label)
                        }
                    } else {
                        Icon(icon, contentDescription = label)
                    }
                },
                label = { Text(label, fontSize = 10.sp) },
                colors = NavigationBarItemDefaults.colors(
                    selectedIconColor = PhonePePurple,
                    unselectedIconColor = PhonePeTextMuted,
                    selectedTextColor = PhonePePurple,
                    unselectedTextColor = PhonePeTextMuted,
                    indicatorColor = Color.Transparent
                )
            )
        }
    }
}
"""
    new_text = text.replace(old_code, new_code)
    with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
        f.write(new_text)
    print("Replaced!")
else:
    print("Not found!")

