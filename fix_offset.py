import re

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    content = f.read()

# Remove duplicate imports
imports = []
new_lines = []
for line in content.split('\n'):
    if line.startswith('import '):
        if line not in imports:
            imports.append(line)
            new_lines.append(line)
    else:
        new_lines.append(line)

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write('\n'.join(new_lines))
