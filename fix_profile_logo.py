import re

with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'r') as f:
    text = f.read()

target_state = """    val userProfile by viewModel.userProfileManager.userProfile.collectAsState()"""

replacement_state = """    val userProfile by viewModel.userProfileManager.userProfile.collectAsState()
    val bankAccounts by viewModel.bankAccounts.collectAsState()"""

text = text.replace(target_state, replacement_state)

target_icon = """                    Text(
                        text = if (userProfile.name.isNotBlank()) userProfile.name.first().toString().uppercase() else "Y",
                        color = Color.White,
                        fontWeight = FontWeight.Bold,
                        fontSize = 20.sp
                    )"""

replacement_icon = """                    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                        coil.compose.AsyncImage(
                            model = getBankLogoUrl(bankAccounts.firstOrNull()?.bankName ?: "SBI"),
                            contentDescription = null,
                            modifier = Modifier.fillMaxSize().padding(4.dp).clip(RoundedCornerShape(12.dp)),
                            contentScale = androidx.compose.ui.layout.ContentScale.Crop
                        )
                    }"""

text = text.replace(target_icon, replacement_icon)

with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'w') as f:
    f.write(text)
