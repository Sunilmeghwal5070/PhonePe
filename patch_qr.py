with open('/app/applet/app/src/main/java/com/example/ui/screens/QrScreen.kt', 'r') as f:
    content = f.read()

import re

# Add context import
if 'import androidx.compose.ui.platform.LocalContext' not in content:
    content = content.replace('import androidx.compose.runtime.Composable', 'import androidx.compose.ui.platform.LocalContext\nimport androidx.compose.runtime.Composable')

if 'import android.annotation.SuppressLint' not in content:
    content = content.replace('import androidx.compose.runtime.Composable', 'import android.annotation.SuppressLint\nimport androidx.compose.runtime.Composable')

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
                    val contextUpi = LocalContext.current
                    val upiRes = contextUpi.resources.getIdentifier("logo_upi", "drawable", contextUpi.packageName)
                    if (upiRes != 0) {
                        androidx.compose.foundation.Image(
                            painter = androidx.compose.ui.res.painterResource(id = upiRes),
                            contentDescription = "UPI",
                            modifier = Modifier.height(24.dp),
                            contentScale = androidx.compose.ui.layout.ContentScale.Fit
                        )
                    } else {
                        // Original generic box or icon
"""

# Wait, what was the content after Column?
# Let's check:
