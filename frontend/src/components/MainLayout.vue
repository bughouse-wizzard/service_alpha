<template>
  <div class="flex h-screen bg-gray-100">
    <!-- Sidebar -->
    <div class="w-64 bg-gray-800 text-white">
      <div class="p-4">
        <h1 class="text-2xl font-bold">Service Alpha</h1>
        <p class="text-gray-400 text-sm mt-1">Search Dashboard</p>
      </div>
      
      <nav class="mt-6">
        <a href="#" class="block py-2 px-4 bg-gray-700 text-white">
          <i class="mr-2">🔍</i> New Search
        </a>
        <a href="#" class="block py-2 px-4 text-gray-300 hover:bg-gray-700">
          <i class="mr-2">📋</i> Search History
        </a>
        <a href="#" class="block py-2 px-4 text-gray-300 hover:bg-gray-700">
          <i class="mr-2">⚙️</i> Settings
        </a>
      </nav>
      
      <div class="absolute bottom-0 w-64 p-4 border-t border-gray-700">
        <div class="flex items-center">
          <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
            <span class="text-white">U</span>
          </div>
          <div class="ml-3">
            <p class="text-sm">User</p>
            <p class="text-xs text-gray-400">Administrator</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Top Bar -->
      <header class="bg-white shadow">
        <div class="px-6 py-4">
          <div class="flex justify-between items-center">
            <h2 class="text-xl font-semibold text-gray-800">{{ currentView }}</h2>
            <div class="flex items-center space-x-4">
              <button class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
                <i class="mr-2">+</i> New Search
              </button>
              <div class="relative">
                <span class="absolute inset-y-0 left-0 flex items-center pl-3">
                  <i>🔔</i>
                </span>
                <span class="inline-block w-2 h-2 bg-red-500 rounded-full absolute top-0 right-0"></span>
              </div>
            </div>
          </div>
        </div>
      </header>
      
      <!-- Content Area -->
      <main class="flex-1 overflow-y-auto p-6">
        <slot></slot>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const currentView = ref('Dashboard')
</script>

<style scoped>
/* Additional custom styles if needed */
</style>