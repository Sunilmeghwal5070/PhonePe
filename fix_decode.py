import re
with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    text = f.read()

# Replace all manual decodes for NavArguments
text = re.sub(r'val name = java\.net\.URLDecoder\.decode\(backStackEntry\.arguments\?\.getString\("name"\) \?: "([^"]+)", "UTF-8"\)', r'val name = backStackEntry.arguments?.getString("name") ?: "\1"', text)
text = re.sub(r'val name = java\.net\.URLDecoder\.decode\(backStackEntry\.arguments\?\.getString\("name"\) \?: "", "UTF-8"\)', r'val name = backStackEntry.arguments?.getString("name") ?: ""', text)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(text)
