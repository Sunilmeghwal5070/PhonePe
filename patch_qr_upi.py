with open('/app/applet/app/src/main/java/com/example/ui/screens/QrScreen.kt', 'r') as f:
    content = f.read()

import re

new_logic = """
                    Column {
                        Text("Supported on all UPI apps", color = Color.Gray, fontSize = 12.sp)
                        Spacer(modifier = Modifier.height(8.dp))
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            val context = LocalContext.current
                            val ppRes = context.resources.getIdentifier("logo_phonepe", "drawable", context.packageName)
                            if (ppRes != 0) {
                                androidx.compose.foundation.Image(
                                    painter = androidx.compose.ui.res.painterResource(id = ppRes),
                                    contentDescription = "PhonePe",
                                    modifier = Modifier.height(16.dp),
                                    contentScale = androidx.compose.ui.layout.ContentScale.Fit
                                )
                            } else {
                                Text("पे PhonePe", fontWeight = FontWeight.Bold, color = Color.Gray, fontSize = 12.sp)
                            }
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("BHIM", fontWeight = FontWeight.Bold, color = Color.Gray, fontSize = 12.sp, fontStyle = androidx.compose.ui.text.font.FontStyle.Italic)
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("G Pay", fontWeight = FontWeight.Bold, color = Color.Gray, fontSize = 12.sp)
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("Paytm", fontWeight = FontWeight.Bold, color = Color.Gray, fontSize = 12.sp)
                        }
                    }
                    
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Box(
                            modifier = Modifier
                                .width(1.dp)
                                .height(32.dp)
                                .background(Color.LightGray)
                        )
                        Spacer(modifier = Modifier.width(16.dp))
                        val contextUpi = LocalContext.current
                        val upiRes = contextUpi.resources.getIdentifier("logo_upi", "drawable", contextUpi.packageName)
                        if (upiRes != 0) {
                            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                Text("Powered by", color = Color.Gray, fontSize = 10.sp)
                                androidx.compose.foundation.Image(
                                    painter = androidx.compose.ui.res.painterResource(id = upiRes),
                                    contentDescription = "UPI",
                                    modifier = Modifier.height(20.dp),
                                    contentScale = androidx.compose.ui.layout.ContentScale.Fit
                                )
                            }
                        } else {
                            Column {
                                Text("Powered by", color = Color.Gray, fontSize = 10.sp)
                                Text("UPI", fontWeight = FontWeight.Bold, fontSize = 14.sp, fontStyle = androidx.compose.ui.text.font.FontStyle.Italic, color = Color.Gray)
                            }
                        }
                    }
"""

content = re.sub(
    r'Column \{\s*Text\("Supported on all UPI apps".*?Text\("UPI", fontWeight = FontWeight.Bold, fontSize = 14.sp, fontStyle = androidx.compose.ui.text.font.FontStyle.Italic, color = Color.Gray\)\s*\}\s*\}',
    new_logic.strip(),
    content,
    flags=re.DOTALL
)

with open('/app/applet/app/src/main/java/com/example/ui/screens/QrScreen.kt', 'w') as f:
    f.write(content)

