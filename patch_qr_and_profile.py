import re

with open("app/src/main/java/com/example/ui/screens/QrScreen.kt", "r") as f:
    content = f.read()

# Make the QR code bigger and denser
content = content.replace("val gridSize = 25", "val gridSize = 45")
content = content.replace("val blockSize = size.width / gridSize", "val blockSize = size.width / gridSize")
content = content.replace(".size(240.dp)", ".size(300.dp)")
# Increase the thickness of position squares
content = content.replace("val posSize = 6 * blockSize", "val posSize = 7 * blockSize")
content = content.replace("val innerSize = 2.5f * blockSize", "val innerSize = 3f * blockSize")

with open("app/src/main/java/com/example/ui/screens/QrScreen.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "r") as f:
    content = f.read()

# Add About PhonePe
about_item = """                    HorizontalDivider(color = Color(0xFFF0F0F0))
                    val context = androidx.compose.ui.platform.LocalContext.current
                    ProfileMenuItem(
                        icon = Icons.Default.Info,
                        title = "About PhonePe",
                        onClick = { android.widget.Toast.makeText(context, "developer by Sunil meghwal", android.widget.Toast.LENGTH_SHORT).show() }
                    )
                }
            }
"""
content = content.replace("                }\n            }", about_item)

# Fix white space at top
content = content.replace("Scaffold(", "Scaffold(\n        modifier = Modifier.fillMaxSize().background(Color(0xFF5f259f)),")

with open("app/src/main/java/com/example/ui/screens/ProfileScreen.kt", "w") as f:
    f.write(content)
