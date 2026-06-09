<template>
  <div v-if="video" class="video-detail-container">
    
    <div class="video-player-wrapper">
      <iframe width="100%" height="500" :src="'https://www.youtube.com/embed/' + video.youtube_id + '?autoplay=1'" frameborder="0" allowfullscreen></iframe>
    </div>

    <div class="video-info-section">
      <h2>{{ video.title }}</h2>
      <div class="creator-info">
        <div class="avatar">🎵</div>
        <div>
          <p style="margin: 0;">Created by <strong>Fuzik User</strong></p>
          <p style="margin: 0; color: #aaa; font-size: 14px;">{{ video.views }} views • {{ video.time }}</p>
        </div>
        <div class="action-buttons">
          <button>— Fans</button>
          <button>— Like</button>
          <button>🔗 Share</button>
        </div>
      </div>

      <hr style="border-color: #333; margin: 20px 0;">

      <div class="description">
        <h4>Description</h4>
        <p style="color: #ccc; white-space: pre-wrap;" v-if="video.description">{{ video.description }}</p>
        <p style="color: #555; font-style: italic;" v-else>ไม่มีคำอธิบายสำหรับวิดีโอนี้</p>
      </div>

      <hr style="border-color: #333; margin: 20px 0;">

      <div class="layout-selection">
        <h4>Select your layout for jamming this play.</h4>
        
        <div class="layout-options">
          
          <div class="layout-card" @click="selectLayout('grid-4')">
            <div class="layout-grid grid-4">
              <div class="box">1</div><div class="box">2</div>
              <div class="box">3</div><div class="box">4</div>
            </div>
          </div>

          <div class="layout-card" @click="selectLayout('grid-3')">
            <div class="layout-grid grid-3">
              <div class="top-row"><div class="box">1</div><div class="box">2</div></div>
              <div class="bottom-row"><div class="box">3</div></div>
            </div>
          </div>

          <div class="layout-card" @click="selectLayout('grid-2')">
            <div class="layout-grid grid-2">
              <div class="box">1</div><div class="box">2</div>
            </div>
          </div>

          <div class="layout-card" @click="selectLayout('grid-3-alt')">
            <div class="layout-grid grid-3-alt">
              <div class="left-col"><div class="box">1</div></div>
              <div class="right-col"><div class="box">2</div><div class="box">3</div></div>
            </div>
          </div>

        </div>
      </div>
    </div>

  </div>
  <div v-else style="color: white; padding: 20px;">
    กำลังโหลดข้อมูลวิดีโอ...
  </div>
</template>

<script setup>
import { computed } from 'vue'
const route = useRoute()
const router = useRouter()

// ดึงข้อมูลวิดีโอจาก API
const config = useRuntimeConfig();
const { data: apiVideos } = await useFetch(`${config.public.apiBase}/api/videos/`)
const video = computed(() => {
  if (!apiVideos.value) return null
  const v = apiVideos.value.find(v => v.id.toString() === route.params.id)
  if (v) {
    return { ...v, views: Math.floor(Math.random() * 100), time: new Date(v.uploaded_at).toLocaleDateString('th-TH') }
  }
  return null
})

// ฟังก์ชันเมื่อกดเลือก Layout -> พาไปหน้า Jam Studio
const selectLayout = (layoutType) => {
  // ส่งรหัสวิดีโอ และ Layout ที่เลือกไปที่หน้า Jam
  router.push(`/jam/${video.value.id}?layout=${layoutType}`)
}
</script>

<style scoped>
.video-detail-container { color: #fff; max-width: 1000px; margin: 0 auto; padding-bottom: 50px; }
.video-player-wrapper { background: #000; border-radius: 10px; overflow: hidden; margin-bottom: 20px; border: 1px solid #fdd835; }
.creator-info { display: flex; align-items: center; gap: 15px; margin-bottom: 20px; }
.avatar { width: 40px; height: 40px; background: #333; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; }
.action-buttons { margin-left: auto; display: flex; gap: 10px; }
.action-buttons button { background: #222; color: #fff; border: 1px solid #444; padding: 5px 15px; border-radius: 20px; cursor: pointer; }
.action-buttons button:hover { background: #333; }

/* CSS สำหรับวาดรูป Layout Grid */
.layout-options { display: flex; flex-wrap: wrap; gap: 20px; margin-top: 15px; }
.layout-card { background: #fff; padding: 10px; border-radius: 8px; cursor: pointer; transition: transform 0.2s; border: 3px solid transparent; }
.layout-card:hover { transform: scale(1.05); border-color: #fdd835; }

.layout-grid { width: 160px; height: 100px; display: flex; flex-direction: column; gap: 2px; background: #000; border: 2px solid #000; }
.box { background: #fff; flex: 1; display: flex; align-items: center; justify-content: center; font-size: 24px; color: #000; font-weight: bold; }

/* 📌 เพิ่ม CSS ของ 2 ช่อง และ 3 ช่องพิเศษ เข้ามา */
.grid-4 { display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; }

.grid-3 .top-row { display: flex; flex: 1; gap: 2px; }
.grid-3 .bottom-row { display: flex; flex: 1; justify-content: center; padding: 0 25%; }

.grid-2 { display: flex; flex-direction: row; gap: 2px; }

.grid-3-alt { display: flex; flex-direction: row; gap: 2px; }
.grid-3-alt .left-col { flex: 1; display: flex; }
.grid-3-alt .right-col { flex: 1; display: flex; flex-direction: column; gap: 2px; }
</style>