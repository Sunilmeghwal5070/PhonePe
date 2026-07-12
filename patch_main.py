with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    text = f.read()

shake_effect = """
@Composable
fun ShakeEffect(onShake: () -> Unit) {
    val context = LocalContext.current
    val currentOnShake by rememberUpdatedState(onShake)
    
    DisposableEffect(context) {
        val sensorManager = context.getSystemService(android.content.Context.SENSOR_SERVICE) as android.hardware.SensorManager
        val accelerometer = sensorManager.getDefaultSensor(android.hardware.Sensor.TYPE_ACCELEROMETER)
        
        val shakeDetector = com.example.ShakeDetector {
            currentOnShake()
        }
        
        if (accelerometer != null) {
            sensorManager.registerListener(shakeDetector, accelerometer, android.hardware.SensorManager.SENSOR_DELAY_UI)
        }
        
        onDispose {
            sensorManager.unregisterListener(shakeDetector)
        }
    }
}
"""

if "fun ShakeEffect" not in text:
    text += shake_effect

# Add call to ShakeEffect in MainAppLayout
if "ShakeEffect {" not in text:
    target = "    val showBottomBar = currentRoute in listOf(\"home\", \"search\", \"qr\", \"alerts\", \"history\")"
    replacement = """
    val showBottomBar = currentRoute in listOf("home", "search", "qr", "alerts", "history")
    
    ShakeEffect {
        if (currentRoute != "qr") {
            navController.navigate("qr") {
                popUpTo("home")
                launchSingleTop = true
                restoreState = true
            }
        }
    }
"""
    text = text.replace(target, replacement)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(text)

