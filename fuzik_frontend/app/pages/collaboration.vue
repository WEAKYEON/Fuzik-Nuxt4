<template>
  <div class="collaboration-page">
    <h2 style="color: yellow;">Collaboration Layout Inventory</h2>
    <p style="color: #ccc; margin-bottom: 30px;">
      เลือก Layout ที่คุณต้องการ แล้วไปหยิบวิดีโอมา Jam กันได้เลย!
    </p>
    
    <div class="layout-gallery">
      <div class="layout-card" @click="startNewJam('grid-4')">
        <div class="layout-grid grid-4">
          <div class="box">1</div><div class="box">2</div><div class="box">3</div><div class="box">4</div>
        </div>
        <p class="layout-name">4-Piece Band (2x2)</p>
      </div>

      <div class="layout-card" @click="startNewJam('grid-3')">
        <div class="layout-grid grid-3">
          <div class="top-row"><div class="box">1</div><div class="box">2</div></div>
          <div class="bottom-row"><div class="box">3</div></div>
        </div>
        <p class="layout-name">Trio (Top 2, Bottom 1)</p>
      </div>

      <div class="layout-card" @click="startNewJam('grid-2')">
        <div class="layout-grid grid-2">
          <div class="box">1</div><div class="box">2</div>
        </div>
        <p class="layout-name">Duo (Side by Side)</p>
      </div>

      <div class="layout-card" @click="startNewJam('grid-3-alt')">
        <div class="layout-grid grid-3-alt">
          <div class="left-col"><div class="box">1</div></div>
          <div class="right-col"><div class="box">2</div><div class="box">3</div></div>
        </div>
        <p class="layout-name">Lead & Backups</p>
      </div>
    </div>
  </div>
</template>

<script setup>
const router = useRouter()

// ฟังก์ชันพาไปหน้าสร้าง Jam ใหม่
const startNewJam = (layoutType) => {
  router.push(`/jam/new?layout=${layoutType}`)
}
</script>

<style scoped>
/* CSS เหมือนเดิมทุกอย่างครับ */
.collaboration-page { padding: 20px; color: white; max-width: 1200px; }
.layout-gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 30px; margin-top: 20px; }
.layout-card { background-color: #111; padding: 20px; border-radius: 12px; border: 1px solid #333; display: flex; flex-direction: column; align-items: center; transition: transform 0.2s, border-color 0.2s; cursor: pointer; }
.layout-card:hover { transform: translateY(-5px); border-color: #fdd835; }
.layout-name { margin-top: 15px; margin-bottom: 0; color: #fff; font-weight: bold; font-size: 14px; }
.layout-grid { width: 100%; aspect-ratio: 16/9; display: flex; flex-direction: column; gap: 4px; background: #000; border: 4px solid #000; border-radius: 4px; overflow: hidden; }
.box { background: #fff; flex: 1; display: flex; align-items: center; justify-content: center; font-size: 32px; color: #000; font-weight: bold; }
.grid-4 { display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; gap: 4px; }
.grid-3 .top-row { display: flex; flex: 1; gap: 4px; }
.grid-3 .bottom-row { display: flex; flex: 1; justify-content: center; padding: 0 25%; }
.grid-2 { display: flex; flex-direction: row; gap: 4px; }
.grid-3-alt { display: flex; flex-direction: row; gap: 4px; }
.grid-3-alt .left-col { flex: 1; display: flex; }
.grid-3-alt .right-col { flex: 1; display: flex; flex-direction: column; gap: 4px; }
</style>