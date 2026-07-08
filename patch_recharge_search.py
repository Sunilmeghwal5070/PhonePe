with open('/app/applet/app/src/main/java/com/example/ui/screens/RechargeScreens.kt', 'r') as f:
    content = f.read()

replacement = """
    val isPhoneNumber = searchQuery.replace(" ", "").all { it.isDigit() } && searchQuery.replace(" ", "").length >= 4
    val filteredContacts = if (searchQuery.isBlank()) {
        contacts
    } else {
        val matches = contacts.filter { it.name.contains(searchQuery, ignoreCase = true) || it.number.contains(searchQuery) }.toMutableList()
        if (isPhoneNumber && matches.none { it.number.replace("\\\\D".toRegex(), "") == searchQuery.replace(" ", "") }) {
            matches.add(0, Contact(name = "Recharge to " + searchQuery, number = searchQuery))
        }
        matches
    }
"""

import re
content = re.sub(
    r'val filteredContacts = if \(searchQuery\.isBlank\(\)\) \{\s*contacts\s*\} else \{\s*contacts\.filter \{ it\.name\.contains\(searchQuery, ignoreCase = true\) \|\| it\.number\.contains\(searchQuery\) \}\s*\}',
    replacement.strip(),
    content
)

with open('/app/applet/app/src/main/java/com/example/ui/screens/RechargeScreens.kt', 'w') as f:
    f.write(content)
