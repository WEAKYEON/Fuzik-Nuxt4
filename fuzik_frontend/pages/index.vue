<template>
  <div>
    <div class="tab-container">
      <button :class="['tab-btn', { active: currentTab === 'solo' }]" @click="currentTab = 'solo'">Solo</button>
      <button :class="['tab-btn', { active: currentTab === 'collab' }]" @click="currentTab = 'collab'">Collaboration</button>
    </div>

    <div class="search-bar">
      <input v-model="searchQuery" type="text" placeholder="Song name or artist name">
      <button class="search-btn">Search</button>
    </div>

    <div v-if="filteredVideos.length === 0" style="text-align: center; color: #aaa; margin-top: 50px;">
      ไม่พบวิดีโอที่คุณค้นหา
    </div>

    <div class="video-grid" v-else>
      <div 
        class="video-card" 
        v-for="video in filteredVideos" 
        :key="video.id" 
        @click="video.youtube_id ? playVideo(video) : null"
      >
        <div class="thumbnail-wrapper">
          <img v-if="video.youtube_id" :src="`https://img.youtube.com/vi/${video.youtube_id}/hqdefault.jpg`" :alt="video.title">
          
          <div v-else class="placeholder-thumb">
            รอดันขึ้น YouTube
          </div>

          <span class="type-badge">{{ video.type === 'solo' ? 'Solo' : 'Jamming' }}</span>
          <div class="play-icon" v-if="video.youtube_id">▶</div>
        </div>
        
        <div class="video-info">
          <h4 class="title">{{ video.title }}</h4>
          <p class="author">{{ video.author }}</p>

          <p class="stats" v-if="video.youtube_id">{{ video.views }} views • {{ video.time }}</p>
          
          <button 
            v-else 
            @click.stop="uploadToYT(video.id)" 
            class="push-btn"
          >
            Push to YouTube
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const currentTab = ref('solo')
const searchQuery = ref('') 
const router = useRouter() 

// ดึงข้อมูลจาก Django
const { data: apiVideos } = await useFetch('https://downloadlovedy.pythonanywhere.com/api/videos/')

const videos = computed(() => {
  if (!apiVideos.value) return []
  return apiVideos.value
    .map((v, index) => ({
      id: v.id,
      title: v.title,
      youtube_id: v.youtube_id,
      type: v.video_type, 
      author: 'Fuzik User', 
      views: (v.id * 13) % 100,
      time: new Date(v.uploaded_at).toLocaleDateString('th-TH')
    }))
})

const filteredVideos = computed(() => {
  return videos.value.filter(video => {
    const matchTab = video.type === currentTab.value
    const matchSearch = video.title.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
                        video.author.toLowerCase().includes(searchQuery.value.toLowerCase())
    return matchTab && matchSearch
  })
})

const playVideo = (video) => { 
  router.push(`/video/${video.id}`) 
}

// ฟังก์ชันสั่งยิง API ขึ้น YouTube ที่เราเพิ่งทำกันในฝั่ง Django
const uploadToYT = async (id) => {
  if (!confirm('ต้องการอัปโหลดวิดีโอนี้ขึ้น YouTube ใช่หรือไม่?')) return;
  
  try {
    alert('ระบบกำลังทำงาน... โปรดรอสักครู่ ห้ามปิดหน้าต่างนี้นะครับ (อาจใช้เวลาหลายวินาที)');
    
    // ยิงไปหา API ตัวใหม่ที่เราเพิ่งสร้าง
    const response = await $fetch(`https://downloadlovedy.pythonanywhere.com/api/videos/${id}/push-youtube/`, {
      method: 'POST'
    });
    
    alert(`อัปโหลดสำเร็จ! 🎉 (YouTube ID: ${response.youtube_id})`);
    window.location.reload(); 
    
  } catch (error) {
    alert('เกิดข้อผิดพลาดในการอัปโหลด เช็คเทอร์มินัลหลังบ้านดูนะครับ');
  }
}
</script>

<style scoped>
.tab-container { display: flex; justify-content: center; margin-bottom: 20px; }
.tab-btn { background: transparent; color: #fff; border: 1px solid #fff; padding: 10px 40px; cursor: pointer; }
.tab-btn:first-child { border-radius: 20px 0 0 20px; }
.tab-btn:last-child { border-radius: 0 20px 20px 0; }
.tab-btn.active { background-color: #fdd835; color: #000; border-color: #fdd835; font-weight: bold; }

.search-bar { text-align: center; margin-bottom: 30px; }
.search-bar input { padding: 10px; width: 400px; border-radius: 20px; border: none; outline: none; }
.search-btn { padding: 10px 20px; border-radius: 20px; background-color: #fdd835; border: none; font-weight: bold; cursor: pointer; margin-left: 10px; }

.video-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
.video-card { cursor: pointer; transition: transform 0.2s; }
.video-card:hover { transform: scale(1.05); }
.thumbnail-wrapper { position: relative; border-radius: 10px; overflow: hidden; background: #222; }
.thumbnail-wrapper img { width: 100%; aspect-ratio: 16/9; object-fit: cover; display: block; transition: opacity 0.3s; }
.video-card:hover .thumbnail-wrapper img { opacity: 0.7; }
.play-icon { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 40px; color: yellow; opacity: 0; transition: opacity 0.3s; }
.video-card:hover .play-icon { opacity: 1; }
.type-badge { position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.7); padding: 3px 10px; border-radius: 5px; font-size: 12px; }
.video-info { margin-top: 10px; }
.title { margin: 0 0 5px 0; font-size: 16px; text-overflow: ellipsis; white-space: nowrap; overflow: hidden; }
.author, .stats { margin: 0; color: #aaa; font-size: 13px; }

/* CSS สำหรับปกสำรองและปุ่ม Push */
.placeholder-thumb { width: 100%; aspect-ratio: 16/9; display: flex; align-items: center; justify-content: center; color: #777; background: #333; font-size: 14px; }
.push-btn { background: #fdd835; color: #000; border: none; padding: 6px 10px; border-radius: 4px; font-weight: bold; cursor: pointer; margin-top: 5px; width: 100%; transition: background 0.2s; }
.push-btn:hover { background: #ffea00; }
</style>