import re

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    lines = f.readlines()

# Insert the Box at line 70
box_start = """    var networkStatus by remember { mutableStateOf(0) } // 0 = none, 1 = red, 2 = green
    
    LaunchedEffect(Unit) {
        delay(3000)
        networkStatus = 1
        delay(4000)
        networkStatus = 2
        delay(4000)
        networkStatus = 0
    }

    Box(modifier = Modifier.fillMaxSize()) {
"""

# The LazyColumn starts at line 71. So insert before line 71.
lines.insert(70, box_start)

# The end of HomeScreen is at line 1101 + 1 = 1102 (because we inserted 1 element which is a multiline string... wait, let's just find the closing brace by matching).
# Let's rebuild the file as text.

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'r') as f:
    text = f.read()

# Replace LazyColumn with Box wrapping LazyColumn
lazy_column_str = """    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFFF5F6FA))
    ) {"""

new_lazy = """    var networkStatus by remember { mutableStateOf(0) }
    
    LaunchedEffect(Unit) {
        delay(3000)
        networkStatus = 1
        delay(4000)
        networkStatus = 2
        delay(4000)
        networkStatus = 0
    }

    Box(modifier = Modifier.fillMaxSize()) {
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFFF5F6FA))
    ) {"""

text = text.replace(lazy_column_str, new_lazy)

# Find the end of HomeScreen
end_idx = text.find("}\n\n@Composable\nfun TransferButton")
if end_idx != -1:
    # insert the banner and the closing brace for the Box
    banner_code = """
        
        // Network Status Banner
        AnimatedVisibility(
            visible = networkStatus != 0,
            enter = slideInVertically(initialOffsetY = { -it }),
            exit = slideOutVertically(targetOffsetY = { -it }),
            modifier = Modifier.align(Alignment.TopCenter)
        ) {
            val isRed = networkStatus == 1
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(if (isRed) Color(0xFFD32F2F) else Color(0xFF388E3C))
                    .padding(horizontal = 16.dp, vertical = 12.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(
                    imageVector = if (isRed) Icons.Default.ErrorOutline else Icons.Default.Check,
                    contentDescription = null,
                    tint = Color.White,
                    modifier = Modifier.size(20.dp)
                )
                Spacer(modifier = Modifier.width(12.dp))
                Text(
                    text = if (isRed) "Could not connect to internet" else "We are back...",
                    color = Color.White,
                    fontSize = 14.sp,
                    fontWeight = FontWeight.Medium
                )
            }
        }
    }"""
    
    text = text[:end_idx] + banner_code + text[end_idx:]

with open('app/src/main/java/com/example/ui/screens/HomeScreen.kt', 'w') as f:
    f.write(text)

print("Home screen patched")

