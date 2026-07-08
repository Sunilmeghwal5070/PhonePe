import re

with open("app/src/main/java/com/example/ui/screens/QrScreen.kt", "r") as f:
    content = f.read()

pattern = r"""val contextUpi = LocalContext\.current\s*val upiRes = contextUpi\.resources\.getIdentifier\("logo_upi", "drawable", contextUpi\.packageName\)\s*if \(upiRes != 0\) \{\s*Column\(horizontalAlignment = Alignment\.CenterHorizontally\) \{\s*Text\("Powered by", color = Color\.Gray, fontSize = 10\.sp\)\s*androidx\.compose\.foundation\.Image\(\s*painter = androidx\.compose\.ui\.res\.painterResource\(id = upiRes\),\s*contentDescription = "UPI",\s*modifier = Modifier\.height\(20\.dp\),\s*contentScale = androidx\.compose\.ui\.layout\.ContentScale\.Fit\s*\)\s*\}\s*\} else \{\s*Column \{\s*Text\("Powered by", color = Color\.Gray, fontSize = 10\.sp\)\s*Text\("UPI", fontWeight = FontWeight\.Bold, fontSize = 14\.sp, fontStyle = androidx\.compose\.ui\.text\.font\.FontStyle\.Italic, color = Color\.Gray\)\s*\}\s*\}"""

replacement = """Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Text("Powered by", color = Color.Gray, fontSize = 10.sp)
                            coil.compose.AsyncImage(
                                model = coil.request.ImageRequest.Builder(androidx.compose.ui.platform.LocalContext.current)
                                    .data("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/UPI-Logo-vector.svg/1024px-UPI-Logo-vector.svg.png")
                                    .crossfade(true)
                                    .build(),
                                contentDescription = "UPI",
                                modifier = Modifier.height(20.dp),
                                contentScale = androidx.compose.ui.layout.ContentScale.Fit
                            )
                        }"""

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/QrScreen.kt", "w") as f:
    f.write(content)
