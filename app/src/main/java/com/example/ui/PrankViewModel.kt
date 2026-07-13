package com.example.ui

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.example.data.PrankDatabase
import com.example.data.PrankRepository
import com.example.data.PrankTransaction
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

data class BankAccount(
    val id: String = java.util.UUID.randomUUID().toString(),
    val bankName: String,
    val accountName: String = "John",
    val bankDesc: String,
    val type: String,
    val branch: String,
    val ifsc: String,
    val balance: Double = 1297.0,
    val upiIds: List<String> = listOf("9876543210-2@axl", "9876543210-2@ybl"),
    val pin: String = "1234"
)

class PrankViewModel(application: Application) : AndroidViewModel(application) {
    var hasShownRechargeReminder = false
    private val prefsManager = PrefsManager(application)
    val userProfileManager = UserProfileManager(application)
    var selectedPayeeUpi = "yashwant@ybl"

    private val _bankAccounts = MutableStateFlow<List<BankAccount>>(prefsManager.getBankAccounts())
    val bankAccounts: StateFlow<List<BankAccount>> = _bankAccounts.asStateFlow()

    private val _isShakeEnabled = MutableStateFlow(prefsManager.isShakeEnabled())
    val isShakeEnabled: StateFlow<Boolean> = _isShakeEnabled.asStateFlow()
    fun setShakeEnabled(enabled: Boolean) {
        _isShakeEnabled.value = enabled
        prefsManager.setShakeEnabled(enabled)
    }

    fun addBankAccount(account: BankAccount) {
        if (_bankAccounts.value.size < 2) {
            val newList = _bankAccounts.value + account
            _bankAccounts.value = newList
            prefsManager.saveBankAccounts(newList)
        }
    }

    fun updateBankAccount(account: BankAccount) {
        val newList = _bankAccounts.value.map { if (it.id == account.id) account else it }
        _bankAccounts.value = newList
        prefsManager.saveBankAccounts(newList)
    }

    fun deleteBankAccount(accountId: String) {
        val newList = _bankAccounts.value.filter { it.id != accountId }
        _bankAccounts.value = newList
        prefsManager.saveBankAccounts(newList)
    }

    private val repository: PrankRepository
    val allTransactions: StateFlow<List<PrankTransaction>>

    init {
        val db = PrankDatabase.getDatabase(application)
        repository = PrankRepository(db.prankTransactionDao())
        allTransactions = repository.allTransactions.stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000),
            initialValue = emptyList()
        )
        
        viewModelScope.launch {
            if (repository.getTransactionCount() == 0) {
                // Add 5-7 dummy records to look real
                val dummyNames = listOf("Rahul Sharma", "Amit Singh", "Priya Patel", "Vikram Rathore", "Neha Gupta", "Suresh Kumar", "Rohan Das")
                val dummyAmounts = listOf(150.0, 500.0, 1200.0, 20.0, 350.0, 2000.0, 75.0)
                
                for (i in 0 until 6) {
                    val timeOffset = (1..10).random() * 24 * 60 * 60 * 1000L // 1 to 10 days ago
                    insertTransaction(
                        name = dummyNames[i],
                        phone = "987654321${i}",
                        upiId = "${dummyNames[i].replace(" ", "").lowercase()}@ybl",
                        amount = dummyAmounts[i],
                        status = "SUCCESS",
                        bankName = "State Bank of India",
                        bankLast4 = (1000..9999).random().toString(),
                        customTxId = generateTransactionId(),
                        customUtr = generateUtr(),
                        timestamp = System.currentTimeMillis() - timeOffset,
                        onSuccess = {}
                    )
                }
            }
        }
    }

    private val _selectedTransaction = MutableStateFlow<PrankTransaction?>(null)
    val selectedTransaction: StateFlow<PrankTransaction?> = _selectedTransaction.asStateFlow()

    fun generateTransactionId(): String {
        val prefix = "T"
        val dateDigits = System.currentTimeMillis().toString().takeLast(10)
        val randomDigits = (100000..999999).random().toString()
        return "$prefix$dateDigits$randomDigits"
    }

    fun generateUtr(): String {
        val firstDigit = (6..9).random().toString()
        val remaining = (10000000000..99999999999).random().toString()
        return "$firstDigit$remaining"
    }

    fun selectTransactionById(id: Int) {
        viewModelScope.launch {
            val tx = repository.getTransactionById(id)
            _selectedTransaction.value = tx
        }
    }

    fun insertTransaction(
        name: String,
        phone: String,
        upiId: String,
        amount: Double,
        status: String,
        type: String = "PAID",
        bankName: String,
        bankLast4: String,
        customTxId: String,
        customUtr: String,
        timestamp: Long,
        onSuccess: (Int) -> Unit
    ) {
        viewModelScope.launch {
            val resolvedTxId = customTxId.ifBlank { generateTransactionId() }
            
            // Deduct balance
            val actualAmount = if (amount <= 0.0) 100.0 else amount
            val newList = _bankAccounts.value.map { acc ->
                if (acc.bankName == bankName || acc.bankDesc.contains(bankLast4)) {
                    acc.copy(balance = acc.balance - actualAmount)
                } else acc
            }
            _bankAccounts.value = newList
            prefsManager.saveBankAccounts(newList)

            val resolvedUtr = customUtr.ifBlank { generateUtr() }
            val resolvedUpi = upiId.ifBlank { 
                val cleanName = name.replace("\\s+".toRegex(), "").lowercase()
                "$cleanName@ybl" 
            }
            
            val transaction = PrankTransaction(
                receiverName = name.ifBlank { "Manoj Kumar" },
                receiverPhone = phone.ifBlank { "9876543210" },
                receiverUpiId = resolvedUpi,
                amount = if (amount <= 0.0) 100.0 else amount,
                timestamp = if (timestamp <= 0L) System.currentTimeMillis() else timestamp,
                status = status,
                type = type,
                senderBankName = bankName.ifBlank { "State Bank of India" },
                senderBankAccountLast4 = bankLast4.ifBlank { (1000..9999).random().toString() },
                transactionId = resolvedTxId,
                utr = resolvedUtr
            )
            
            val newId = repository.insertTransaction(transaction)
            onSuccess(newId.toInt())
        }
    }

    fun deleteTransaction(id: Int) {
        viewModelScope.launch {
            repository.deleteTransaction(id)
        }
    }

    fun clearAll() {
        viewModelScope.launch {
            repository.deleteAll()
        }
    }
}

class PrankViewModelFactory(private val application: Application) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(PrankViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return PrankViewModel(application) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}
