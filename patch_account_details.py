import re

with open("app/src/main/java/com/example/ui/screens/AccountDetailsScreen.kt", "r") as f:
    content = f.read()

save_button = """
            if (isEditableState && account != null) {
                Spacer(modifier = Modifier.height(16.dp))
                Button(
                    onClick = {
                        val updated = account.copy(
                            accountName = accName,
                            bankDesc = bankDesc,
                            type = accType,
                            branch = branch,
                            ifsc = ifsc,
                            balance = balance.toDoubleOrNull() ?: account.balance
                        )
                        viewModel.updateBankAccount(updated)
                        onBack()
                    },
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp)
                        .height(52.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF5f259f)),
                    shape = RoundedCornerShape(26.dp)
                ) {
                    Text("SAVE CHANGES", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.White)
                }
            }
"""

content = content.replace("            // International UPI", save_button + "\n            // International UPI")

with open("app/src/main/java/com/example/ui/screens/AccountDetailsScreen.kt", "w") as f:
    f.write(content)
