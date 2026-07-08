import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Replace NavHost startDestination and remove splash composable
navhost_pattern = re.compile(r'NavHost\(\s*navController = navController,\s*startDestination = "splash",')
if not navhost_pattern.search(content):
    print("NavHost startDestination splash not found")
else:
    content = navhost_pattern.sub('NavHost(\n            navController = navController,\n            startDestination = "home",', content)

splash_composable = """            composable("splash") {
                SplashScreen(
                    onTimeout = {
                        navController.navigate("home") {
                            popUpTo("splash") { inclusive = true }
                        }
                    }
                )
            }
"""
content = content.replace(splash_composable, "")

# Add var showSplash
scaffold_pattern = r'    Scaffold\('
show_splash_code = """    var showSplash by remember { mutableStateOf(true) }

    if (showSplash) {
        SplashScreen(onTimeout = { showSplash = false })
        return
    }

    Scaffold("""
content = content.replace('    Scaffold(', show_splash_code)

# Add missing import for getStartDestination
if 'import androidx.navigation.NavGraph.Companion.findStartDestination' not in content:
    content = content.replace('import androidx.navigation.compose.rememberNavController', 'import androidx.navigation.compose.rememberNavController\nimport androidx.navigation.NavGraph.Companion.findStartDestination')

# Fix popUpTo in NavigationBar
# Find popUpTo("home") and replace with popUpTo(navController.graph.findStartDestination().id)
content = content.replace('popUpTo("home") { saveState = true }', 'popUpTo(navController.graph.findStartDestination().id) { saveState = true }')

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

print("Splash fixed")
