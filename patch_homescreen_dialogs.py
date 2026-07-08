import re

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

# Replace all showDialogTitle = "..." with showDialogTitle = "" (or we can just leave it empty)
# Actually, if I remove them, what should the buttons do? 
# Maybe just show a Toast saying "Coming Soon" or do nothing.
# Let's replace the whole dialog display block.
dialog_pattern = r'if \(showDialogTitle\.isNotEmpty\(\)\) \{[\s\S]*?\}\s*\}'
content = re.sub(dialog_pattern, '', content)

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
