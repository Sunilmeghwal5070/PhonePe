with open('app/src/main/java/com/example/ui/screens/SearchScreen.kt', 'r') as f:
    content = f.read()

old_logo = '''                                Box(
                                    modifier = Modifier
                                        .size(40.dp)
                                        .clip(CircleShape)
                                        .background(Color.White),
                                    contentAlignment = Alignment.Center
                                ) {
                                    Text("पे", color = PhonePePurple, fontWeight = FontWeight.Bold, fontSize = 22.sp)
                                }'''

new_logo = '''                                androidx.compose.foundation.Image(
                                    painter = androidx.compose.ui.res.painterResource(id = com.example.R.drawable.splash_logo),
                                    contentDescription = "Logo",
                                    contentScale = androidx.compose.ui.layout.ContentScale.Crop,
                                    modifier = Modifier
                                        .size(40.dp)
                                        .clip(CircleShape)
                                )'''

content = content.replace(old_logo, new_logo)

with open('app/src/main/java/com/example/ui/screens/SearchScreen.kt', 'w') as f:
    f.write(content)
