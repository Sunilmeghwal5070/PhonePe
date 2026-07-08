with open('/app/applet/app/src/main/AndroidManifest.xml', 'r') as f:
    content = f.read()

content = content.replace('<uses-permission android:name="android.permission.CAMERA" />', '<uses-permission android:name="android.permission.INTERNET" />\n    <uses-permission android:name="android.permission.CAMERA" />')

with open('/app/applet/app/src/main/AndroidManifest.xml', 'w') as f:
    f.write(content)
