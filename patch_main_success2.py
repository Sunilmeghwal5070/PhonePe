with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '"pay_success/{amount}/{transactionId}"' in line:
        lines[i] = line.replace('"pay_success/{amount}/{transactionId}"', '"pay_success/{amount}/{transactionId}/{name}"')
    if 'navArgument("transactionId") { type = NavType.IntType }' in line:
        lines[i] = '                    navArgument("transactionId") { type = NavType.IntType },\n                    navArgument("name") { type = NavType.StringType }\n'
    if 'val txId = backStackEntry.arguments?.getInt("transactionId") ?: 0' in line:
        lines[i] = line + '                val name = backStackEntry.arguments?.getString("name") ?: "Karishna Karishna"\n'
    if 'amount = amount,' in line and i > 390 and i < 415:
        lines[i] = line + '                    payeeName = name,\n'

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.writelines(lines)
