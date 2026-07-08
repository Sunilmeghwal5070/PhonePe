with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

old_home = '''                HomeScreen(
                    viewModel = prankViewModel,
                    onCreatePrank = {
                        navController.navigate("create")
                    },
                    onNavigateToReceipt = { transactionId ->
                        navController.navigate("receipt/$transactionId")
                    },
                    onNavigateToQr = {
                        navController.navigate("my_qr")
                    },
                    onNavigateToCheckBalance = {
                        navController.navigate("check_balance")
                    },
                    onNavigateToProfile = {
                        navController.navigate("profile")
                    }
                )'''

new_home = '''                HomeScreen(
                    viewModel = prankViewModel,
                    onCreatePrank = {
                        navController.navigate("create")
                    },
                    onNavigateToReceipt = { transactionId ->
                        navController.navigate("receipt/$transactionId")
                    },
                    onNavigateToQr = {
                        navController.navigate("my_qr")
                    },
                    onNavigateToCheckBalance = {
                        navController.navigate("check_balance")
                    },
                    onNavigateToProfile = {
                        navController.navigate("profile")
                    },
                    onNavigateToContactList = {
                        navController.navigate("contact_list")
                    }
                )'''

content = content.replace(old_home, new_home)

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
