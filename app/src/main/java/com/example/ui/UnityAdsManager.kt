package com.example.ui

import android.app.Activity
import android.content.Context
import android.util.Log
import com.unity3d.ads.IUnityAdsInitializationListener
import com.unity3d.ads.IUnityAdsLoadListener
import com.unity3d.ads.IUnityAdsShowListener
import com.unity3d.ads.UnityAds
import com.unity3d.ads.UnityAdsShowOptions

object UnityAdsManager {
    private const val GAME_ID = "800084470"
    private const val AD_UNIT_ID = "Rewarded_Android"
    private const val TEST_MODE = false
    
    fun initialize(context: Context) {
        UnityAds.initialize(context, GAME_ID, TEST_MODE, object : IUnityAdsInitializationListener {
            override fun onInitializationComplete() {
                Log.d("UnityAds", "Initialization Complete")
                loadRewardedAd()
            }

            override fun onInitializationFailed(error: UnityAds.UnityAdsInitializationError, message: String) {
                Log.e("UnityAds", "Initialization Failed: $error - $message")
            }
        })
    }

    private fun loadRewardedAd() {
        UnityAds.load(AD_UNIT_ID, object : IUnityAdsLoadListener {
            override fun onUnityAdsAdLoaded(placementId: String) {
                Log.d("UnityAds", "Ad Loaded: $placementId")
            }

            override fun onUnityAdsFailedToLoad(placementId: String, error: UnityAds.UnityAdsLoadError, message: String) {
                Log.e("UnityAds", "Ad Failed to Load: $placementId - $error - $message")
            }
        })
    }

    fun showRewardedAd(activity: Activity, onRewardEarned: () -> Unit) {
        UnityAds.show(activity, AD_UNIT_ID, UnityAdsShowOptions(), object : IUnityAdsShowListener {
            override fun onUnityAdsShowFailure(placementId: String, error: UnityAds.UnityAdsShowError, message: String) {
                Log.e("UnityAds", "Ad Show Failed: $placementId - $error - $message")
                // Fallback in case of error (optional)
            }

            override fun onUnityAdsShowStart(placementId: String) {
                Log.d("UnityAds", "Ad Show Started: $placementId")
            }

            override fun onUnityAdsShowClick(placementId: String) {
                Log.d("UnityAds", "Ad Show Clicked: $placementId")
            }

            override fun onUnityAdsShowComplete(placementId: String, state: UnityAds.UnityAdsShowCompletionState) {
                Log.d("UnityAds", "Ad Show Complete: $placementId, state: $state")
                if (state == UnityAds.UnityAdsShowCompletionState.COMPLETED) {
                    onRewardEarned()
                }
                loadRewardedAd() // Load next ad
            }
        })
    }
}
