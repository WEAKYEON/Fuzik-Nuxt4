<template>
  <div style="padding-bottom: 50px;">
    <h2 style="color: #fdd835; margin-bottom: 5px;">My Jam Sessions</h2>
    <p style="color: #aaa; margin-bottom: 30px; font-size: 14px;">โปรเจกต์ที่คุณทำค้างไว้ เลือกเพื่อเปิดเข้าไปมิกซ์ต่อได้เลย</p>

    <div v-if="pending" class="empty-state">
      กำลังโหลดข้อมูลโปรเจกต์...
    </div>

    <div v-else-if="sessions && sessions.length > 0" class="jam-grid">
      <div 
        v-for="session in sessions" 
        :key="session.id" 
        class="jam-card" 
        @click="openSession(session.id)"
      >
        <div class="jam-header">
          <h3>Jam #{{ session.id }}</h3>
          <span class="status-badge" :class="session.status || 'pending'">
            {{ session.status || 'pending' }}
          </span>
        </div>
        
        <p><strong>Layout:</strong> {{ session.layout }}</p>
        <p><strong>คลิปในคิว:</strong> {{ session.tracks ? session.tracks.length : 0 }} รายการ</p>
        
        <div style="margin-top: 20px; text-align: right;">
          <button class="open-btn">เปิดทำต่อ ➔</button>
        </div>
      </div>
    </div>
    
    <div v-else class="empty-state">
      ยังไม่มีโปรเจกต์ที่ทำค้างไว้ ลองนำวิดีโอไปสร้าง Jam Session ดูสิ!
    </div>
  </div>
</template>

<script setup>
const router = useRouter()
const config = useRuntimeConfig()

// ดึงข้อมูล
const { data: sessions, pending } = await useFetch(`${config.public.apiBase}/api/jam/session/`)

// เปิดหน้า Editor
const openSession = (id) => {
  router.push(`/jam/editor?session_id=${id}`)
}
</script>

<style scoped>
.empty-state {
  color: #aaa;
  text-align: center;
  padding: 50px;
  background: #111;
  border-radius: 10px;
  border: 1px dashed #333;
}
.jam-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}
.jam-card {
  background: #1a1a1a;
  border: 1px solid #333;
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #ccc;
}
.jam-card:hover {
  border-color: #fdd835;
  transform: translateY(-4px);
  background: #222;
}
.jam-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}
.jam-header h3 { margin: 0; color: #fff; font-size: 20px; }
.jam-card p { margin: 8px 0; font-size: 14px; }

.status-badge {
  padding: 4px 10px;
  border-radius: 15px;
  font-size: 12px;
  font-weight: bold;
}
.status-badge.pending { background: rgba(253, 216, 53, 0.2); color: #fdd835; border: 1px solid #fdd835; }

.open-btn {
  background: transparent;
  color: #fdd835;
  border: none;
  font-weight: bold;
  cursor: pointer;
  padding: 0;
  font-size: 14px;
}
.jam-card:hover .open-btn { text-decoration: underline; }
</style>