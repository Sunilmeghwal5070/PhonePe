package com.example.ui.screens

fun getBankLogoUrl(bankName: String): String {
    return when {
        bankName.contains("State Bank", ignoreCase = true) || bankName.contains("SBI", ignoreCase = true) -> "https://companieslogo.com/downloads/logos/State-Bank-of-India-SBI-Logo.png"
        bankName.contains("Baroda", ignoreCase = true) -> "https://companieslogo.com/downloads/logos/Bank-of-Baroda-Logo.png"
        bankName.contains("Punjab National", ignoreCase = true) || bankName.contains("PNB", ignoreCase = true) -> "https://companieslogo.com/downloads/logos/Punjab-National-Bank-Logo.png"
        bankName.contains("HDFC", ignoreCase = true) -> "https://companieslogo.com/downloads/logos/HDFC-Bank-Logo.png"
        bankName.contains("ICICI", ignoreCase = true) -> "https://companieslogo.com/downloads/logos/ICICI-Bank-Logo.png"
        bankName.contains("Union Bank", ignoreCase = true) -> "https://companieslogo.com/downloads/logos/Union-Bank-of-India-Logo.png"
        bankName.contains("Axis", ignoreCase = true) -> "https://companieslogo.com/downloads/logos/Axis-Bank-Logo.png"
        bankName.contains("Kotak", ignoreCase = true) -> "https://companieslogo.com/downloads/logos/Kotak-Mahindra-Bank-Logo.png"
        bankName.contains("Yes Bank", ignoreCase = true) -> "https://companieslogo.com/downloads/logos/Yes-Bank-Logo.png"
        bankName.contains("IndusInd", ignoreCase = true) -> "https://companieslogo.com/downloads/logos/IndusInd-Bank-Logo.png"
        bankName.contains("Canara", ignoreCase = true) -> "https://companieslogo.com/downloads/logos/Canara-Bank-Logo.png"
        bankName.contains("Bank of India", ignoreCase = true) -> "https://companieslogo.com/downloads/logos/Bank-of-India-Logo.png"
        bankName.contains("Maharashtra", ignoreCase = true) -> "https://companieslogo.com/downloads/logos/Bank-of-Maharashtra-Logo.png"
        else -> "https://cdn-icons-png.flaticon.com/512/2830/2830284.png" // Generic bank icon
    }
}
