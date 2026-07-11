import re

with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'fun ProfileScreen(\n    viewModel: PrankViewModel,\n    onBack: () -> Unit,\n    onNavigateToEditDetails: () -> Unit = {},\n    onNavigateToAccountDetails: () -> Unit = {}\n) {',
    'fun ProfileScreen(\n    viewModel: PrankViewModel,\n    prefsManager: com.example.ui.PrefsManager,\n    onBack: () -> Unit,\n    onNavigateToEditDetails: () -> Unit = {},\n    onNavigateToAccountDetails: () -> Unit = {}\n) {'
)

profile_item_code = """
            ProfileMethodItem(icon = Icons.Default.Info, title = "About PhonePe", onClick = {})
            
            // App License/Key Details
            val activationKey = prefsManager.getActivationKey() ?: "Unknown"
            val expiryTime = prefsManager.getActivationExpiry()
            val formatter = java.text.SimpleDateFormat("dd MMM yyyy, hh:mm a", java.util.Locale.getDefault())
            val expiryDateStr = if (expiryTime > 0) formatter.format(java.util.Date(expiryTime)) else "N/A"
            
            ProfileMethodItem(
                icon = Icons.Default.VpnKey, 
                title = "App License Details", 
                subtitle = "Key: $activationKey\\nExpires: $expiryDateStr", 
                onClick = {}
            )
"""

content = content.replace(
    '            ProfileMethodItem(icon = Icons.Default.Info, title = "About PhonePe", onClick = {})',
    profile_item_code
)

with open('app/src/main/java/com/example/ui/screens/ProfileScreen.kt', 'w') as f:
    f.write(content)
