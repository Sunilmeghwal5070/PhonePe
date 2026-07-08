import re

with open("app/src/main/java/com/example/ui/screens/RechargeReminderDialog.kt", "r") as f:
    content = f.read()

import_statement = """import androidx.compose.material.icons.Icons\nimport androidx.compose.material.icons.filled.Close\nimport androidx.compose.foundation.layout.Column\n"""
content = content.replace("import androidx.compose.foundation.background", import_statement + "import androidx.compose.foundation.background")

dialog_start = r"""    Dialog\(onDismissRequest = onDismiss\) \{
        Card\("""

dialog_replacement = """    Dialog(onDismissRequest = onDismiss) {
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Card("""

dialog_end = r"""                \}
            \}
        \}
    \}
\}"""

dialog_end_replacement = """                }
            }
        }
        
        Spacer(modifier = Modifier.height(24.dp))
        
        // Close Button
        Box(
            modifier = Modifier
                .size(48.dp)
                .background(Color.White.copy(alpha = 0.2f), CircleShape)
                .clickable { onDismiss() },
            contentAlignment = Alignment.Center
        ) {
            Icon(Icons.Default.Close, contentDescription = "Close", tint = Color.White, modifier = Modifier.size(24.dp))
        }
        }
    }
}"""

content = re.sub(dialog_start, dialog_replacement, content)
content = re.sub(dialog_end, dialog_end_replacement, content)

with open("app/src/main/java/com/example/ui/screens/RechargeReminderDialog.kt", "w") as f:
    f.write(content)
