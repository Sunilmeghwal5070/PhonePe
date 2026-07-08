import re

with open("app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt", "r") as f:
    content = f.read()

pattern = r'Text\("UPI", fontWeight = FontWeight\.Bold, fontStyle = FontStyle\.Italic, fontSize = 24\.sp, color = Color\(0xFF666666\)\)\s*Icon\(Icons\.Default\.PlayArrow, contentDescription = null, tint = Color\(0xFF168039\), modifier = Modifier\.size\(20\.dp\)\)'

replacement = """coil.compose.AsyncImage(
                        model = coil.request.ImageRequest.Builder(androidx.compose.ui.platform.LocalContext.current)
                            .data("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/UPI-Logo-vector.svg/1024px-UPI-Logo-vector.svg.png")
                            .crossfade(true)
                            .build(),
                        contentDescription = "UPI",
                        modifier = Modifier.height(24.dp),
                        contentScale = androidx.compose.ui.layout.ContentScale.Fit
                    )"""

content = re.sub(pattern, replacement, content)

with open("app/src/main/java/com/example/ui/screens/CheckBalanceScreen.kt", "w") as f:
    f.write(content)
