package com.example.data

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import kotlinx.coroutines.flow.Flow

@Dao
interface PrankTransactionDao {
    @Query("SELECT * FROM prank_transactions ORDER BY timestamp DESC")
    fun getAllTransactions(): Flow<List<PrankTransaction>>
    
    @Query("SELECT COUNT(*) FROM prank_transactions")
    suspend fun getTransactionCount(): Int

    @Query("SELECT * FROM prank_transactions WHERE id = :id LIMIT 1")
    suspend fun getTransactionById(id: Int): PrankTransaction?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertTransaction(transaction: PrankTransaction): Long

    @Query("DELETE FROM prank_transactions WHERE id = :id")
    suspend fun deleteTransactionById(id: Int)

    @Query("DELETE FROM prank_transactions")
    suspend fun deleteAllTransactions()
}
