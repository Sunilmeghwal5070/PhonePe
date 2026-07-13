import re

with open('app/src/main/java/com/example/ui/screens/ScannerScreen.kt', 'r') as f:
    text = f.read()

target = """                                                if (cleanUrl.lowercase().startsWith("upi://pay")) {
                                                    val uri = Uri.parse(cleanUrl)
                                                    val name = uri.getQueryParameter("pn") ?: "Unknown"
                                                    val upi = uri.getQueryParameter("pa") ?: "unknown@upi"
                                                    imageAnalysis.clearAnalyzer()
                                                    onScanSuccess(name, upi)
                                                    break
                                                }"""

replacement = """                                                if (cleanUrl.lowercase().startsWith("upi://pay")) {
                                                    val uri = Uri.parse(cleanUrl)
                                                    val name = uri.getQueryParameter("pn") ?: uri.getQueryParameter("pa") ?: "Unknown"
                                                    val upi = uri.getQueryParameter("pa") ?: uri.getQueryParameter("pn") ?: "unknown@upi"
                                                    imageAnalysis.clearAnalyzer()
                                                    onScanSuccess(name, upi)
                                                    break
                                                }"""

text = text.replace(target, replacement)

target2 = """                                                if (cleanUrl.lowercase().startsWith("upi://pay")) {
                                                    val uri = Uri.parse(cleanUrl)
                                                    val name = uri.getQueryParameter("pn") ?: "Unknown"
                                                    val upi = uri.getQueryParameter("pa") ?: "unknown@upi"
                                                    onScanSuccess(name, upi)
                                                    found = true
                                                    break
                                                }"""

replacement2 = """                                                if (cleanUrl.lowercase().startsWith("upi://pay")) {
                                                    val uri = Uri.parse(cleanUrl)
                                                    val name = uri.getQueryParameter("pn") ?: uri.getQueryParameter("pa") ?: "Unknown"
                                                    val upi = uri.getQueryParameter("pa") ?: uri.getQueryParameter("pn") ?: "unknown@upi"
                                                    onScanSuccess(name, upi)
                                                    found = true
                                                    break
                                                } else {
                                                    // if it's not a UPI URI but some text, try treating it as UPI ID
                                                    if (cleanUrl.contains("@")) {
                                                        onScanSuccess(cleanUrl, cleanUrl)
                                                        found = true
                                                        break
                                                    }
                                                }"""

text = text.replace(target2, replacement2)

with open('app/src/main/java/com/example/ui/screens/ScannerScreen.kt', 'w') as f:
    f.write(text)
