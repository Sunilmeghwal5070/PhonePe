import re

with open('app/src/main/java/com/example/ui/screens/WrongPinScreen.kt', 'r') as f:
    text = f.read()

target = """            Text(
                text = if (errorTitle.contains("Insufficient", ignoreCase = true)) "Insufficient Balance" else "Wrong UPI PIN",
                fontSize = 24.sp,
                fontWeight = FontWeight.Bold,
                color = Color.Black
            )
            Spacer(modifier = Modifier.height(16.dp))"""

replacement = """            Text(
                text = if (errorTitle.contains("Insufficient", ignoreCase = true)) "Insufficient Balance" else "Wrong UPI PIN",
                fontSize = 24.sp,
                fontWeight = FontWeight.Bold,
                color = Color.Black
            )
            if (!errorTitle.contains("Insufficient", ignoreCase = true)) {
                Text("Hint: The default PIN is 1234 (change it in Bank Accounts).", fontSize = 12.sp, color = Color.Gray)
            }
            Spacer(modifier = Modifier.height(16.dp))"""

text = text.replace(target, replacement)

with open('app/src/main/java/com/example/ui/screens/WrongPinScreen.kt', 'w') as f:
    f.write(text)
