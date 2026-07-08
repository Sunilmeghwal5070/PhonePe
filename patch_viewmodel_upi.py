import re

with open("app/src/main/java/com/example/ui/PrankViewModel.kt", "r") as f:
    content = f.read()

if "var selectedPayeeUpi" not in content:
    content = content.replace("class PrankViewModel", "class PrankViewModel")
    content = content.replace("    val userProfileManager = UserProfileManager(application)", "    val userProfileManager = UserProfileManager(application)\n    var selectedPayeeUpi = \"yashwant@ybl\"")

with open("app/src/main/java/com/example/ui/PrankViewModel.kt", "w") as f:
    f.write(content)
