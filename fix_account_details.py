import re

with open("app/src/main/java/com/example/ui/screens/AccountDetailsScreen.kt", "r") as f:
    content = f.read()

# Fix Unlink bank account
pattern_unlink = r"""Row\(\s*modifier = Modifier\s*\.fillMaxWidth\(\)\s*\.clickable \{ \}\s*\.padding\(16\.dp\),\s*verticalAlignment = Alignment\.CenterVertically\s*\)\s*\{\s*Icon\(Icons\.Default\.DeleteOutline, contentDescription = null, tint = Color\(0xFFD32F2F\)\)\s*Spacer\(modifier = Modifier\.width\(16\.dp\)\)\s*Text\("Unlink Bank Account", fontSize = 16\.sp, color = Color\(0xFFD32F2F\)\)\s*\}"""
replacement_unlink = """Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable { viewModel.deleteBankAccount(accountId); onBack() }
                        .padding(16.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(Icons.Default.DeleteOutline, contentDescription = null, tint = Color(0xFFD32F2F))
                    Spacer(modifier = Modifier.width(16.dp))
                    Text("Unlink Bank Account", fontSize = 16.sp, color = Color(0xFFD32F2F))
                }"""
content = re.sub(pattern_unlink, replacement_unlink, content)

# Fix Powered by UPI
pattern_powered = r"""Row\(verticalAlignment = Alignment\.CenterVertically\)\s*\{\s*Text\("UPI", fontSize = 24\.sp, color = Color\.Gray, fontWeight = FontWeight\.Bold\)\s*Canvas\(modifier = Modifier\.size\(24\.dp\)\)\s*\{\s*val path = Path\(\)\.apply \{\s*moveTo\(size\.width \* 0\.2f, size\.height \* 0\.2f\)\s*lineTo\(size\.width \* 0\.8f, size\.height \* 0\.5f\)\s*lineTo\(size\.width \* 0\.2f, size\.height \* 0\.8f\)\s*close\(\)\s*\}\s*drawPath\(path, color = Color\(0xFF388E3C\)\)\s*val path2 = Path\(\)\.apply \{\s*moveTo\(size\.width \* 0\.1f, size\.height \* 0\.1f\)\s*lineTo\(size\.width \* 0\.9f, size\.height \* 0\.5f\)\s*lineTo\(size\.width \* 0\.1f, size\.height \* 0\.9f\)\s*\}\s*drawPath\(path2, color = Color\(0xFFF57C00\), style = Stroke\(width = 3\.dp\.toPx\(\)\)\)\s*\}\s*\}\s*Text\("UNIFIED PAYMENTS INTERFACE", fontSize = 8\.sp, color = Color\.Gray\)"""
replacement_powered = """Row(verticalAlignment = Alignment.CenterVertically) {
                        coil.compose.AsyncImage(
                            model = coil.request.ImageRequest.Builder(androidx.compose.ui.platform.LocalContext.current)
                                .data("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/UPI-Logo-vector.svg/1024px-UPI-Logo-vector.svg.png")
                                .crossfade(true)
                                .build(),
                            contentDescription = "UPI",
                            modifier = Modifier.height(24.dp),
                            contentScale = androidx.compose.ui.layout.ContentScale.Fit
                        )
                    }"""
content = re.sub(pattern_powered, replacement_powered, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/AccountDetailsScreen.kt", "w") as f:
    f.write(content)
