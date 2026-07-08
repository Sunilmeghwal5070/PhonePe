import re

with open("app/src/main/java/com/example/ui/screens/SplashScreen.kt", "r") as f:
    content = f.read()

pattern = r"""        // Centered Main Logo
        Column\(
            modifier = Modifier\.align\(Alignment\.Center\),
            horizontalAlignment = Alignment\.CenterHorizontally
        \) \{
            val context = LocalContext\.current
            val resourceId = context\.resources\.getIdentifier\("logo_phonepe", "drawable", context\.packageName\)
            if \(resourceId != 0\) \{
                Image\(
                    painter = androidx\.compose\.ui\.res\.painterResource\(id = resourceId\),
                    contentDescription = "Logo",
                    contentScale = androidx\.compose\.ui\.layout\.ContentScale\.Fit,
                    modifier = Modifier\.size\(150\.dp\)\.clip\(CircleShape\)
                \)
            \} else \{
                // Centered App Logo
                Image\(
                    painter = androidx\.compose\.ui\.res\.painterResource\(id = com\.example\.R\.drawable\.ic_launcher_foreground\),
                    contentDescription = "Logo",
                    contentScale = androidx\.compose\.ui\.layout\.ContentScale\.Crop,
                    modifier = Modifier
                        \.size\(125\.dp\)
                        \.clip\(CircleShape\)
                        \.background\(PhonePePurple\)
                \)
                
                Spacer\(modifier = Modifier\.height\(16\.dp\)\)
                
                // "PhonePe" Text below logo
                Text\(
                    text = "PhonePe",
                    color = PhonePePurple,
                    fontSize = 42\.sp,
                    fontWeight = FontWeight\.ExtraBold,
                    fontFamily = FontFamily\.SansSerif,
                    letterSpacing = \(-1\)\.sp
                \)
            \}
        \}"""

replacement = """        // Centered Main Logo
        Column(
            modifier = Modifier.align(Alignment.Center),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            val context = LocalContext.current
            val resourceId = context.resources.getIdentifier("logo_phonepe", "drawable", context.packageName)
            if (resourceId != 0) {
                Image(
                    painter = androidx.compose.ui.res.painterResource(id = resourceId),
                    contentDescription = "Logo",
                    contentScale = androidx.compose.ui.layout.ContentScale.Fit,
                    modifier = Modifier.size(150.dp).clip(CircleShape)
                )
            } else {
                Image(
                    painter = androidx.compose.ui.res.painterResource(id = com.example.R.drawable.ic_launcher_foreground),
                    contentDescription = "Logo",
                    contentScale = androidx.compose.ui.layout.ContentScale.Crop,
                    modifier = Modifier
                        .size(125.dp)
                        .clip(CircleShape)
                        .background(PhonePePurple)
                )
            }
            
            Spacer(modifier = Modifier.height(8.dp))
            
            Text(
                text = "PhonePe",
                color = PhonePePurple,
                fontSize = 50.sp,
                fontWeight = FontWeight.Bold,
                fontFamily = FontFamily.SansSerif,
                letterSpacing = (-1.5).sp
            )
        }"""

content = re.sub(pattern, replacement, content)

with open("app/src/main/java/com/example/ui/screens/SplashScreen.kt", "w") as f:
    f.write(content)
