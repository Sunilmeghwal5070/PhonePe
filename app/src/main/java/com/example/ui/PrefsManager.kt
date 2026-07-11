package com.example.ui

import android.content.Context
import android.content.SharedPreferences
import androidx.core.content.edit
import com.squareup.moshi.Moshi
import com.squareup.moshi.Types
import com.squareup.moshi.kotlin.reflect.KotlinJsonAdapterFactory
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

class PrefsManager(context: Context) {
    private val prefs: SharedPreferences = context.getSharedPreferences("prank_prefs", Context.MODE_PRIVATE)
    private val moshi = Moshi.Builder().add(KotlinJsonAdapterFactory()).build()
    private val listType = Types.newParameterizedType(List::class.java, BankAccount::class.java)
    private val adapter = moshi.adapter<List<BankAccount>>(listType)

    fun getBankAccounts(): List<BankAccount> {
        val json = prefs.getString("bank_accounts", null)
        return if (json != null) {
            try {
                adapter.fromJson(json) ?: defaultAccounts()
            } catch (e: Exception) {
                defaultAccounts()
            }
        } else {
            defaultAccounts()
        }
    }

    fun saveBankAccounts(accounts: List<BankAccount>) {
        prefs.edit {
            putString("bank_accounts", adapter.toJson(accounts))
        }
    }

    fun saveActivation(key: String, expiryTime: Long) {
        prefs.edit {
            putString("activation_key", key)
            putLong("activation_expiry", expiryTime)
        }
    }

    fun getActivationKey(): String? = prefs.getString("activation_key", null)
    
    fun getActivationExpiry(): Long = prefs.getLong("activation_expiry", 0L)

    fun isActivated(): Boolean {
        val expiry = getActivationExpiry()
        return expiry > System.currentTimeMillis()
    }

    private fun defaultAccounts(): List<BankAccount> {
        return listOf(
            BankAccount(
                id = "1",
                bankName = "State Bank of India",
                accountName = "John",
                bankDesc = "State Bank Of India - 0365",
                type = ":  Saving Account",
                branch = ":  MUMBAI MAIN",
                ifsc = ":  UBIN0000000"
            )
        )
    }
}
