with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

import re

# replace ${Uri.encode("Karishna Karishna")} with Karishna%20Karishna
content = content.replace('${Uri.encode("Karishna Karishna")}', 'Karishna%20Karishna')
content = content.replace('${Uri.encode(\\"Karishna Karishna\\")}', 'Karishna%20Karishna')

# replace ${Uri.encode(name)} with ${java.net.URLEncoder.encode(name, "UTF-8")}
content = content.replace('${Uri.encode(name)}', '${java.net.URLEncoder.encode(name, "UTF-8")}')
content = content.replace('${Uri.encode(contactName)}', '${java.net.URLEncoder.encode(contactName, "UTF-8")}')
content = content.replace('${Uri.encode(contact.name)}', '${java.net.URLEncoder.encode(contact.name, "UTF-8")}')

# Add import if needed
if 'import java.net.URLEncoder' not in content:
    content = content.replace('import android.net.Uri', 'import android.net.Uri\nimport java.net.URLEncoder')

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
