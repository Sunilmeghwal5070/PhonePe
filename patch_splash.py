with open('/app/applet/app/src/main/java/com/example/ui/screens/SplashScreen.kt', 'r') as f:
    content = f.read()

import re

# Add imports
imports = """import androidx.compose.ui.platform.LocalContext
import android.annotation.SuppressLint
"""
content = content.replace('import androidx.compose.runtime.Composable', imports + 'import androidx.compose.runtime.Composable')

new_logic = """
            val context = LocalContext.current
            val resourceId = context.resources.getIdentifier("logo_phonepe", "drawable", context.packageName)
            if (resourceId != 0) {
                Image(
                    painter = androidx.compose.ui.res.painterResource(id = resourceId),
                    contentDescription = "Logo",
                    contentScale = androidx.compose.ui.layout.ContentScale.Fit,
                    modifier = Modifier.size(150.dp)
                )
            } else {
                // Centered App Logo
                Image(
                    painter = androidx.compose.ui.res.painterResource(id = com.example.R.drawable.ic_launcher_foreground),
                    contentDescription = "Logo",
                    contentScale = androidx.compose.ui.layout.ContentScale.Crop,
                    modifier = Modifier
                        .size(125.dp)
                        .clip(CircleShape)
                        .background(PhonePePurple)
                )
                
                Spacer(modifier = Modifier.height(16.dp))
                
                // "PhonePe" Text below logo
                Text(
                    text = "PhonePe",
                    color = PhonePePurple,
                    fontSize = 42.sp,
                    fontWeight = FontWeight.ExtraBold,
                    fontFamily = FontFamily.SansSerif,
                    letterSpacing = (-1).sp
                )
            }
"""

content = re.sub(
    r'// Centered App Logo.*?letterSpacing = \(-1\)\.sp\s*\)',
    new_logic.strip(),
    content,
    flags=re.DOTALL
)

with open('/app/applet/app/src/main/java/com/example/ui/screens/SplashScreen.kt', 'w') as f:
    f.write(content)

