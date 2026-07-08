import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

import_statement = """import com.example.ui.screens.AppLockScreen\nimport androidx.compose.runtime.getValue\nimport androidx.compose.runtime.setValue\nimport androidx.compose.runtime.mutableStateOf\nimport androidx.compose.runtime.remember"""
content = content.replace("import com.example.ui.screens.HistoryScreen", import_statement + "\nimport com.example.ui.screens.HistoryScreen")

nav_host_start = r"""        NavHost\(
            navController = navController,
            startDestination = "splash"
        \) \{"""

nav_host_replacement = """        var isUnlocked by remember { mutableStateOf(false) }

        if (!isUnlocked) {
            AppLockScreen(onUnlocked = { isUnlocked = true })
        } else {
            NavHost(
                navController = navController,
                startDestination = "splash"
            ) {"""

content = re.sub(nav_host_start, nav_host_replacement, content)

# We need to add one more brace at the end of the NavHost block to close the else block
# Let's find the end of NavHost.
old_end = r"""            composable\("profile"\) \{
                ProfileScreen\(
                    viewModel = prankViewModel,
                    onBack = \{ navController\.popBackStack\(\) \},
                    onNavigateToEditDetails = \{ navController\.navigate\("edit_details"\) \},
                    onNavigateToAccountDetails = \{ navController\.navigate\("bank_accounts"\) \}
                \)
            \}
        \}
    \}
\}"""

new_end = """            composable("profile") {
                ProfileScreen(
                    viewModel = prankViewModel,
                    onBack = { navController.popBackStack() },
                    onNavigateToEditDetails = { navController.navigate("edit_details") },
                    onNavigateToAccountDetails = { navController.navigate("bank_accounts") }
                )
            }
        }
        }
    }
}"""

content = re.sub(old_end, new_end, content)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
