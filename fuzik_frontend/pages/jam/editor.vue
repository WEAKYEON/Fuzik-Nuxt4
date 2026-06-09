<template>
  <div class="editor-container">
    
    <div class="left-panel">
      <div class="ruler-toggle">
        <input type="checkbox" id="ruler" checked>
        <label for="ruler">Ruler</label>
      </div>

      <div :class="['layout-preview', layoutType]">
        <div class="layout-box" v-for="(vid, index) in selectedVideos" :key="'box-'+vid.id">
          {{ index + 1 }}
        </div>
      </div>

      <div class="track-colors">
        <div v-for="(vid, index) in selectedVideos" :key="'line-'+vid.id" :class="['line', `${trackColors[index]}-line`]"></div>
      </div>

      <button class="btn-generate" @click="generatePreview">
        {{ isPreviewing ? '⏹ Stop Preview' : '▶ Generate 20s preview' }}
      </button>

      <div class="preview-section">
        <p class="preview-text">Preview</p>
        
        <div class="preview-screen" v-if="!isPreviewing">
          Not available
        </div>
        
        <div class="preview-screen active" v-else>
          <div :class="['mini-grid-container', layoutType]">
            <div v-for="(vid, index) in selectedVideos" :key="'prev-'+vid.id" class="mini-slot">
              <iframe 
                width="100%" 
                height="100%" 
                :src="`https://www.youtube.com/embed/${vid.youtube_id}?autoplay=1&mute=1&start=${trackDelays[index]}`" 
                frameborder="0" 
                allow="autoplay; encrypted-media" 
                allowfullscreen>
              </iframe>
            </div>
          </div>

        </div>
      </div>

      <button class="btn-queue" @click="sendToQueue">Send to Queue</button>
    </div>

    <div class="right-panel">
      
      <div class="track-row" v-for="(vid, index) in selectedVideos" :key="'track-'+vid.id">
        <div class="track-controls">
          <img :src="`https://img.youtube.com/vi/${vid.youtube_id}/hqdefault.jpg`" class="track-thumb">
          <div class="time-adjust">
            <span class="time-val">-{{ trackDelays[index].toFixed(2) }}s</span>
            <span class="icon arrow">❮</span>
            <span class="icon arrow">❯</span>
          </div>
        </div>
        
        <div class="track-timeline">
          <input 
            type="range" 
            min="0" 
            max="10" 
            step="0.1" 
            v-model.number="trackDelays[index]" 
            class="timeline-slider"
            :style="`--thumb-color: var(--${trackColors[index]}-color)`"
          >
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const route = useRoute()
const router = useRouter()
const config = useRuntimeConfig()

// 1. ประกาศตัวแปรพื้นฐาน
const apiVideos = ref([]) 
const vidsParam = ref(route.query.vids ? route.query.vids.split(',') : [])
const layoutType = ref(route.query.layout || 'grid-4')
const trackDelays = ref([0, 0, 0, 0])
const isPreviewing = ref(false)
const trackColors = ['red', 'blue', 'green', 'yellow']

// 2. ประกาศฟังก์ชันโหลด Session ไว้ด้านบนก่อนเรียกใช้
const loadExistingSession = async () => {
  const sessionId = route.query.session_id
  if (!sessionId) return
  try {
    const sessionData = await $fetch(`${config.public.apiBase}/api/jam/session/${sessionId}/`)
    if (sessionData && sessionData.tracks) {
      layoutType.value = sessionData.layout
      vidsParam.value = sessionData.tracks.map(t => t.video_id.toString())
      sessionData.tracks.forEach((track, index) => {
        trackDelays.value[index] = track.delay_seconds
      })
    }
  } catch (error) {
    console.error("ไม่พบข้อมูล Session นี้:", error)
  }
}

// 3. ประกาศ selectedVideos ตรงนี้ (ต้องมีก่อนที่ HTML จะเรียกใช้)
const selectedVideos = computed(() => {
  if (!apiVideos.value || apiVideos.value.length === 0) return [];
  return vidsParam.value
    .map(id => apiVideos.value.find(v => String(v.id) === String(id)))
    .filter(v => v !== undefined);
})

// 4. สั่งรันใน onMounted
onMounted(async () => {
  try {
    apiVideos.value = await $fetch(`${config.public.apiBase}/api/videos/`)
    console.log("โหลดวิดีโอสำเร็จ:", apiVideos.value)
    await loadExistingSession()
  } catch (error) {
    console.error("ดึงข้อมูลพลาด:", error)
  }
})

const generatePreview = () => {
  isPreviewing.value = !isPreviewing.value
}

const sendToQueue = async () => {
  console.log("selectedVideos ก่อนตรวจสอบ:", selectedVideos.value);
  
  const validVideos = selectedVideos.value.filter(vid => vid && vid.id);

  if (validVideos.length === 0) {
    alert(`ไม่มีวิดีโอ! (apiVideos: ${apiVideos.value ? 'มี' : 'ไม่มี'}, vidsParam: ${vidsParam.value.length})`);
    return;
  }

  const payload = {
    layout: layoutType.value || 'grid-2',
    // 2. map จาก validVideos แทน
    tracks: validVideos.map((vid, index) => ({
      video_id: vid.id,
      youtube_id: vid.youtube_id,
      // ใช้ index ของ vid เพื่อดึง delay ที่ตรงกัน
      delay_seconds: trackDelays.value[index] || 0
    }))
  };

  try {
    const response = await $fetch(`${config.public.apiBase}/api/jam/session/`, {
      method: 'POST',
      body: payload
    });

    // 3. ปรับตรงนี้: ถ้า response เป็น object ข้อมูลเลย ให้ใช้ response.id
    // ลอง console.log(response) ดูใน F12 ว่าค่า ID อยู่ตรงไหนครับ
    const sessionId = response.id || (response.data && response.data.id);
    
    alert(`ส่งข้อมูล Jam Session สำเร็จ!\nแชร์ลิงก์ให้เพื่อน: fuzik.com/jam/editor?session_id=${sessionId}`);
    setTimeout(() => { router.push('/') }, 1500);
    
  } catch (error) {
    console.error("Error saving Jam session:", error);
    alert('เกิดข้อผิดพลาดในการส่งเข้าคิว: ' + (error.message || 'ไม่ทราบสาเหตุ'));
  }
}
</script>

<style scoped>
/* กำหนดตัวแปรสีให้ดึงไปใช้ใน Slider ได้ */
.editor-container { 
  --red-color: #d32f2f;
  --blue-color: #1976d2;
  --green-color: #388e3c; 
  --yellow-color: #fbc02d;
  display: flex; gap: 20px; background-color: #000; padding: 20px; min-height: 80vh; color: #fff; font-family: sans-serif; 
}

/* แผงซ้าย */
.left-panel { border: 2px solid #fdd835; border-radius: 8px; width: 300px; padding: 15px; display: flex; flex-direction: column; gap: 15px; background: #050505; }
.ruler-toggle { display: flex; align-items: center; gap: 5px; font-size: 14px; }

/* จัดเรียง Layout Preview ให้ดูคล้ายของจริง */
.layout-preview { display: grid; gap: 2px; background: #000; border: 2px solid #ccc; height: 120px; padding: 2px; }
.layout-preview.grid-4 { grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; }
.layout-preview.grid-2 { grid-template-columns: 1fr 1fr; }
.layout-preview.grid-3 { grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; }
.layout-preview.grid-3 .layout-box:nth-child(3) { grid-column: 1 / span 2; width: 50%; justify-self: center; }
.layout-preview.grid-3-alt { grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; }
.layout-preview.grid-3-alt .layout-box:nth-child(1) { grid-row: span 2; }
.layout-box { background: #fff; color: #000; display: flex; justify-content: center; align-items: center; font-size: 24px; font-weight: bold; width: 100%; height: 100%; }

.track-colors { border: 1px solid #555; padding: 10px; display: flex; flex-direction: column; gap: 5px; width: 100px; margin: 0 auto; }
.line { height: 2px; width: 100%; }
.red-line { background: var(--red-color); }
.blue-line { background: var(--blue-color); }
.green-line { background: var(--green-color); }
.yellow-line { background: var(--yellow-color); }

.btn-generate { background: #fdd835; color: #000; border: none; padding: 10px; font-weight: bold; border-radius: 4px; cursor: pointer; }
.btn-queue { background: #fff; color: #000; border: none; padding: 8px; font-weight: bold; border-radius: 4px; cursor: pointer; margin-top: auto; }

.preview-text { margin: 0 0 5px 0; font-size: 14px; }
.preview-screen { border: 1px solid #fdd835; height: 180px; display: flex; justify-content: center; align-items: center; color: #ccc; font-size: 14px; background: #111; overflow: hidden; }
.preview-screen.active { padding: 2px; background: #000; }

/* โครงสร้าง Mini Grid ในจอ Preview */
.mini-grid-container { display: grid; gap: 1px; width: 100%; height: 100%; }
.mini-grid-container.grid-4 { grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; }
.mini-grid-container.grid-2 { grid-template-columns: 1fr 1fr; }
.mini-grid-container.grid-3 { grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; }
.mini-grid-container.grid-3 .mini-slot:nth-child(3) { grid-column: 1 / span 2; width: 50%; justify-self: center; }
.mini-grid-container.grid-3-alt { grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; }
.mini-grid-container.grid-3-alt .mini-slot:nth-child(1) { grid-row: span 2; }
.mini-slot { background: #222; }

/* แผงขวา */
.right-panel { flex: 1; display: flex; flex-direction: column; gap: 10px; }
.track-row { display: flex; border: 2px solid #ccc; border-radius: 8px; background: #111; overflow: hidden; height: 120px; }
.track-controls { width: 140px; background: #fff; color: #000; display: flex; flex-direction: column; padding: 5px; border-right: 2px solid #ccc; }
.track-thumb { width: 100%; height: 80px; object-fit: cover; border-radius: 4px; }
.time-adjust { display: flex; justify-content: space-between; align-items: center; margin-top: auto; font-size: 12px; padding: 0 5px; }
.time-val { color: #555; font-weight: bold; }
.icon { cursor: pointer; font-size: 12px; color: #d32f2f; }

/* Custom Range Slider ให้เหมือน Timeline ของจริง */
.track-timeline { flex: 1; background: #fff; position: relative; padding: 0 10px; display: flex; align-items: center; }
.timeline-slider {
  -webkit-appearance: none;
  width: 100%;
  height: 2px;
  background: #ccc;
  outline: none;
}
.timeline-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 12px;
  height: 100px;
  background: var(--thumb-color, #333);
  cursor: ew-resize;
  border-radius: 4px;
}
</style>