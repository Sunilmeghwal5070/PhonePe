import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    text = f.read()

target = """    ShakeEffect {
        if (currentRoute != "qr") {
            navController.navigate("qr") {
                popUpTo("home")
                launchSingleTop = true
                restoreState = true
            }
        }
    }"""

replacement = """    val isShakeEnabled by prankViewModel.isShakeEnabled.collectAsState()
    if (isShakeEnabled) {
        ShakeEffect {
            if (currentRoute != "qr") {
                navController.navigate("qr") {
                    popUpTo("home")
                    launchSingleTop = true
                    restoreState = true
                }
            }
        }
    }"""

text = text.replace(target, replacement)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(text)
