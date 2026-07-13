import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    text = f.read()

if "import com.google.firebase.firestore.FirebaseFirestore" not in text:
    text = text.replace("import android.os.Bundle", "import android.os.Bundle\nimport com.google.firebase.firestore.FirebaseFirestore\nimport android.widget.Toast\nimport com.google.firebase.FirebaseApp")

# Let's insert a LaunchedEffect inside MainActivity setup (maybe near Scaffold)
target = """    val bankAccounts by prankViewModel.bankAccounts.collectAsState()
    val allTransactions by prankViewModel.allTransactions.collectAsState()"""

replacement = """    val bankAccounts by prankViewModel.bankAccounts.collectAsState()
    val allTransactions by prankViewModel.allTransactions.collectAsState()
    val context = androidx.compose.ui.platform.LocalContext.current

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
text = text.replace(target, replacement)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(text)
