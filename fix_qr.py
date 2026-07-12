import re

with open('app/src/main/java/com/example/ui/screens/QrScreen.kt', 'r') as f:
    text = f.read()

# Instead of regex, let's find the Box for Bank Logo
bank_box_start = text.find("// Bank Logo")
spacer_after = text.find("Spacer(modifier = Modifier.height(16.dp))", bank_box_start)

if bank_box_start != -1 and spacer_after != -1:
    new_box = """// Bank Logo
            Box(
                modifier = Modifier
                    .size(48.dp)
                    .border(1.dp, Color(0xFFE0E0E0), RoundedCornerShape(12.dp)),
                contentAlignment = Alignment.Center
            ) {
                coil.compose.AsyncImage(
                    model = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Union_Bank_of_India_Logo.svg/1024px-Union_Bank_of_India_Logo.svg.png",
                    contentDescription = "Bank Logo",
                    modifier = Modifier.fillMaxSize().padding(6.dp),
                    contentScale = androidx.compose.ui.layout.ContentScale.Fit
                )
            }
            
            """
    text = text[:bank_box_start] + new_box + text[spacer_after:]

with open('app/src/main/java/com/example/ui/screens/QrScreen.kt', 'w') as f:
    f.write(text)

