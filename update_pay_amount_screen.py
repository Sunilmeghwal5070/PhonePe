import re

with open('app/src/main/java/com/example/ui/screens/PayAmountScreen.kt', 'r') as f:
    text = f.read()

target = """                        Column {
                            Text(payeeName, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Text("Banking name: $payeeName", color = Color.Gray, fontSize = 14.sp)
                                Spacer(modifier = Modifier.width(4.dp))
                                Icon(Icons.Default.CheckCircle, contentDescription = null, tint = Color(0xFF388E3C), modifier = Modifier.size(14.dp))
                            }
                        }"""

replacement = """                        Column {
                            Text(payeeName.replace("+", " ").replace("%20", " "), fontWeight = FontWeight.Bold, fontSize = 16.sp)
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Text(upiId, color = Color.Gray, fontSize = 14.sp)
                            }
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Text("Banking name: ${payeeName.replace("+", " ").replace("%20", " ")}", color = Color.Gray, fontSize = 12.sp)
                                Spacer(modifier = Modifier.width(4.dp))
                                Icon(Icons.Default.CheckCircle, contentDescription = null, tint = Color(0xFF388E3C), modifier = Modifier.size(14.dp))
                            }
                        }"""
text = text.replace(target, replacement)

target2 = """Text(payeeName.take(2).uppercase(), color = Color.White, fontSize = 18.sp)"""
replacement2 = """Text(payeeName.replace("+", "").replace("%20", "").take(2).uppercase(), color = Color.White, fontSize = 18.sp)"""
text = text.replace(target2, replacement2)

with open('app/src/main/java/com/example/ui/screens/PayAmountScreen.kt', 'w') as f:
    f.write(text)
