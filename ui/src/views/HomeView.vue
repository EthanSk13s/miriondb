<script setup lang="ts">
import { ref, inject, onMounted } from 'vue';
import type { Ref } from 'vue';
import type { AxiosResponse } from 'axios';

import { Card, CardEvent } from '@/models';
import { IDOL_NAMES } from '@/consts';
import ItemContainer from "@/components/partials/ItemContainer.vue";
import CardIcon from "@/components/partials/CardIcon.vue";
import SearchBar from '@/components/partials/SearchBar.vue';

const axios: any = inject('axios');

let refEventCards: Ref<Card[]> = ref([]);
let refEvent: Ref<CardEvent> = ref(new CardEvent());
let refRecentCards: Ref<Card[]> = ref([]);
let refPreviousCards: Ref<any[][]> = ref([]);
let refEventString = ref('');

axios.get(`http://127.0.0.1:5500/latest`)
  .then((response: AxiosResponse) => {
    let data = response.data.data

    refEvent.value = new CardEvent(data.currentEvent.event);
    refEventString.value = refEvent.value.name;

    if (data.currentEvent.cards) {
      data.currentEvent.cards.forEach((cards: any) => {
        refEventCards.value.push(new Card(cards))
      })
    }

    data.recentCards.forEach((cards: any) => {
      refRecentCards.value.push(new Card(cards))
    })

    data.previousAdditions.forEach((date: any) => {
      refPreviousCards.value.push(date);
    })

    refPreviousCards.value.forEach((date: any[]) => {
      let tempList: Card[] = []

      date.forEach((card: any) => {
        tempList.push(new Card(card));
      })

      date.splice(0, tempList.length, ...tempList)
    })
  })

onMounted(() => {
  setInterval(() => {
    let delta = refEvent.value.getDeltaTime();
    if (delta) {
      let days = Math.floor(delta / (1000 * 60 * 60 * 24));
      let hours = String(Math.floor((delta % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))).padStart(2, "0");
      let minutes = String(Math.floor((delta % (1000 * 60 * 60)) / (1000 * 60))).padStart(2, "0");
      let seconds = String(Math.floor((delta % (1000 * 60)) / 1000)).padStart(2, "0");

      refEventString.value = `${refEvent.value.name} ends in ${days}d, ${hours}:${minutes}:${seconds}`;
    } else {
      refEventString.value = `${refEvent.value.name} has ended, Good Work Everyone!`;
    }
  }, 1000)
})

</script>

<template>
  <main class="flex flex-col justify-center m-auto md:w-7/12 mt-5 gap-2">
    <div class="p-1 m-1">
      <form action="" method="GET">
        <SearchBar placeholder="Search for Cards (E.g kotoha ssr 5 | kotoha ssr)" :result-list="IDOL_NAMES" />
      </form>
    </div>
    <ItemContainer :label="refEventString" color="sky" :bold="true" :is-text-white="true">
      <CardIcon v-for="card in refEventCards" :name="card.name" :rarity="card.rarity" :type="card.idolType"
        :url="card.getIconUrl()" :id="card.id" />
    </ItemContainer>
    <ItemContainer label="Recent Additions" color="gray" :bold="true" :is-text-white="true">
      <CardIcon v-for="card in refRecentCards" :name="card.name" :rarity="card.rarity" :type="card.idolType"
        :url="card.getIconUrl()" :id="card.id" />
    </ItemContainer>
    <div class="flex flex-col text-white mx-2">
      <h1 class="text-2xl">About</h1>
      <div>
        <p>
          Just a translated database for MLTD cards. All data is from
          <a class="text-teal-400 hover:text-teal-500" href="https://api.matsurihi.me/docs/">matsurihi.me</a>
          <br />
          Website Repository
          <a class="text-teal-400 hover:text-teal-500" href="https://github.com/EthanSk13s/miriondb">here</a>
        </p>
      </div>
    </div>
    <div class="flex flex-col gap-2">
      <h1 class="text-white text-xl mx-2">Previous Additions</h1>
      <ItemContainer v-for="date in refPreviousCards" :label="date[0].release.toLocaleString()" color="gray"
        :bold="true" :is-text-white="true">
        <CardIcon v-for="card in date" :name="card.name" :rarity="card.rarity" :type="card.idolType"
          :url="card.getIconUrl()" :id="card.id" />
      </ItemContainer>
    </div>
  </main>
</template>
