import re

with open('app/src/main/java/com/example/ui/screens/ReceiptScreen.kt', 'r') as f:
    text = f.read()

target = """                                    Row(verticalAlignment = Alignment.CenterVertically) {
                                        Box(
                                            modifier = Modifier
                                                .size(32.dp)
                                                .border(1.dp, Color(0xFFEEEEEE), RoundedCornerShape(8.dp)),
                                            contentAlignment = Alignment.Center
                                        ) {
                                            Text(if (currentTx.type == "PAID") currentTx.senderBankName.take(1).uppercase() else currentTx.receiverName.take(1).uppercase(), color = Color(0xFFe31837), fontWeight = FontWeight.Bold, fontSize = 18.sp)
                                        }"""

replacement = """                                    Row(verticalAlignment = Alignment.CenterVertically) {
                                        Box(
                                            modifier = Modifier
                                                .size(32.dp)
                                                .border(1.dp, Color(0xFFEEEEEE), RoundedCornerShape(8.dp)),
                                            contentAlignment = Alignment.Center
                                        ) {
                                            coil.compose.AsyncImage(
                                                model = getBankLogoUrl(currentTx.senderBankName),
                                                contentDescription = "Bank Logo",
                                                modifier = Modifier.fillMaxSize().padding(4.dp),
                                                contentScale = androidx.compose.ui.layout.ContentScale.Fit
                                            )
                                        }"""

text = text.replace(target, replacement)

with open('app/src/main/java/com/example/ui/screens/ReceiptScreen.kt', 'w') as f:
    f.write(text)
