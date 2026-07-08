with open('/app/applet/app/src/main/java/com/example/ui/screens/RechargeFlowScreens.kt', 'r') as f:
    content = f.read()

sound_logic = """
    val context = LocalContext.current
    LaunchedEffect(Unit) {
        val resourceId = context.resources.getIdentifier("payment_success", "raw", context.packageName)
        if (resourceId != 0) {
            try {
                val mediaPlayer = android.media.MediaPlayer.create(context, resourceId)
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

with open('/app/applet/app/src/main/java/com/example/ui/screens/RechargeFlowScreens.kt', 'w') as f:
    f.write(content)
