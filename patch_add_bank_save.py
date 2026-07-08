import re

with open("app/src/main/java/com/example/ui/screens/AddBankAccountDetailsScreen.kt", "r") as f:
    content = f.read()

# Add a Save button at the end
save_button = """
            Spacer(modifier = Modifier.height(16.dp))
            Button(
                onClick = {
                    val newAccount = BankAccount(
                        bankName = bankName,
                        accountName = accName,
                        bankDesc = bankDesc,
                        type = accType,
                        branch = branch,
                        ifsc = ifsc,
                        balance = balance.toDoubleOrNull() ?: 0.0
                    )
                    viewModel.addBankAccount(newAccount)
                    onBack()
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp)
                    .height(52.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF5f259f)),
                shape = RoundedCornerShape(26.dp)
            ) {
                Text("SAVE ACCOUNT", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.White)
            }
            Spacer(modifier = Modifier.height(24.dp))
        }
    }
}
"""

content = content.replace("            Spacer(modifier = Modifier.height(24.dp))\n        }\n    }\n}", save_button)

with open("app/src/main/java/com/example/ui/screens/AddBankAccountDetailsScreen.kt", "w") as f:
    f.write(content)
