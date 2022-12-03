<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
</script>

<template>
  <header>
    <nav
      class="bg-gray-800 flex flex-col md:flex-row flex-wrap gap-2 align-middle justify-around text-white text-center p-5 border-slate-700 border-b-2"
    >
      <RouterLink to="" class="text-lg"><b>MirionDB</b></RouterLink>
      <div
        class="flex flex-col md:flex-row gap-3 justify-center align-middle self-center"
      >
        <RouterLink to="/" class="self-center hover:opacity-80"
          >Cards</RouterLink
        >
        <RouterLink to="/card" class="self-center hover:opacity-80"
          >Example Card View</RouterLink
        >
        <RouterLink to="/about" class="self-center hover:opacity-80"
          >History</RouterLink
        >
      </div>
    </nav>
  </header>
  <RouterView />
</template>
