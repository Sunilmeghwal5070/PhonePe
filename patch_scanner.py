with open('/app/applet/app/src/main/java/com/example/ui/screens/ScannerScreen.kt', 'r') as f:
    content = f.read()

# Add LaunchedEffect
if 'import androidx.compose.runtime.LaunchedEffect' not in content:
    content = content.replace('import androidx.compose.runtime.getValue', 'import androidx.compose.runtime.getValue\nimport androidx.compose.runtime.LaunchedEffect\nimport kotlinx.coroutines.delay')

old_scanner_box = '''    val infiniteTransition = rememberInfiniteTransition(label = "scanner")'''
new_scanner_box = '''    LaunchedEffect(Unit) {
        delay(2500)
        onScanComplete()
    }
    val infiniteTransition = rememberInfiniteTransition(label = "scanner")'''

if old_scanner_box in content:
    content = content.replace(old_scanner_box, new_scanner_box)

with open('/app/applet/app/src/main/java/com/example/ui/screens/ScannerScreen.kt', 'w') as f:
    f.write(content)
