import re

with open('app/src/main/java/com/example/ui/screens/ReceiptScreen.kt', 'r') as f:
    text = f.read()

target = """                                    Box(
                                        modifier = Modifier
                                            .size(44.dp)
                                            .background(Color(0xFF5f259f), RoundedCornerShape(12.dp)),
                                        contentAlignment = Alignment.Center
                                    ) {
                                        Icon(
                                            imageVector = Icons.AutoMirrored.Filled.ArrowForward,
                                            contentDescription = null,
                                            tint = Color.White,
                                            modifier = Modifier.size(20.dp).rotate(if (currentTx.type == "PAID") -45f else 135f)
                                        )
                                    }"""

replacement = """                                    Box(
                                        modifier = Modifier
                                            .size(44.dp)
                                            .background(if (currentTx.type == "PAID") Color(0xFF29B6F6) else Color(0xFF5f259f), if (currentTx.type == "PAID") CircleShape else RoundedCornerShape(12.dp)),
                                        contentAlignment = Alignment.Center
                                    ) {
                                        if (currentTx.type == "PAID") {
                                            val initials = currentTx.receiverName.split(" ").mapNotNull { it.firstOrNull()?.uppercase() }.take(2).joinToString("")
                                            Text(initials, color = Color.White, fontSize = 18.sp, fontWeight = FontWeight.Bold)
                                        } else {
                                            Icon(
                                                imageVector = Icons.AutoMirrored.Filled.ArrowForward,
                                                contentDescription = null,
                                                tint = Color.White,
                                                modifier = Modifier.size(20.dp).rotate(135f)
                                            )
                                        }
                                    }"""

text = text.replace(target, replacement)

with open('app/src/main/java/com/example/ui/screens/ReceiptScreen.kt', 'w') as f:
    f.write(text)
