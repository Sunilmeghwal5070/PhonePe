with open('/app/applet/app/src/main/java/com/example/ui/screens/RechargeFlowScreens.kt', 'r') as f:
    content = f.read()

import re

# Add imports for animation if they don't exist
if 'import androidx.compose.animation.core.*' not in content:
    content = content.replace('import androidx.compose.runtime.*', 'import androidx.compose.runtime.*\nimport androidx.compose.animation.core.*\nimport androidx.compose.ui.draw.scale')

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
    'fun RechargeSuccessScreen(\n    amount: String,\n    name: String,\n    transactionId: Int,\n    onDone: () -> Unit\n) {',
    'fun RechargeSuccessScreen(\n    amount: String,\n    name: String,\n    transactionId: Int,\n    onDone: () -> Unit\n) {\n' + animation_logic
)

content = content.replace(
    '.size(100.dp)\n                .background(Color(0xFF4CAF50), CircleShape)',
    '.size(100.dp)\n                .scale(scale)\n                .background(Color(0xFF4CAF50), CircleShape)'
)

with open('/app/applet/app/src/main/java/com/example/ui/screens/RechargeFlowScreens.kt', 'w') as f:
    f.write(content)
