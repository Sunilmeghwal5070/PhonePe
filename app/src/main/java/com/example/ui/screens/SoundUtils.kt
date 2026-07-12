package com.example.ui.screens

import android.media.AudioFormat
import android.media.AudioManager
import android.media.AudioTrack

fun playSuccessBeep() {
    Thread {
        try {
            val sampleRate = 44100
            val duration1 = 0.15
            val duration2 = 0.4
            val gap = 0.05
            val numSamples = (sampleRate * (duration1 + gap + duration2)).toInt()
            val sample = ShortArray(numSamples)
            
            fun fill(startIdx: Int, duration: Double, freq: Double) {
                val samples = (sampleRate * duration).toInt()
                for (i in 0 until samples) {
                    val t = i.toDouble() / sampleRate
                    var env = 1.0
                    if (i < 400) env = i / 400.0
                    if (i > samples - 400) env = (samples - i) / 400.0
                    val v = Math.sin(2.0 * Math.PI * freq * t) * env
                    if (startIdx + i < sample.size) {
                        sample[startIdx + i] = (v * 32767).toInt().toShort()
                    }
                }
            }
            
            fill(0, duration1, 987.0)
            fill((sampleRate * (duration1 + gap)).toInt(), duration2, 1318.0)
            
            val audioTrack = AudioTrack(
                AudioManager.STREAM_MUSIC,
                sampleRate,
                AudioFormat.CHANNEL_OUT_MONO,
                AudioFormat.ENCODING_PCM_16BIT,
                sample.size * 2,
                AudioTrack.MODE_STATIC
            )
            audioTrack.write(sample, 0, sample.size)
            audioTrack.play()
            Thread.sleep(((duration1 + gap + duration2) * 1000).toLong() + 100)
            audioTrack.release()
        } catch (e: Exception) {}
    }.start()
}
