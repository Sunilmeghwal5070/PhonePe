import re

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    content = f.read()

content = content.replace('import androidx.compose.ui.draw.clip', 'import androidx.compose.ui.draw.clip\nimport androidx.compose.ui.zIndex')

target = """                // Top App Bar Overlay
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 14.dp, vertical = 10.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Box(
                        modifier = Modifier
                            .size(40.dp)
                            .clickable { onNavigateToProfile() }
                    ) {
                        Box(
                            modifier = Modifier
                                .size(36.dp)
                                .clip(CircleShape)
                                .background(Color(0xFFFBC02D)),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(
                                text = if (userProfile.name.isNotBlank()) userProfile.name.first().toString().uppercase() else "Y",
                                color = Color.White,
                                fontWeight = FontWeight.Bold,
                                fontSize = 18.sp
                            )
                        }
                        Box(
                            modifier = Modifier
                                .size(16.dp)
                                .align(Alignment.BottomEnd)
                                .clip(CircleShape)
                                .background(Color.White)
                                .border(1.dp, Color.LightGray, CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = Icons.Default.QrCode,
                                contentDescription = null,
                                tint = Color(0xFF5f259f),
                                modifier = Modifier.size(10.dp)
                            )
                        }
                    }
                    Icon(
                        imageVector = Icons.Default.HelpOutline,"""

replacement = """                // Top App Bar Overlay
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .zIndex(1f) // Ensures this Row renders above the grid animation
                        .padding(horizontal = 14.dp, vertical = 10.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Box(
                        modifier = Modifier
                            .size(52.dp)
                            .clickable { onNavigateToProfile() },
                        contentAlignment = Alignment.Center
                    ) {
                        Box(
                            modifier = Modifier
                                .size(48.dp)
                                .clip(CircleShape)
                                .background(Color(0xFFFBC02D)),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(
                                text = if (userProfile.name.isNotBlank()) userProfile.name.first().toString().uppercase() else "Y",
                                color = Color.White,
                                fontWeight = FontWeight.Bold,
                                fontSize = 24.sp
                            )
                        }
                        Box(
                            modifier = Modifier
                                .size(20.dp)
                                .align(Alignment.BottomEnd)
                                .clip(CircleShape)
                                .background(Color.White)
                                .border(1.dp, Color.LightGray, CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = Icons.Default.QrCode,
                                contentDescription = null,
                                tint = Color(0xFF5f259f),
                                modifier = Modifier.size(12.dp)
                            )
                        }
                    }
                    Icon(
                        imageVector = Icons.AutoMirrored.Filled.HelpOutline,"""

if target in content:
    content = content.replace(target, replacement)
    print("Replaced Header!")
else:
    print("Header Target not found!")
    
with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(content)
