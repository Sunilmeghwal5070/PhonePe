with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    content = f.read()

# We need to put `item` inside the LazyColumn, or rather, we were supposed to delete the My QR Button Section too?
# The user said "My QR code ke liye extra button mat karo QR code direct add karo wala page Pura"
# So I should remove the "My QR Button Section" completely.

pattern = r'item \{\s*// My QR Button Section.*?Spacer\(modifier = Modifier\.height\(24\.dp\)\)\s*\}\s*\}'
import re
content = re.sub(pattern, '}', content, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(content)
