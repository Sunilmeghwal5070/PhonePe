with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Add import if missing
if 'import android.net.Uri' not in content:
    content = content.replace('import android.os.Bundle', 'import android.os.Bundle\nimport android.net.Uri')

# update chat navigation
content = content.replace('navController.navigate("chat/$contactName")', 'navController.navigate("chat/${Uri.encode(contactName)}")')
content = content.replace('navController.navigate("chat/${contact.name}")', 'navController.navigate("chat/${Uri.encode(contact.name)}")')

# update pay_amount_prefilled
content = content.replace('navController.navigate("pay_amount_prefilled/$amount/$name")', 'navController.navigate("pay_amount_prefilled/$amount/${Uri.encode(name)}")')

# update pay_pin
content = content.replace('navController.navigate("pay_pin/$amount/${bankAccount.id}/Karishna Karishna")', 'navController.navigate("pay_pin/$amount/${bankAccount.id}/${Uri.encode(\\"Karishna Karishna\\")}")')
content = content.replace('navController.navigate("pay_pin/$amt/${bankAccount.id}/$name")', 'navController.navigate("pay_pin/$amt/${bankAccount.id}/${Uri.encode(name)}")')

# update pay_processing
content = content.replace('navController.navigate("pay_processing/$amount/$bankId/$name")', 'navController.navigate("pay_processing/$amount/$bankId/${Uri.encode(name)}")')

# update pay_success
content = content.replace('navController.navigate("pay_success/$amount/$insertedId/$name")', 'navController.navigate("pay_success/$amount/$insertedId/${Uri.encode(name)}")')

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
