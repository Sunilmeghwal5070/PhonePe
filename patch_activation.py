import re

with open('app/src/main/java/com/example/ui/screens/ActivationScreen.kt', 'r') as f:
    content = f.read()

# Add userNameInput state
content = content.replace(
    '    var keyInput by remember { mutableStateOf("") }',
    '    var keyInput by remember { mutableStateOf("") }\n    var userNameInput by remember { mutableStateOf("") }'
)

# Add userNameInput TextField
user_name_field = """                        OutlinedTextField(
                value = userNameInput,
                onValueChange = { userNameInput = it; errorMessage = "" },
                label = { Text("Your Name") },
                placeholder = { Text("Enter your full name") },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true,
                enabled = !isLoading
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            OutlinedTextField("""

content = content.replace(
    '            OutlinedTextField(',
    user_name_field,
    1 # Only replace the first occurrence
)

# Add validation
content = content.replace(
    '                    if (keyInput.isBlank()) {',
    '                    if (userNameInput.isBlank()) {\n                        errorMessage = "Please enter your name"\n                        return@Button\n                    }\n                    if (keyInput.isBlank()) {'
)

# Add save userName
content = content.replace(
    '                                                "expiresAt" to expiresAt',
    '                                                "expiresAt" to expiresAt,\n                                                "userName" to userNameInput'
)

content = content.replace(
    'prefsManager.saveActivation(keyInput, expiresAt)',
    'prefsManager.saveActivation(keyInput, expiresAt, userNameInput)'
)

content = content.replace(
    'prefsManager.saveActivation(keyInput, expiryTime)',
    'prefsManager.saveActivation(keyInput, expiryTime, userNameInput)'
)

with open('app/src/main/java/com/example/ui/screens/ActivationScreen.kt', 'w') as f:
    f.write(content)
