<template>
  <div class="fuzik-container">
    <aside class="sidebar">
      <h2 style="color: yellow; margin-bottom: 30px;">FUZIK</h2>
      <ul>
        <li><NuxtLink to="/" exact-active-class="active-link">Dashboard</NuxtLink></li>
        <li><NuxtLink to="/my-jams" active-class="active-link">My Jams</NuxtLink></li>
        <li><NuxtLink to="/upload" active-class="active-link">Upload</NuxtLink></li>
        <li><NuxtLink to="/collaboration" active-class="active-link">Collaboration</NuxtLink></li>
      </ul>
    </aside>

    <main class="content">
      <NuxtPage />
    </main>
  </div>
</template>

<style>
/* CSS กลางสำหรับโครงสร้างหลัก */
body { margin: 0; background-color: #000; color: #fff; font-family: sans-serif; }
.fuzik-container { display: flex; min-height: 100vh; }
.sidebar { width: 200px; border-right: 1px solid #333; padding: 20px; }
.sidebar ul { list-style: none; padding: 0; }
.sidebar li { margin-bottom: 15px; }
/* ตกแต่งลิงก์เมนู */
.sidebar a { text-decoration: none; color: #ccc; font-size: 16px; display: block; }
.sidebar a:hover { color: #fff; }
.sidebar a.active-link { color: yellow; font-weight: bold; }
.content { flex: 1; padding: 20px; }
</style>