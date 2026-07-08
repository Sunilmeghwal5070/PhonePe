import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Add launcher definition
launcher_def = """    val currentRoute = navBackStackEntry?.destination?.route

    val permissionLauncher = androidx.activity.compose.rememberLauncherForActivityResult(
        androidx.activity.result.contract.ActivityResultContracts.RequestMultiplePermissions()
    ) { _ ->
        navController.navigate("qr") {
            popUpTo("home")
            launchSingleTop = true
            restoreState = true
        }
    }"""

content = content.replace("    val currentRoute = navBackStackEntry?.destination?.route", launcher_def)

# Replace the click listener for qr
old_click = """                                        .clickable {
                                            navController.navigate(route) {
                                                popUpTo("home")
                                                launchSingleTop = true
                                                restoreState = true
                                            }
                                        },"""

new_click = """                                        .clickable {
                                            val permissions = if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.TIRAMISU) {
                                                arrayOf(android.Manifest.permission.CAMERA, android.Manifest.permission.READ_MEDIA_IMAGES)
                                            } else {
                                                arrayOf(android.Manifest.permission.CAMERA, android.Manifest.permission.READ_EXTERNAL_STORAGE)
                                            }
                                            permissionLauncher.launch(permissions)
                                        },"""

content = content.replace(old_click, new_click)

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
