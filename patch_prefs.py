import re

with open('app/src/main/java/com/example/ui/PrefsManager.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'fun saveActivation(key: String, expiryTime: Long) {\n        prefs.edit {\n            putString("activation_key", key)\n            putLong("activation_expiry", expiryTime)\n        }\n    }',
    'fun saveActivation(key: String, expiryTime: Long, userName: String = "") {\n        prefs.edit {\n            putString("activation_key", key)\n            putLong("activation_expiry", expiryTime)\n            if (userName.isNotEmpty()) putString("activation_user_name", userName)\n        }\n    }'
)

content = content.replace(
    'fun getActivationKey(): String? = prefs.getString("activation_key", null)',
    'fun getActivationKey(): String? = prefs.getString("activation_key", null)\n    fun getActivationUserName(): String? = prefs.getString("activation_user_name", null)'
)

with open('app/src/main/java/com/example/ui/PrefsManager.kt', 'w') as f:
    f.write(content)
