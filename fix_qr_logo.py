with open('app/src/main/java/com/example/ui/screens/QrScreen.kt', 'r') as f:
    content = f.read()

old_logo = '''                            Box(
                                modifier = Modifier
                                    .fillMaxSize()
                                    .clip(CircleShape)
                                    .background(Color.Black),
                                contentAlignment = Alignment.Center
                            ) {
                                Text(
                                    text = "पे",
                                    color = Color.White,
                                    fontSize = 24.sp,
                                    fontWeight = FontWeight.Bold,
                                    fontFamily = FontFamily.SansSerif
                                )
                            }'''

new_logo = '''                            androidx.compose.foundation.Image(
                                painter = androidx.compose.ui.res.painterResource(id = com.example.R.drawable.splash_logo),
                                contentDescription = "Logo",
                                contentScale = androidx.compose.ui.layout.ContentScale.Crop,
                                modifier = Modifier
                                    .fillMaxSize()
                                    .clip(CircleShape)
                            )'''

content = content.replace(old_logo, new_logo)

with open('app/src/main/java/com/example/ui/screens/QrScreen.kt', 'w') as f:
    f.write(content)
