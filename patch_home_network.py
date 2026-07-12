import re

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    text = f.read()

# Replace the LaunchedEffect networkStatus simulation with a real ConnectivityManager callback
target = """    var networkStatus by remember { mutableStateOf(0) }
    
    LaunchedEffect(Unit) {
        delay(3000)
        networkStatus = 1
        delay(4000)
        networkStatus = 2
        delay(4000)
        networkStatus = 0
    }"""

replacement = """    val context = LocalContext.current
    var networkStatus by remember { mutableStateOf(0) } // 0 = none/initial, 1 = offline, 2 = online (we are back)
    
    DisposableEffect(context) {
        val connectivityManager = context.getSystemService(android.content.Context.CONNECTIVITY_SERVICE) as android.net.ConnectivityManager
        
        val networkCallback = object : android.net.ConnectivityManager.NetworkCallback() {
            override fun onAvailable(network: android.net.Network) {
                // If it was previously offline, show "We are back"
                if (networkStatus == 1) {
                    networkStatus = 2
                }
            }

            override fun onLost(network: android.net.Network) {
                networkStatus = 1
            }
        }
        
        val request = android.net.NetworkRequest.Builder()
            .addCapability(android.net.NetworkCapabilities.NET_CAPABILITY_INTERNET)
            .build()
            
        connectivityManager.registerNetworkCallback(request, networkCallback)
        
        onDispose {
            connectivityManager.unregisterNetworkCallback(networkCallback)
        }
    }
    
    // Auto-hide "We are back" after 3 seconds
    LaunchedEffect(networkStatus) {
        if (networkStatus == 2) {
            delay(3000)
            networkStatus = 0
        }
    }"""

text = text.replace(target, replacement)

# We need to make sure we don't have multiple `val context = LocalContext.current`
text = text.replace("    val context = LocalContext.current\n    val context = LocalContext.current", "    val context = LocalContext.current")

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(text)

