import re

with open('/app/applet/app/src/main/java/com/example/ui/screens/AddBankAccountScreen.kt', 'r') as f:
    content = f.read()

content = content.replace("fun AddBankAccountScreen(onBack: () -> Unit)", "fun AddBankAccountScreen(onBack: () -> Unit, onNavigateToAddBankAccountDetails: (String) -> Unit)")

# Find usages of PopularBankItem and pass the callback
content = content.replace("""Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                                PopularBankItem("State Bank of India", Modifier.weight(1f))
                                PopularBankItem("Bank Of Baroda", Modifier.weight(1f))
                                PopularBankItem("Punjab National Bank", Modifier.weight(1f))
                            }""", """Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                                PopularBankItem("State Bank of India", Modifier.weight(1f), onClick = { onNavigateToAddBankAccountDetails("State Bank of India") })
                                PopularBankItem("Bank Of Baroda", Modifier.weight(1f), onClick = { onNavigateToAddBankAccountDetails("Bank Of Baroda") })
                                PopularBankItem("Punjab National Bank", Modifier.weight(1f), onClick = { onNavigateToAddBankAccountDetails("Punjab National Bank") })
                            }""")

content = content.replace("""Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                                PopularBankItem("HDFC Bank", Modifier.weight(1f))
                                PopularBankItem("ICICI Bank", Modifier.weight(1f))
                                PopularBankItem("Union Bank", Modifier.weight(1f))
                            }""", """Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                                PopularBankItem("HDFC Bank", Modifier.weight(1f), onClick = { onNavigateToAddBankAccountDetails("HDFC Bank") })
                                PopularBankItem("ICICI Bank", Modifier.weight(1f), onClick = { onNavigateToAddBankAccountDetails("ICICI Bank") })
                                PopularBankItem("Union Bank", Modifier.weight(1f), onClick = { onNavigateToAddBankAccountDetails("Union Bank") })
                            }""")

content = content.replace("""items(allBanks) { bank ->
                    BankListItem(bank)
                }""", """items(allBanks) { bank ->
                    BankListItem(bank, onClick = { onNavigateToAddBankAccountDetails(bank) })
                }""")

# Change PopularBankItem signature
content = content.replace("""@Composable
fun PopularBankItem(name: String, modifier: Modifier = Modifier) {
    Column(
        modifier = modifier.clickable { },
        horizontalAlignment = Alignment.CenterHorizontally
    ) {""", """@Composable
fun PopularBankItem(name: String, modifier: Modifier = Modifier, onClick: () -> Unit = {}) {
    Column(
        modifier = modifier.clickable { onClick() },
        horizontalAlignment = Alignment.CenterHorizontally
    ) {""")

# Change BankListItem signature
content = content.replace("""@Composable
fun BankListItem(name: String) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { }
            .padding(horizontal = 16.dp, vertical = 12.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {""", """@Composable
fun BankListItem(name: String, onClick: () -> Unit = {}) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() }
            .padding(horizontal = 16.dp, vertical = 12.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {""")

with open('/app/applet/app/src/main/java/com/example/ui/screens/AddBankAccountScreen.kt', 'w') as f:
    f.write(content)
