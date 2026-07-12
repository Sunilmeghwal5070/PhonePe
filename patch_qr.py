import re

with open('app/src/main/java/com/example/ui/screens/QrScreen.kt', 'r') as f:
    text = f.read()

pattern = re.compile(r'// Union Bank logo approximation.*?\}', re.DOTALL)
new_code = """coil.compose.AsyncImage(
                    model = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Union_Bank_of_India_Logo.svg/1024px-Union_Bank_of_India_Logo.svg.png",
                    contentDescription = "Bank Logo",
                    modifier = Modifier.fillMaxSize().padding(6.dp),
                    contentScale = androidx.compose.ui.layout.ContentScale.Fit
                )"""

text = pattern.sub(new_code, text)

with open('app/src/main/java/com/example/ui/screens/QrScreen.kt', 'w') as f:
    f.write(text)

