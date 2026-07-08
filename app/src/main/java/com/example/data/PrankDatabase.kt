package com.example.data

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase

@Database(entities = [PrankTransaction::class], version = 3, exportSchema = false)
abstract class PrankDatabase : RoomDatabase() {
    abstract fun prankTransactionDao(): PrankTransactionDao

    companion object {
        @Volatile
        private var INSTANCE: PrankDatabase? = null

        fun getDatabase(context: Context): PrankDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    PrankDatabase::class.java,
                    "prank_database"
                )
                .fallbackToDestructiveMigration()
                .build()
                INSTANCE = instance
                instance
            }
        }
    }
}
