with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    text = f.read()

# Let's fix the end
import re
new_text = re.sub(r'\}\s*\}\s*\}\s*\}\s*$', '}\n}\n', text)

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(new_text)

