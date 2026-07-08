with open('/app/applet/app/src/main/java/com/example/ui/screens/RechargeScreens.kt', 'r') as f:
    content = f.read()

content = content.replace('replace("\D".toRegex(), "")', 'replace("\\\\D".toRegex(), "")')

with open('/app/applet/app/src/main/java/com/example/ui/screens/RechargeScreens.kt', 'w') as f:
    f.write(content)
