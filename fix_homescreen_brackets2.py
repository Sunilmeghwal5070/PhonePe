import re
with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    content = f.read()

# Replace the extra brackets before `// Dialog warnings/pranks`
pattern = r'            \}\n        \}\n    \}\n\}\n\n    // Dialog warnings/pranks'
replacement = r'            }\n        }\n    }\n\n    // Dialog warnings/pranks'
content = content.replace('            }\n        }\n    }\n}\n\n    // Dialog warnings/pranks', '    }\n\n    // Dialog warnings/pranks')

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(content)
