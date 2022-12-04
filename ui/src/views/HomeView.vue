<script setup lang="ts">
import ItemContainer from "@/components/partials/ItemContainer.vue";
import CardIcon from "@/components/partials/CardIcon.vue";
</script>

<template>
  <main class="flex flex-col justify-center m-auto md:w-7/12 mt-5 gap-2">
    <div class="p-1 m-1">
      <form action="" method="GET">
        <input type="text"
          class="w-full py-1 pl-2 bg-slate-800 text-white rounded focus:outline-none focus:ring focus:ring-violet-400"
          placeholder="Search for Cards (E.g kotoha ssr 5 | kotoha ssr)">
      </form>
    </div>
    <ItemContainer label="Current Event" color="sky" :bold="true" :is-text-white="true">
      <CardIcon />
      <CardIcon />
      <CardIcon />
      <CardIcon />
    </ItemContainer>
    <ItemContainer label="Recent Additions" color="gray" :bold="true" :is-text-white="true">
      <CardIcon />
      <CardIcon />
      <CardIcon />
      <CardIcon />
    </ItemContainer>
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
      <ItemContainer label="Dec 3 2022, 15:00" color="gray" :bold="true" :is-text-white="true">
        <CardIcon />
        <CardIcon />
        <CardIcon />
        <CardIcon />
      </ItemContainer>
      <ItemContainer label="Dec 3 2022, 15:00" color="gray" :bold="true" :is-text-white="true">
        <CardIcon />
        <CardIcon />
        <CardIcon />
        <CardIcon />
      </ItemContainer>
      <ItemContainer label="Dec 3 2022, 15:00" color="gray" :bold="true" :is-text-white="true">
        <CardIcon />
        <CardIcon />
        <CardIcon />
        <CardIcon />
      </ItemContainer>
    </div>
  </main>
</template>
