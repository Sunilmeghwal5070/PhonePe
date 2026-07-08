import re

with open("app/src/main/java/com/example/ui/screens/PayAmountScreen.kt", "r") as f:
    content = f.read()

content = content.replace("prefilledName: String = \"YASHWANT MEGHWAL\",", "payeeName: String = \"YASHWANT MEGHWAL\",\n    upiId: String = \"yashwant@ybl\",")
content = content.replace("prefilledName", "payeeName")

with open("app/src/main/java/com/example/ui/screens/PayAmountScreen.kt", "w") as f:
    f.write(content)
