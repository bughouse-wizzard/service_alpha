<template>
  <div id="app">
    <main-layout>
      <dashboard-view />
    </main-layout>
  </div>
</template>

<script setup lang="ts">
import MainLayout from './components/MainLayout.vue'
import DashboardView from './views/DashboardView.vue'
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-smoothing: grayscale;
  color: #2c3e50;
  height: 100vh;
}
</style>