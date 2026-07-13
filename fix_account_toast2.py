import re

with open('app/src/main/java/com/example/ui/screens/AccountDetailsScreen.kt', 'r') as f:
    text = f.read()

target = """            if (showAdDialog && account != null) {
                var adProgress by remember { mutableStateOf(5) }
                
                androidx.compose.runtime.LaunchedEffect(Unit) {"""

replacement = """            if (showAdDialog && account != null) {
                var adProgress by remember { mutableStateOf(5) }
                val context = androidx.compose.ui.platform.LocalContext.current
                androidx.compose.runtime.LaunchedEffect(Unit) {"""

text = text.replace(target, replacement)
text = text.replace("android.widget.Toast.makeText(androidx.compose.ui.platform.LocalContext.current,", "android.widget.Toast.makeText(context,")

with open('app/src/main/java/com/example/ui/screens/AccountDetailsScreen.kt', 'w') as f:
    f.write(text)
