import re

with open('/app/applet/app/src/main/java/com/example/ui/screens/SplashScreen.kt', 'r') as f:
    content = f.read()

# Replace the Image block with the PhonePeLogo Composable
image_pattern = r'Image\(\s*painter = androidx\.compose\.ui\.res\.painterResource\(id = com\.example\.R\.drawable\.ic_launcher_foreground\),\s*contentDescription = "Logo",\s*contentScale = androidx\.compose\.ui\.layout\.ContentScale\.Crop,\s*modifier = Modifier\s*\.size\(125\.dp\)\s*\.clip\(CircleShape\)\s*\.background\(Color\.White\)\s*\)'

replacement = '''Box(
                modifier = Modifier
                    .size(100.dp)
                    .clip(CircleShape)
                    .background(PhonePePurple),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = "पे",
                    color = Color.White,
                    fontSize = 64.sp,
                    fontWeight = FontWeight.Bold
                )
            }'''

content = re.sub(image_pattern, replacement, content, flags=re.DOTALL)

with open('/app/applet/app/src/main/java/com/example/ui/screens/SplashScreen.kt', 'w') as f:
    f.write(content)
