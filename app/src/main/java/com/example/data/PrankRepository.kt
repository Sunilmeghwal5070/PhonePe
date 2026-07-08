package com.example.data

import kotlinx.coroutines.flow.Flow

class PrankRepository(private val dao: PrankTransactionDao) {
    val allTransactions: Flow<List<PrankTransaction>> = dao.getAllTransactions()

    suspend fun getTransactionCount(): Int {
        return dao.getTransactionCount()
    }

    suspend fun getTransactionById(id: Int): PrankTransaction? {
        return dao.getTransactionById(id)
    }

    suspend fun insertTransaction(transaction: PrankTransaction): Long {
        return dao.insertTransaction(transaction)
    }

    suspend fun deleteTransaction(id: Int) {
        dao.deleteTransactionById(id)
    }

    suspend fun deleteAll() {
        dao.deleteAllTransactions()
    }
}
