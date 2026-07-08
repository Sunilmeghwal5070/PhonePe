import re

with open("app/src/main/java/com/example/ui/screens/RechargeReminderDialog.kt", "r") as f:
    content = f.read()

# Replace border modifier
pattern = r"""\.border\(3\.dp, Color\.White, CircleShape\)"""
replacement = """.border(width = 3.dp, color = Color.White, shape = CircleShape)"""
content = re.sub(pattern, replacement, content)

with open("app/src/main/java/com/example/ui/screens/RechargeReminderDialog.kt", "w") as f:
    f.write(content)
