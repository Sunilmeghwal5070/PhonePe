import re
with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'onNavigateToQr = {\n                        navController.navigate("my_qr")\n                    }',
    'onNavigateToQr = {\n                        navController.navigate("my_qr")\n                    },\n                    onNavigateToCheckBalance = {\n                        navController.navigate("check_balance")\n                    }'
)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
