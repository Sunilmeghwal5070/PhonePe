import re

with open('app/src/main/java/com/example/ui/screens/ScannerScreen.kt', 'r') as f:
    text = f.read()

target = """                                                if (url.lowercase().startsWith("upi://pay")) {
                                                    val uri = Uri.parse(url)
                                                    val name = uri.getQueryParameter("pn") ?: "Unknown"
                                                    val upi = uri.getQueryParameter("pa") ?: "unknown@upi"
                                                    imageAnalysis.clearAnalyzer()
                                                    onScanSuccess(name, upi)
                                                    break
                                                }"""

replacement = """                                                val cleanUrl = url.trim()
                                                if (cleanUrl.lowercase().startsWith("upi://pay")) {
                                                    val uri = Uri.parse(cleanUrl)
                                                    val name = uri.getQueryParameter("pn") ?: "Unknown"
                                                    val upi = uri.getQueryParameter("pa") ?: "unknown@upi"
                                                    imageAnalysis.clearAnalyzer()
                                                    onScanSuccess(name, upi)
                                                    break
                                                }"""

text = text.replace(target, replacement)

with open('app/src/main/java/com/example/ui/screens/ScannerScreen.kt', 'w') as f:
    f.write(text)

