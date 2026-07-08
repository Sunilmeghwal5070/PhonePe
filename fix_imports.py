with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    content = f.read()

content = content.replace("import androidx.compose.ui.draw.clip\nimport androidx.compose.ui.zIndex\nimport androidx.compose.ui.draw.clip\nimport androidx.compose.ui.zIndexToBounds", "import androidx.compose.ui.draw.clip\nimport androidx.compose.ui.zIndex\nimport androidx.compose.ui.draw.clipToBounds")

# And wait, the compiler also complained:
# e: file:///app/src/main/java/com/example/ui/screens/HomeScreen.kt:133:65 Unresolved reference. None of the following candidates is applicable because of a receiver type mismatch: val Icons.Filled.HelpOutline: ImageVector

content = content.replace("Icons.AutoMirrored.Filled.HelpOutline", "Icons.Default.HelpOutline")

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(content)
