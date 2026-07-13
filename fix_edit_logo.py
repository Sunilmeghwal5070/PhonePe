import re

with open('app/src/main/java/com/example/ui/screens/EditDetailsScreen.kt', 'r') as f:
    text = f.read()

target_state = """    val userProfile by viewModel.userProfileManager.userProfile.collectAsState()"""

replacement_state = """    val userProfile by viewModel.userProfileManager.userProfile.collectAsState()
    val bankAccounts by viewModel.bankAccounts.collectAsState()"""

text = text.replace(target_state, replacement_state)

target_icon = """                if (userProfile.name.isNotBlank()) {
                    Text(
                        text = userProfile.name.first().toString().uppercase(),
                        color = Color.White,
                        fontSize = 48.sp,
                        fontWeight = FontWeight.Bold
                    )
                } else {
                    Icon(
                        Icons.Default.Person,
                        contentDescription = "Profile Picture",
                        tint = Color.White,
                        modifier = Modifier.size(80.dp)
                    )
                }"""

replacement_icon = """                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    coil.compose.AsyncImage(
                        model = getBankLogoUrl(bankAccounts.firstOrNull()?.bankName ?: "SBI"),
                        contentDescription = null,
                        modifier = Modifier.fillMaxSize().padding(12.dp).clip(CircleShape),
                        contentScale = androidx.compose.ui.layout.ContentScale.Fit
                    )
                }"""

text = text.replace(target_icon, replacement_icon)

with open('app/src/main/java/com/example/ui/screens/EditDetailsScreen.kt', 'w') as f:
    f.write(text)
