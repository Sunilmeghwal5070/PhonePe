with open('/app/applet/app/src/main/java/com/example/ui/screens/RechargeScreens.kt', 'r') as f:
    lines = f.readlines()

content = "".join(lines)

import re
# Find the end of RechargePlanScreen
# It's before @Composable fun BenefitRow

split_point = content.find('@Composable\nfun BenefitRow')

if split_point != -1:
    # We remove the appended payment_sheet_code from the end
    payment_sheet_idx = content.find('    if (showPaymentSheet && selectedPlan != null) {')
    if payment_sheet_idx != -1:
        payment_sheet_code = content[payment_sheet_idx:]
        content = content[:payment_sheet_idx]
        
        # Now insert payment_sheet_code before split_point
        # We need to insert it right before the closing brace of RechargePlanScreen
        # Which is just before split_point
        
        insert_idx = content.rfind('}', 0, split_point)
        content = content[:insert_idx] + payment_sheet_code + "\n}\n\n" + content[split_point:]

with open('/app/applet/app/src/main/java/com/example/ui/screens/RechargeScreens.kt', 'w') as f:
    f.write(content)
