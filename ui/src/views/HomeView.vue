<script setup lang="ts">
import CardsContainer from "@/components/partials/CardsContainer.vue";
</script>

<template>
  <main class="flex flex-col justify-center m-auto md:w-7/12 mt-5 gap-2">
    <CardsContainer label="Current Event" header-class="mx-1 rounded-t p-1 text-white bg-sky-500"
      border-class="mx-1 bg-slate-800 p-1 flex flex-col md:flex-row gap-2 border rounded-b border-sky-500" />
    <CardsContainer label="Recent Additions" header-class="mx-1 rounded-t p-1 text-white bg-gray-700"
      border-class="mx-1 bg-slate-800 p-1 flex flex-col md:flex-row gap-2 border rounded-b border-gray-700" />
    <div class="flex flex-col text-white mx-2">
      <h1 class="text-2xl">About</h1>
      <div>
        Just a translated database for MLTD cards. All data is from
        <a class="text-teal-400 hover:text-teal-500" href="https://api.matsurihi.me/docs/">matsurihi.me</a>
        <br />
        Website Repository
        <a class="text-teal-400 hover:text-teal-500" href="https://github.com/EthanSk13s/miriondb">here</a>
      </div>
    </div>
    <div class="flex flex-col gap-2">
      <h1 class="text-white text-xl mx-2">Previous Additions</h1>
      <CardsContainer label="2022-11-17 15:00:00" header-class="mx-1 rounded-t p-1 text-white bg-gray-700"
        border-class="mx-1 bg-slate-800 p-1 flex flex-col md:flex-row gap-2 border rounded-b border-gray-700" />
      <CardsContainer label="2022-11-17 15:00:00" header-class="mx-1 rounded-t p-1 text-white bg-gray-700"
        border-class="mx-1 bg-slate-800 p-1 flex flex-col md:flex-row gap-2 border rounded-b border-gray-700" />
      <CardsContainer label="2022-11-17 15:00:00" header-class="mx-1 rounded-t p-1 text-white bg-gray-700"
        border-class="mx-1 bg-slate-800 p-1 flex flex-col md:flex-row gap-2 border rounded-b border-gray-700" />
    </div>
  </main>
</template>