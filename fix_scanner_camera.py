import re

with open('app/src/main/java/com/example/ui/screens/ScannerScreen.kt', 'r') as f:
    text = f.read()

target = """                                                if (cleanUrl.lowercase().startsWith("upi://pay")) {
                                                    val uri = Uri.parse(cleanUrl)
                                                    val name = uri.getQueryParameter("pn") ?: uri.getQueryParameter("pa") ?: "Unknown"
                                                    val upi = uri.getQueryParameter("pa") ?: uri.getQueryParameter("pn") ?: "unknown@upi"
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
                                                } else if (cleanUrl.contains("@")) {
                                                    imageAnalysis.clearAnalyzer()
                                                    onScanSuccess(cleanUrl, cleanUrl)
                                                    break
                                                }"""

text = text.replace(target, replacement)

with open('app/src/main/java/com/example/ui/screens/ScannerScreen.kt', 'w') as f:
    f.write(text)
