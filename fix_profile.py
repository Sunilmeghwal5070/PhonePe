import re

with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'r') as f:
    content = f.read()

# Add needed imports
imports = """import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import kotlin.random.Random
import androidx.compose.foundation.Canvas"""

if 'import androidx.compose.ui.geometry.Offset' not in content:
    content = content.replace('import androidx.compose.ui.Alignment', imports + '\nimport androidx.compose.ui.Alignment')

target = """                    Box(modifier = Modifier.size(200.dp).background(Color.White)) {
                        // Dummy QR Code Drawing
                        for (i in 0 until 10) {
                            for (j in 0 until 10) {
                                if ((i + j) % 2 == 0) {
                                    Box(modifier = Modifier.offset(x = (i * 20).dp, y = (j * 20).dp).size(20.dp).background(Color.Black))
                                }
                            }
                        }
                        // Center Logo
                        Box(
                            modifier = Modifier.align(Alignment.Center).size(48.dp).background(Color.White, CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Box(modifier = Modifier.size(40.dp).background(Color.Black, CircleShape), contentAlignment = Alignment.Center) {
                                Text("पे", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 24.sp)
                            }
                        }
                    }"""

replacement = """                    Box(modifier = Modifier.size(200.dp).background(Color.White)) {
                        Canvas(modifier = Modifier.fillMaxSize()) {
                            val blockSize = size.width / 25
                            // Draw corner squares
                            fun drawFinderPattern(x: Float, y: Float) {
                                drawRect(
                                    color = Color.Black,
                                    topLeft = Offset(x, y),
                                    size = Size(blockSize * 7, blockSize * 7)
                                )
                                drawRect(
                                    color = Color.White,
                                    topLeft = Offset(x + blockSize, y + blockSize),
                                    size = Size(blockSize * 5, blockSize * 5)
                                )
                                drawRect(
                                    color = Color.Black,
                                    topLeft = Offset(x + blockSize * 2, y + blockSize * 2),
                                    size = Size(blockSize * 3, blockSize * 3)
                                )
                            }
                            
                            drawFinderPattern(0f, 0f)
                            drawFinderPattern(size.width - blockSize * 7, 0f)
                            drawFinderPattern(0f, size.height - blockSize * 7)
                            
                            // Draw random blocks to simulate QR
                            val random = Random(42)
                            for (i in 0 until 25) {
                                for (j in 0 until 25) {
                                    // Avoid finder patterns
                                    val inTopLeft = i < 8 && j < 8
                                    val inTopRight = i > 16 && j < 8
                                    val inBottomLeft = i < 8 && j > 16
                                    // Avoid center for logo
                                    val inCenter = i in 10..14 && j in 10..14
                                    
                                    if (!inTopLeft && !inTopRight && !inBottomLeft && !inCenter) {
                                        if (random.nextBoolean()) {
                                            drawRect(
                                                color = Color.Black,
                                                topLeft = Offset(i * blockSize, j * blockSize),
                                                size = Size(blockSize, blockSize)
                                            )
                                        }
                                    }
                                }
                            }
                        }
                        
                        // Center Logo
                        Box(
                            modifier = Modifier.align(Alignment.Center).size(48.dp).background(Color.White, CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Box(modifier = Modifier.size(40.dp).background(Color.Black, CircleShape), contentAlignment = Alignment.Center) {
                                Text("पे", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 24.sp)
                            }
                        }
                    }"""

if target in content:
    content = content.replace(target, replacement)
    print("Replaced QR Code!")
else:
    print("QR Code Target not found!")

with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'w') as f:
    f.write(content)
