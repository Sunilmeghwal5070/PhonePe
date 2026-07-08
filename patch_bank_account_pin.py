import re

with open('/app/applet/app/src/main/java/com/example/ui/PrankViewModel.kt', 'r') as f:
    content = f.read()

content = content.replace(
'''    val balance: String = "Balance: ₹----",
    val upiIds: List<String> = listOf("9876543210-2@axl", "9876543210-2@ybl")
)''',
'''    val balance: String = "Balance: ₹----",
    val upiIds: List<String> = listOf("9876543210-2@axl", "9876543210-2@ybl"),
    val pin: String = "1234"
)''')

content = content.replace(
'''                            accountName = name,
                            bankDesc = bankDesc,
                            type = accType,
                            branch = branch,
                            ifsc = ifsc,
                            balance = balance
                        ))''',
'''                            accountName = name,
                            bankDesc = bankDesc,
                            type = accType,
                            branch = branch,
                            ifsc = ifsc,
                            balance = balance,
                            pin = pin
                        ))''') # Wait, I also need to update AccountDetailsScreen to edit PIN

with open('/app/applet/app/src/main/java/com/example/ui/PrankViewModel.kt', 'w') as f:
    f.write(content)

