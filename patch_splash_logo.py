import re

with open('/app/applet/app/src/main/java/com/example/ui/screens/SplashScreen.kt', 'r') as f:
    content = f.read()

box_pattern = r'Box\(\s*modifier = Modifier\s*\.size\(100\.dp\)\s*\.clip\(CircleShape\)\s*\.background\(PhonePePurple\),\s*contentAlignment = Alignment\.Center\s*\)\s*\{\s*Text\(\s*text = "पे",\s*color = Color\.White,\s*fontSize = 64\.sp,\s*fontWeight = FontWeight\.Bold\s*\)\s*\}'

replacement = '''Image(
                painter = androidx.compose.ui.res.painterResource(id = com.example.R.drawable.ic_launcher_foreground),
                contentDescription = "Logo",
                contentScale = androidx.compose.ui.layout.ContentScale.Crop,
                modifier = Modifier
                    .size(125.dp)
                    .clip(CircleShape)
                    .background(PhonePePurple)
            )'''

content = re.sub(box_pattern, replacement, content, flags=re.DOTALL)

with open('/app/applet/app/src/main/java/com/example/ui/screens/SplashScreen.kt', 'w') as f:
    f.write(content)

