import re

with open('app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt', 'r') as f:
    content = f.read()

old_done = """        // Done Button at bottom
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 16.dp),
            contentAlignment = Alignment.Center
        ) {
            Button(
                onClick = onBack,
                modifier = Modifier
                    .fillMaxWidth(0.9f)
                    .height(48.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFF0F0F0)),
                shape = RoundedCornerShape(24.dp),
                elevation = ButtonDefaults.buttonElevation(0.dp)
            ) {
                Text("DONE", color = Color(0xFF5f259f), fontSize = 15.sp, fontWeight = FontWeight.Bold, letterSpacing = 0.5.sp)
            }
        }"""

new_done = """        // Done Button at bottom
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 24.dp, vertical = 16.dp),
            contentAlignment = Alignment.CenterEnd
        ) {
            Text(
                text = "DONE",
                color = Color(0xFF5f259f),
                fontSize = 16.sp,
                fontWeight = FontWeight.Bold,
                letterSpacing = 0.5.sp,
                modifier = Modifier.clickable(onClick = onBack).padding(8.dp)
            )
        }"""

content = content.replace(old_done, new_done)

with open('app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt', 'w') as f:
    f.write(content)
