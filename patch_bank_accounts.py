import re

with open("app/src/main/java/com/example/ui/screens/BankAccountsScreen.kt", "r") as f:
    content = f.read()

pattern = r"""                                Box\(
                                    modifier = Modifier
                                        \.background\(Color\(0xFF388E3C\), RoundedCornerShape\(12\.dp\)\)
                                        \.padding\(horizontal = 8\.dp, vertical = 4\.dp\)
                                \) \{
                                    Text\("Primary", color = Color\.White, fontSize = 12\.sp, fontWeight = FontWeight\.Bold\)
                                \}"""

replacement = """                                Box(
                                    modifier = Modifier
                                        .background(Color(0xFF2E7D32), RoundedCornerShape(10.dp))
                                        .padding(horizontal = 8.dp, vertical = 2.dp)
                                ) {
                                    Text("Primary", color = Color.White, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                                }"""

content = re.sub(pattern, replacement, content)

with open("app/src/main/java/com/example/ui/screens/BankAccountsScreen.kt", "w") as f:
    f.write(content)
