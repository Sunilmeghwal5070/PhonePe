import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Make sure we import URLDecoder
if 'import java.net.URLDecoder' not in content:
    content = content.replace('import java.net.URLEncoder', 'import java.net.URLEncoder\nimport java.net.URLDecoder')

content = content.replace(
    'val name = backStackEntry.arguments?.getString("name") ?: "Karishna Karishna"',
    'val name = java.net.URLDecoder.decode(backStackEntry.arguments?.getString("name") ?: "Karishna Karishna", "UTF-8")'
)

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
