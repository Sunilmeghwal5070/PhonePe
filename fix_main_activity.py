import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if i != 119 and 'prefsManager = prefsManager,' in line:
        if line.strip() == 'prefsManager = prefsManager,':
            continue
        else:
            line = line.replace('prefsManager = prefsManager, ', '')
    new_lines.append(line)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.writelines(new_lines)

