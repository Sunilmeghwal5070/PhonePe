with open('/app/applet/app/src/main/java/com/example/ui/screens/PaymentSuccessScreen.kt', 'r') as f:
    content = f.read()

import re

# Add MediaPlayer import
content = content.replace(
    'import androidx.compose.animation.core.*',
    'import androidx.compose.animation.core.*\nimport android.media.MediaPlayer\nimport androidx.compose.ui.platform.LocalContext\nimport androidx.compose.runtime.LaunchedEffect'
)

sound_logic = """
    val context = LocalContext.current
    LaunchedEffect(Unit) {
        val resourceId = context.resources.getIdentifier("payment_success", "raw", context.packageName)
        if (resourceId != 0) {
            try {
                val mediaPlayer = MediaPlayer.create(context, resourceId)
                mediaPlayer.start()
                mediaPlayer.setOnCompletionListener {
                    it.release()
                }
            } catch (e: Exception) {
                // Ignore
            }
        }
    }
"""

content = content.replace(
    'val infiniteTransition = rememberInfiniteTransition()',
    sound_logic + '\n    val infiniteTransition = rememberInfiniteTransition()'
)

with open('/app/applet/app/src/main/java/com/example/ui/screens/PaymentSuccessScreen.kt', 'w') as f:
    f.write(content)
