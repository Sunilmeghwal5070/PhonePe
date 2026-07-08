import re

with open("app/src/main/java/com/example/ui/screens/ReceiptScreen.kt", "r") as f:
    content = f.read()

# Fix 'Received from' text to handle Paid vs Received
old_received = 'Text("Received from", fontWeight = FontWeight.Bold, fontSize = 16.sp, color = Color.Black)'
new_received = 'Text(if (currentTx.type == "PAID") "Paid to" else "Received from", fontWeight = FontWeight.Bold, fontSize = 16.sp, color = Color.Black)'
content = content.replace(old_received, new_received)

# Fix the Arrow icon
old_arrow_box = """                                        Icon(
                                            imageVector = Icons.Default.ArrowBack, // Rotate to look like CallReceived
                                            contentDescription = null,
                                            tint = Color.White,
                                            modifier = Modifier.size(20.dp).rotate(-45f)
                                        )"""
new_arrow_box = """                                        Icon(
                                            imageVector = Icons.AutoMirrored.Filled.ArrowForward,
                                            contentDescription = null,
                                            tint = Color.White,
                                            modifier = Modifier.size(20.dp).rotate(if (currentTx.type == "PAID") -45f else 135f)
                                        )"""
content = content.replace(old_arrow_box, new_arrow_box)

# Fix Transfer details Debited from vs Credited to
old_credited = 'Text("Credited to", fontSize = 12.sp, color = Color.Gray)'
new_credited = 'Text(if (currentTx.type == "PAID") "Debited from" else "Credited to", fontSize = 12.sp, color = Color.Gray)'
content = content.replace(old_credited, new_credited)

# Also fix the name below Credited to
old_sunil = 'Text("Sunil", fontSize = 15.sp, color = Color.DarkGray)'
new_sunil = 'Text(if (currentTx.type == "PAID") "XXXXXXX${currentTx.senderBankAccountLast4}" else "XXXXXXX${currentTx.receiverPhone.takeLast(4)}", fontSize = 15.sp, color = Color.DarkGray)'
content = content.replace(old_sunil, new_sunil)

# Also the initial 'S' logic
old_s_logic = 'Text("S", color = Color(0xFFe31837), fontWeight = FontWeight.Bold, fontSize = 18.sp)'
new_s_logic = 'Text(if (currentTx.type == "PAID") currentTx.senderBankName.take(1).uppercase() else currentTx.receiverName.take(1).uppercase(), color = Color(0xFFe31837), fontWeight = FontWeight.Bold, fontSize = 18.sp)'
content = content.replace(old_s_logic, new_s_logic)

with open("app/src/main/java/com/example/ui/screens/ReceiptScreen.kt", "w") as f:
    f.write(content)
