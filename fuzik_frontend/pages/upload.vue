<template>
  <div style="padding: 20px;">
    <h2 style="color: white;">อัปโหลดวิดีโอขึ้นระบบ</h2>
    <form @submit.prevent="uploadVideo" style="border: 1px solid #333; padding: 20px; border-radius: 8px; max-width: 600px; background-color: #111;">
      
      <div style="margin-bottom: 15px;">
        <label style="display: block; font-weight: bold; margin-bottom: 5px; color: #ccc;">ชื่อวิดีโอ:</label>
        <input type="text" v-model="title" required placeholder="เช่น Cover กีตาร์เพลง..." style="width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #555; background: #222; color: #fff; box-sizing: border-box;">
      </div>

      <div style="margin-bottom: 15px;">
        <label style="display: block; font-weight: bold; margin-bottom: 5px; color: #ccc;">รายละเอียด (Description):</label>
        <textarea v-model="description" placeholder="อธิบายวิดีโอของคุณเพิ่มเติม..." style="width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #555; background: #222; color: #fff; box-sizing: border-box; min-height: 100px;"></textarea>
      </div>

      <div style="margin-bottom: 15px;">
        <label style="display: block; font-weight: bold; margin-bottom: 5px; color: #ccc;">เลือกไฟล์วิดีโอ (.mp4):</label>
        <input type="file" @change="handleFileChange" accept="video/*" required style="color: white;">
      </div>
    
      <button type="submit" :disabled="isUploading" style="background-color: #fdd835; color: #000; padding: 12px 15px; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; width: 100%; font-size: 16px; transition: transform 0.2s;">
        {{ isUploading ? 'กำลังส่งเข้าระบบ Fuzik (หุ่นยนต์กำลังทำงาน)...' : 'อัปโหลดวิดีโอ' }}
      </button>
    </form>

    <div v-if="message" style="margin-top: 20px; padding: 15px; background-color: #222; border-radius: 5px; border: 1px solid #333; max-width: 600px;">
      <strong style="color: yellow;">สถานะ:</strong> {{ message }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const title = ref('')
const description = ref('') // เพิ่มตัวแปรสำหรับรับค่า Description
const file = ref(null)
const isUploading = ref(false)
const message = ref('')

const handleFileChange = (event) => { file.value = event.target.files[0] }

const uploadVideo = async () => {
  if (!file.value) {
    message.value = 'กรุณาเลือกไฟล์วิดีโอก่อนกดอัปโหลดครับ!'
    return
  }

  isUploading.value = true
  message.value = 'กำลังส่งไฟล์ไปที่เซิร์ฟเวอร์หลังบ้าน...'

  const formData = new FormData()
  formData.append('title', title.value)
  formData.append('description', description.value) // ส่ง Description ไปด้วย
  formData.append('video_file', file.value)
  
  formData.append('video_type', 'solo')

  try {
    await $fetch('https://downloadlovedy.pythonanywhere.com/api/upload/', {
      method: 'POST',
      body: formData
    })
    message.value = 'อัปโหลดสำเร็จ! วิดีโอของคุณถูกส่งขึ้น YouTube อัตโนมัติแล้ว กลับไปดูที่ Dashboard ได้เลย'
    
    // เคลียร์ฟอร์มหลังอัปโหลดเสร็จ
    title.value = ''
    description.value = ''
    file.value = null 
  } catch (error) {
    message.value = 'เกิดข้อผิดพลาดในการอัปโหลด'
  } finally {
    isUploading.value = false
  }
}
</script>