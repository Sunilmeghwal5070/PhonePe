with open("app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt", "r") as f:
    content = f.read()

content = content.replace(
    "HorizontalDivider(color = Color(0xFFF5F5F5), thickness = 1.dp, modifier = Modifier.padding(start = 72.dp))\n            HorizontalDivider(color = Color(0xFFF5F5F5), thickness = 1.dp, modifier = Modifier.padding(start = 72.dp))",
    "HorizontalDivider(color = Color(0xFFF5F5F5), thickness = 1.dp, modifier = Modifier.padding(start = 72.dp))"
)

with open("app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt", "w") as f:
    f.write(content)
