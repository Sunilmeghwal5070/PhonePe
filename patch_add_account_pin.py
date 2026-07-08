import re

with open('/app/applet/app/src/main/java/com/example/ui/screens/AddBankAccountDetailsScreen.kt', 'r') as f:
    content = f.read()

content = content.replace(
'''                                bankDesc = bankDesc,
                                type = accType,
                                branch = branch,
                                ifsc = ifsc,
                                balance = balance
                            )''',
'''                                bankDesc = bankDesc,
                                type = accType,
                                branch = branch,
                                ifsc = ifsc,
                                balance = balance,
                                pin = "1234"
                            )'''
)

with open('/app/applet/app/src/main/java/com/example/ui/screens/AddBankAccountDetailsScreen.kt', 'w') as f:
    f.write(content)
