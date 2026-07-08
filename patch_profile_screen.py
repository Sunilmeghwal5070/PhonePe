import re

with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "r") as f:
    content = f.read()

# I will remove the divider and ProfileMenuItem from the header Row
pattern_to_remove = r"HorizontalDivider\(color = Color\(0xFFF0F0F0\)\)\s*val context = androidx\.compose\.ui\.platform\.LocalContext\.current\s*ProfileMenuItem\(\s*icon = Icons\.Default\.Info,\s*title = \"About PhonePe\",\s*onClick = \{[^\}]*\}\s*\)"
content = re.sub(pattern_to_remove, "", content)

# I'll also ensure the Row handles content cleanly.
with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "w") as f:
    f.write(content)
