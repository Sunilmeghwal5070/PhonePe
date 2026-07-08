with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'onNavigateToContactList = {\n                        navController.navigate("contact_list")\n                    }\n                )',
    'onNavigateToContactList = {\n                        navController.navigate("contact_list")\n                    },\n                    onNavigateToMobileRecharge = {\n                        navController.navigate("mobile_recharge")\n                    }\n                )'
)

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
