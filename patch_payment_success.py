with open('/app/applet/app/src/main/java/com/example/ui/screens/PaymentSuccessScreen.kt', 'r') as f:
    content = f.read()

import re

# Add imports for animation
imports = """import androidx.compose.animation.core.*
import androidx.compose.runtime.getValue
import androidx.compose.ui.draw.scale
"""

content = content.replace('import androidx.compose.runtime.Composable', imports + 'import androidx.compose.runtime.Composable')

# Add animation logic
animation_logic = """
    val infiniteTransition = rememberInfiniteTransition()
    val scale by infiniteTransition.animateFloat(
        initialValue = 1f,
        targetValue = 1.15f,
        animationSpec = infiniteRepeatable(
            animation = tween(800, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        )
    )
"""

content = content.replace(
    'val currentTime = SimpleDateFormat("dd MMMM yyyy \'at\' hh:mm a", Locale.getDefault()).format(Date())',
    'val currentTime = SimpleDateFormat("dd MMMM yyyy \'at\' hh:mm a", Locale.getDefault()).format(Date())\n' + animation_logic
)

content = content.replace(
    '.size(80.dp)',
    '.size(80.dp)\n                .scale(scale)'
)

with open('/app/applet/app/src/main/java/com/example/ui/screens/PaymentSuccessScreen.kt', 'w') as f:
    f.write(content)
