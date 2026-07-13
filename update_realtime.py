import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    text = f.read()

target = """    LaunchedEffect(isActivated) {
        if (isActivated) {
            val key = prefsManager.getActivationKey()
            if (!key.isNullOrEmpty()) {
                try {
                    if (FirebaseApp.getInstance() != null) {
                        val db = FirebaseFirestore.getInstance()
                        val registration = db.collection("activation_keys").document(key).addSnapshotListener { snapshot, error ->
                            if (error != null) return@addSnapshotListener
                            if (snapshot != null && snapshot.exists()) {
                                val status = snapshot.getString("status")
                                if (status == "BLOCKED" || status == "EXPIRED") {
                                    Toast.makeText(context, "Key is $status", Toast.LENGTH_LONG).show()
                                    prefsManager.saveActivation("", 0L)
                                    isActivated = false
                                }
                            }
                        }
                    }
                } catch(e: Exception) {}
            }
        }
    }"""

replacement = """    var showDeactivationDialog by remember { mutableStateOf<String?>(null) }
    
    if (showDeactivationDialog != null) {
        androidx.compose.material3.AlertDialog(
            onDismissRequest = { 
                showDeactivationDialog = null
                prefsManager.saveActivation("", 0L)
                isActivated = false
            },
            title = { androidx.compose.material3.Text("Access Revoked") },
            text = { androidx.compose.material3.Text(showDeactivationDialog!!) },
            confirmButton = {
                androidx.compose.material3.TextButton(onClick = {
                    showDeactivationDialog = null
                    prefsManager.saveActivation("", 0L)
                    isActivated = false
                }) {
                    androidx.compose.material3.Text("OK")
                }
            }
        )
    }

    LaunchedEffect(isActivated) {
        if (isActivated) {
            val key = prefsManager.getActivationKey()
            if (!key.isNullOrEmpty()) {
                try {
                    if (FirebaseApp.getInstance() != null) {
                        val db = FirebaseFirestore.getInstance()
                        val registration = db.collection("activation_keys").document(key).addSnapshotListener { snapshot, error ->
                            if (error != null) return@addSnapshotListener
                            if (snapshot != null && snapshot.exists()) {
                                val status = snapshot.getString("status")
                                if (status == "BLOCKED" || status == "EXPIRED") {
                                    showDeactivationDialog = if (status == "BLOCKED") {
                                        "Your activation key has been blocked by the administrator."
                                    } else {
                                        "Your activation key has expired."
                                    }
                                }
                            }
                        }
                    }
                } catch(e: Exception) {}
            }
        }
    }"""

text = text.replace(target, replacement)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(text)
