import re

with open("app/src/main/java/com/example/ui/PrankViewModel.kt", "r") as f:
    content = f.read()

pattern = r"""class PrankViewModel\(application: Application\) : AndroidViewModel\(application\) \{"""
replacement = """class PrankViewModel(application: Application) : AndroidViewModel(application) {
    var hasShownRechargeReminder = false"""
content = re.sub(pattern, replacement, content)

with open("app/src/main/java/com/example/ui/PrankViewModel.kt", "w") as f:
    f.write(content)
