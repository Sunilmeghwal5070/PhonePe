with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    content = f.read()

# Add import
if 'import androidx.compose.animation.animateContentSize' not in content:
    content = content.replace('import androidx.compose.animation.core.*', 'import androidx.compose.animation.core.*\nimport androidx.compose.animation.animateContentSize\nimport kotlinx.coroutines.delay')

# Change Profile onClick to QR
content = content.replace('Toast.makeText(context, "Profile Settings", Toast.LENGTH_SHORT).show()', 'onNavigateToQr()')

# Text changes
content = content.replace('"Your Prank Space"', '"Your Space"')
help_text_old = 'showDialogText = "With the help of this Prank Clone you can play fun pranks on your friends. Just click on \'Money Transfer\' and show them a fake success screen!"'
help_text_new = 'showDialogText = "Here you can manage your settings. Click on \'Money Transfer\' to proceed!"'
content = content.replace(help_text_old, help_text_new)

ref_old = 'showDialogText = "Share the link of this prank clone with your friends and get a fictional ₹200! 🤑🔥"'
ref_new = 'showDialogText = "Share the link of this app with your friends and get ₹200! 🤑🔥"'
content = content.replace(ref_old, ref_new)

bb_old = 'showDialogText = "Your actual prank balance is ₹1,45,392.50. You have been declared the richest person in this area! 👑💥"'
bb_new = 'showDialogText = "Your actual balance is ₹1,45,392.50. Keep it up! 👑💥"'
content = content.replace(bb_old, bb_new)

tf_old = 'Toast.makeText(context, "Tuition fees paid in prank!", Toast.LENGTH_SHORT).show()'
tf_new = 'Toast.makeText(context, "Tuition fees paid!", Toast.LENGTH_SHORT).show()'
content = content.replace(tf_old, tf_new)

formula_old = '''                    // Formula Block
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 8.dp)
                            .border(1.dp, Color(0xFF5f259f).copy(alpha = 0.8f), RoundedCornerShape(12.dp))
                            .background(Color(0xFF1E033A).copy(alpha = 0.8f))
                            .padding(horizontal = 14.dp, vertical = 10.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceEvenly
                    ) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Text("₹100", color = Color.White, fontSize = 24.sp, fontWeight = FontWeight.ExtraBold)
                            Text("balance", color = Color.LightGray, fontSize = 11.sp)
                        }

                        Text("=", color = Color(0xFFCCFF00), fontSize = 28.sp, fontWeight = FontWeight.Bold)

                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Text("₹500", color = Color.White, fontSize = 24.sp, fontWeight = FontWeight.ExtraBold)
                            Text("in buying power", color = Color.LightGray, fontSize = 11.sp)
                        }
                    }'''

formula_new = '''                    // Formula Block Animation State
                    var animationStep by remember { mutableIntStateOf(0) }
                    LaunchedEffect(Unit) {
                        while (true) {
                            animationStep = 0
                            delay(1500)
                            animationStep = 1
                            delay(3000)
                        }
                    }

                    // Formula Block
                    Row(
                        modifier = Modifier
                            .animateContentSize()
                            .padding(horizontal = 8.dp)
                            .border(1.dp, Color(0xFF5f259f).copy(alpha = 0.8f), RoundedCornerShape(12.dp))
                            .background(Color(0xFF1E033A).copy(alpha = 0.8f))
                            .padding(horizontal = 14.dp, vertical = 10.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.Center
                    ) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Text("₹100", color = Color.White, fontSize = 24.sp, fontWeight = FontWeight.ExtraBold)
                            Text("balance", color = Color.LightGray, fontSize = 11.sp)
                        }

                        if (animationStep >= 1) {
                            Spacer(modifier = Modifier.width(16.dp))
                            Text("=", color = Color(0xFFCCFF00), fontSize = 28.sp, fontWeight = FontWeight.Bold)
                            Spacer(modifier = Modifier.width(16.dp))
                            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                Text("₹500", color = Color.White, fontSize = 24.sp, fontWeight = FontWeight.ExtraBold)
                                Text("in buying power", color = Color.LightGray, fontSize = 11.sp)
                            }
                        }
                    }'''
content = content.replace(formula_old, formula_new)

content = content.replace("prank balance", "balance")
content = content.replace("Prank Clone", "App")
content = content.replace("Had fun! 😂", "Paid successfully! ✅")
content = content.replace("Make a new prank payment to prank your friends!", "Make a new payment")

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(content)
