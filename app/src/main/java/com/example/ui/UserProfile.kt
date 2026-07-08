package com.example.ui

import android.content.Context
import android.content.SharedPreferences
import androidx.core.content.edit
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

data class UserProfile(
    val name: String = "John Doe",
    val phone: String = "9" + (100000000..999999999).random().toString()
)

class UserProfileManager(context: Context) {
    private val prefs: SharedPreferences = context.getSharedPreferences("user_profile_prefs", Context.MODE_PRIVATE)

    private val _userProfile = MutableStateFlow(
        UserProfile(
            name = prefs.getString("name", "John Doe") ?: "John Doe",
            phone = prefs.getString("phone", "9" + (100000000..999999999).random().toString()) ?: "9" + (100000000..999999999).random().toString()
        )
    )
    val userProfile: StateFlow<UserProfile> = _userProfile.asStateFlow()

    fun updateProfile(name: String, phone: String) {
        prefs.edit {
            putString("name", name)
            putString("phone", phone)
        }
        _userProfile.value = UserProfile(name, phone)
    }
}
