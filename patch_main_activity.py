import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Add LaunchedEffect to check key status
check_code = """    if (!isActivated) {
        ActivationScreen(
            prefsManager = prefsManager,
            onActivated = { isActivated = true }
        )
        return
    }

    LaunchedEffect(Unit) {
        try {
            val key = prefsManager.getActivationKey()
            if (key != null && com.google.firebase.FirebaseApp.getApps(context).isNotEmpty()) {
                val db = com.google.firebase.firestore.FirebaseFirestore.getInstance()
                db.collection("activation_keys").document(key).get().addOnSuccessListener { doc ->
                    if (doc.exists()) {
                        val status = doc.getString("status")
                        if (status == "BLOCKED" || status == "EXPIRED") {
                            prefsManager.saveActivation("", 0L)
                            isActivated = false
                        }
                    } else {
                        // Key deleted from DB
                        prefsManager.saveActivation("", 0L)
                        isActivated = false
                    }
                }
            }
        } catch (e: Exception) {}
    }
"""

content = content.replace(
    '    if (!isActivated) {\n        ActivationScreen(\n            prefsManager = prefsManager,\n            onActivated = { isActivated = true }\n        )\n        return\n    }',
    check_code
)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
