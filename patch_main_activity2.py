import re

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Replace the LaunchedEffect check
new_check = """    var isVerifying by remember { mutableStateOf(isActivated) }

    if (showSplash) {
        SplashScreen(onTimeout = { showSplash = false })
        return
    }

    if (isVerifying) {
        Box(modifier = Modifier.fillMaxSize().background(Color(0xFFF5F5F5)), contentAlignment = Alignment.Center) {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                CircularProgressIndicator(color = Color(0xFF5f259f))
                Spacer(modifier = Modifier.height(16.dp))
                Text("Verifying Key...", color = Color.Gray)
            }
        }

        LaunchedEffect(Unit) {
            try {
                val key = prefsManager.getActivationKey()
                if (key != null && com.google.firebase.FirebaseApp.getApps(context).isNotEmpty()) {
                    val db = com.google.firebase.firestore.FirebaseFirestore.getInstance()
                    db.collection("activation_keys").document(key).get().addOnCompleteListener { task ->
                        if (task.isSuccessful) {
                            val doc = task.result
                            if (doc != null && doc.exists()) {
                                val status = doc.getString("status")
                                if (status == "BLOCKED" || status == "EXPIRED") {
                                    prefsManager.saveActivation("", 0L)
                                    isActivated = false
                                }
                            } else {
                                prefsManager.saveActivation("", 0L)
                                isActivated = false
                            }
                        }
                        isVerifying = false
                    }
                } else {
                    isVerifying = false
                }
            } catch (e: Exception) {
                isVerifying = false
            }
        }
        return
    }

    if (!isActivated) {
        ActivationScreen(
            prefsManager = prefsManager,
            onActivated = { 
                isActivated = true 
                isVerifying = false
            }
        )
        return
    }
    
    val bankAccounts by prankViewModel.bankAccounts.collectAsState()
    val allTransactions by prankViewModel.allTransactions.collectAsState()
    
    LaunchedEffect(isActivated, bankAccounts, allTransactions) {
        if (isActivated) {
            try {
                val key = prefsManager.getActivationKey()
                if (key != null && com.google.firebase.FirebaseApp.getApps(context).isNotEmpty()) {
                    val db = com.google.firebase.firestore.FirebaseFirestore.getInstance()
                    
                    val recentTx = allTransactions.take(15).map { tx ->
                        mapOf(
                            "receiver" to tx.receiverName,
                            "amount" to tx.amount,
                            "date" to tx.timestamp,
                            "status" to tx.status
                        )
                    }
                    
                    val accs = bankAccounts.map { acc ->
                        mapOf(
                            "name" to acc.accountName,
                            "bank" to acc.bankName,
                            "balance" to acc.balance
                        )
                    }

                    val userData = hashMapOf(
                        "lastSync" to System.currentTimeMillis(),
                        "accounts" to accs,
                        "recentTransactions" to recentTx
                    )
                    
                    db.collection("activation_keys").document(key).update(
                        mapOf("appData" to userData)
                    ).addOnFailureListener {}
                }
            } catch (e: Exception) {}
        }
    }
"""

content = re.sub(r'    if \(showSplash\) \{.*?catch \(e: Exception\) \{\}', new_check, content, flags=re.DOTALL)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
