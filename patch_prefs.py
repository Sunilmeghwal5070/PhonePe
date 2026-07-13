import re

with open('app/src/main/java/com/example/ui/PrefsManager.kt', 'r') as f:
    text = f.read()

text = text.replace("    fun isActivated(): Boolean {", "    fun isShakeEnabled(): Boolean = prefs.getBoolean(\"shake_to_scan\", false)\n    fun setShakeEnabled(enabled: Boolean) = prefs.edit { putBoolean(\"shake_to_scan\", enabled) }\n\n    fun isActivated(): Boolean {")

with open('app/src/main/java/com/example/ui/PrefsManager.kt', 'w') as f:
    f.write(text)
