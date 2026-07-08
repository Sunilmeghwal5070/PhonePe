package com.example.data

import androidx.room.Entity
import androidx.room.PrimaryKey
import java.io.Serializable

@Entity(tableName = "prank_transactions")
data class PrankTransaction(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val receiverName: String,
    val receiverPhone: String,
    val receiverUpiId: String,
    val amount: Double,
    val timestamp: Long,
    val status: String, // "SUCCESS", "PENDING", "FAILED"
    val type: String = "PAID", // "PAID", "RECEIVED"
    val senderBankName: String,
    val senderBankAccountLast4: String,
    val transactionId: String,
    val utr: String
) : Serializable
