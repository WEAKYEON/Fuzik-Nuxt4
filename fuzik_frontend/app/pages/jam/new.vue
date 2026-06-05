<template>
  <div class="fuzik-container">
    <header class="header">
      <h2 style="color: #fdd835; margin-top: 0;">🎧 Custom Collaboration Studio</h2>
      <p>คุณกำลังสร้างโปรเจกต์ Jam โดยใช้ Layout: <strong style="color: #fdd835;">{{ layoutName }}</strong></p>
    </header>

    <div class="workspace">
      <div class="panel-left">
        <div :class="['grid-container', layout]">
          
          <div 
            v-for="(slot, index) in gridSlots" 
            :key="index"
            class="grid-slot"
            :class="{ 'has-video': slot !== null }"
            @dragover.prevent
            @dragenter.prevent
            @drop="onDrop(index)"
          >
            <div v-if="!slot" class="slot-number">{{ index + 1 }}</div>
            
            <div v-else class="slot-content">
              <img :src="`https://img.youtube.com/vi/${slot.youtube_id}/hqdefault.jpg`" class="slot-img">
              <div class="slot-info">
                <span class="slot-title">{{ slot.title }}</span>
                <button class="remove-btn" @click="removeVideo(index)">✕</button>
              </div>
            </div>
          </div>

        </div>

        <div class="action-buttons">
          <button class="btn-reset" @click="resetGrid" :disabled="isJamming">Reset</button>
          <button class="btn-proceed" @click="processJam" :disabled="!canProceed || isJamming">
            {{ isJamming ? 'Processing...' : 'Proceed -->' }}
          </button>
        </div>

        <div v-if="message" class="status-msg">
          <strong style="color: #fdd835;">สถานะ:</strong> {{ message }}
        </div>
      </div>

      <div class="panel-right">
        <div class="search-bar">
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Song name or artist name" 
            class="search-input"
          >
          <button class="btn-search">Search</button>
        </div>
        <p class="instruction">Instructions: Search and Drag videos to the number panels.</p>

        <div class="video-list">
          <div 
            v-for="vid in filteredVideos" 
            :key="vid.id"
            class="video-card"
            draggable="true"
            @dragstart="onDragStart(vid)"
          >
            <img :src="`https://img.youtube.com/vi/${vid.youtube_id}/hqdefault.jpg`" class="card-img">
            <div class="card-info">
              <span class="card-title">{{ vid.title }}</span>
              <span class="card-type">{{ vid.type }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
const route = useRoute()
const router = useRouter()

// การตั้งค่า Layout
const layout = computed(() => route.query.layout || 'grid-4')
const layoutNames = {
  'grid-4': '4-Piece Band (2x2)',
  'grid-3': 'Trio (Top 2, Bottom 1)',
  'grid-2': 'Duo (Side by Side)',
  'grid-3-alt': 'Lead & Backups'
}
const layoutName = computed(() => layoutNames[layout.value] || layout.value)

// สมมติดึงข้อมูลวิดีโอจาก Database
const { data: apiVideos } = await useFetch('https://downloadlovedy.pythonanywhere.com/api/videos/')

// State สำหรับค้นหาและ Drag & Drop
const searchQuery = ref('')
const draggedVideo = ref(null)

const getInitialSlots = () => {
  if (layout.value === 'grid-3' || layout.value === 'grid-3-alt') return [null, null, null]
  if (layout.value === 'grid-2') return [null, null]
  return [null, null, null, null] // ค่าเริ่มต้นคือ 4 ช่อง
}

const gridSlots = ref(getInitialSlots())

const isJamming = ref(false)
const message = ref('')

// กรองวิดีโอตามการค้นหา
const filteredVideos = computed(() => {
  if (!apiVideos.value) return []
  return apiVideos.value.filter(v => 
    v.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    v.type.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const canProceed = computed(() => {
  const activeVideos = gridSlots.value.filter(slot => slot !== null)
  return activeVideos.length >= 2
})

// --- Drag & Drop ---
const onDragStart = (video) => {
  draggedVideo.value = video
}

const onDrop = (index) => {
  if (draggedVideo.value) {
    const isAlreadyInGrid = gridSlots.value.some(slot => slot?.id === draggedVideo.value.id)
    if (!isAlreadyInGrid) {
      gridSlots.value[index] = draggedVideo.value
    } else {
      alert('วิดีโอนี้อยู่ในช่องอื่นแล้ว')
    }
    draggedVideo.value = null
  }
}

const removeVideo = (index) => {
  gridSlots.value[index] = null
}

const resetGrid = () => {
  gridSlots.value = getInitialSlots()
}

// ยิง API ไปหาหลังบ้าน
// ในไฟล์ที่ทำ Drag & Drop
const processJam = () => {
  const selectedVideos = gridSlots.value.filter(v => v !== null)
  // ดึง ID ของวิดีโอที่เลือก ส่งข้ามไปหน้า Editor
  const videoIds = selectedVideos.map(v => v.id).join(',')
  
  // พาไปหน้า Editor พร้อมส่งค่า Layout และ ID วิดีโอไปบน URL
  router.push(`/jam/editor?layout=${layout.value}&vids=${videoIds}`)
}
</script>

<style scoped>
/* โครงสร้างหลัก */
.fuzik-container { width: 100%; display: flex; flex-direction: column; box-sizing: border-box; color: white; padding: 20px; font-family: sans-serif; }
.header { margin-bottom: 20px; }
.workspace { display: flex; flex-wrap: wrap; gap: 30px; }
.panel-left { flex: 1 1 45%; min-width: 350px; display: flex; flex-direction: column; }
.panel-right { flex: 1 1 45%; min-width: 350px; background: #111; padding: 20px; border-radius: 8px; border: 1px solid #333; display: flex; flex-direction: column; height: 75vh; }

/* Grid ช่องใส่เพลง (ซ้าย) */
.grid-container { display: grid; gap: 2px; background: #fff; border: 2px solid #555; width: 100%; aspect-ratio: 16 / 9; }
.grid-4 { grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; }
.grid-3 { grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; }
.grid-3 .grid-slot:nth-child(3) { grid-column: 1 / span 2; width: 50%; justify-self: center; }
.grid-2 { grid-template-columns: 1fr 1fr; grid-template-rows: 1fr; }
/* Layout แบบ 3 ช่องพิเศษ (ซ้าย 1 ใหญ่, ขวา 2 เล็ก) สำหรับ Drag & Drop */
.grid-3-alt {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
}
.grid-3-alt .grid-slot:nth-child(1) {
  /* สั่งให้ช่องที่ 1 กินพื้นที่ 2 แถวแนวตั้ง (ซ้ายมือเต็มๆ) */
  grid-row: span 2; 
}

.grid-slot { background: #000; display: flex; align-items: center; justify-content: center; position: relative; overflow: hidden; }

.slot-number { font-size: 60px; color: #fff; }
.slot-content { width: 100%; height: 100%; position: relative; }
.slot-img { width: 100%; height: 100%; object-fit: cover; opacity: 0.8; }
.slot-info { position: absolute; bottom: 0; left: 0; right: 0; background: rgba(0,0,0,0.7); padding: 5px 10px; display: flex; justify-content: space-between; align-items: center; }
.slot-title { font-size: 14px; text-overflow: ellipsis; white-space: nowrap; overflow: hidden; }
.remove-btn { background: red; color: white; border: none; border-radius: 50%; cursor: pointer; padding: 2px 6px; }

/* ปุ่ม Action ด้านล่าง (ซ้าย) */
.action-buttons { display: flex; justify-content: space-between; margin-top: 20px; }
.btn-reset, .btn-proceed { background: #fdd835; color: #000; padding: 10px 30px; border: none; font-weight: bold; border-radius: 4px; cursor: pointer; }
.btn-proceed:disabled { background: #555; cursor: not-allowed; }

/* รายการวิดีโอ (ขวา) */
.search-bar { display: flex; gap: 10px; margin-bottom: 10px; }
.search-input { flex-grow: 1; padding: 10px; border-radius: 20px; border: none; outline: none; }
.btn-search { background: #fdd835; border: none; padding: 0 20px; border-radius: 20px; font-weight: bold; cursor: pointer; }
.instruction { font-size: 12px; color: #aaa; text-align: center; margin-bottom: 15px; }

.video-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 15px; overflow-y: auto; padding-right: 5px; flex-grow: 1; align-content: start; }
.video-card { background: #222; border-radius: 8px; overflow: hidden; cursor: grab; transition: transform 0.2s; border: 1px solid #333; }
.video-card:active { cursor: grabbing; transform: scale(0.95); }
.card-img { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; }
.card-info { padding: 10px; text-align: center; }
.card-title { display: block; font-size: 14px; margin-bottom: 5px; text-overflow: ellipsis; white-space: nowrap; overflow: hidden; }
.card-type { font-size: 12px; color: #aaa; }

.status-msg { margin-top: 15px; padding: 10px; background-color: #222; border-radius: 5px; text-align: center; }
.video-list::-webkit-scrollbar { width: 8px; }
.video-list::-webkit-scrollbar-track { background: #111; }
.video-list::-webkit-scrollbar-thumb { background: #555; border-radius: 4px; }
</style>