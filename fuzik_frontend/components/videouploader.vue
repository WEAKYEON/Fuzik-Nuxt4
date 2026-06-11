<template>
  <div class="uploader-card">
    <h2>อัปโหลดวิดีโอ Jam ของคุณ</h2>
    
    <form @submit.prevent="submitUpload">
      <div>
        <label>ชื่อวิดีโอ:</label>
        <input type="text" v-model="formData.title" required />
      </div>
      <div>
        <label>ชื่อเพลง:</label>
        <input type="text" v-model="formData.music_title" required />
      </div>
      <div>
        <label>ชื่อนักดนตรี:</label>
        <input type="text" v-model="formData.musician_name" required />
      </div>

      <div>
        <label>ไฟล์วิดีโอ (MP4):</label>
        <input type="file" accept="video/mp4,video/x-m4v,video/*" @change="handleFileChange" required />
      </div>

      <button type="submit" :disabled="isUploading">
        {{ isUploading ? 'กำลังอัปโหลด...' : 'ส่งวิดีโอ' }}
      </button>
    </form>

    <p v-if="message" class="status-message">{{ message }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const formData = ref({
  title: '',
  music_title: '',
  musician_name: ''
})
const selectedFile = ref(null)
const isUploading = ref(false)
const message = ref('')

// ฟังก์ชันจับไฟล์เมื่อผู้ใช้กดเลือกไฟล์
const handleFileChange = (event) => {
  selectedFile.value = event.target.files[0]
}

// ฟังก์ชันส่งข้อมูล (AJAX) ไปหา Django
const submitUpload = async () => {
  if (!selectedFile.value) return

  isUploading.value = true
  message.value = 'กำลังส่งไฟล์เข้าเซิร์ฟเวอร์ กรุณารอสักครู่...'

  // แพ็กของใส่กล่อง (FormData) เตรียมส่ง
  const uploadData = new FormData()
  uploadData.append('video_file', selectedFile.value)
  uploadData.append('title', formData.value.title)
  uploadData.append('music_title', formData.value.music_title)
  uploadData.append('musician_name', formData.value.musician_name)

  try {
    // ยิง AJAX ไปหา API ของ Django ที่เราสร้างไว้
    const response = await $fetch('http://127.0.0.1:8000/api/videos/upload/', {
      method: 'POST',
      body: uploadData
    })
    
    message.value = "อัปโหลดสำเร็จ! รอแอดมินตรวจสอบก่อนนำขึ้น YouTube"
    console.log("Upload Success:", response)
    
  } catch (error) {
    console.error("Upload Error:", error)
    message.value = "เกิดข้อผิดพลาดในการอัปโหลด"
  } finally {
    isUploading.value = false
  }
}
</script>

<style scoped>
/* แต่ง UI คร่าวๆ (คุณเอาไปปรับให้เข้ากับเว็บ Fuzik ได้เลย) */
.uploader-card { border: 1px solid #ccc; padding: 20px; max-width: 500px; border-radius: 8px; }
div { margin-bottom: 15px; }
input { width: 100%; padding: 8px; margin-top: 5px; }
button { padding: 10px 20px; background-color: #ff0000; color: white; border: none; cursor: pointer; }
button:disabled { background-color: #999; }
.status-message { margin-top: 15px; font-weight: bold; }
</style>