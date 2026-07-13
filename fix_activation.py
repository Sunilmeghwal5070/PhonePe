import re

with open('app/src/main/java/com/example/ui/screens/ActivationScreen.kt', 'r') as f:
    text = f.read()

target_failure = """                                .addOnFailureListener {
                                    errorMessage = "Error: ${it.message}"
                                    isLoading = false
                                }"""

replacement_failure = """                                .addOnFailureListener {
                                    // Fallback to local validation if Firebase fails (offline or not configured)
                                    if (keyInput.matches(Regex("Ph-\\\\d{4}-[A-Z]{2}"))) {
                                        val expiryTime = if (keyInput.endsWith("FR")) {
                                            System.currentTimeMillis() + 24 * 60 * 60 * 1000L
                                        } else {
                                            System.currentTimeMillis() + 28L * 24 * 60 * 60 * 1000L
                                        }
                                        prefsManager.saveActivation(keyInput, expiryTime, userNameInput)
                                        isLoading = false
                                        onActivated()
                                    } else {
                                        errorMessage = "Error: ${it.message}"
                                        isLoading = false
                                    }
                                }"""

text = text.replace(target_failure, replacement_failure)

with open('app/src/main/java/com/example/ui/screens/ActivationScreen.kt', 'w') as f:
    f.write(text)
