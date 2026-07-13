import re

with open('app/src/main/java/com/example/ui/screens/AccountDetailsScreen.kt', 'r') as f:
    text = f.read()

text = text.replace("android.widget.Toast.makeText(context,", "android.widget.Toast.makeText(androidx.compose.ui.platform.LocalContext.current,")

with open('app/src/main/java/com/example/ui/screens/AccountDetailsScreen.kt', 'w') as f:
    f.write(text)
