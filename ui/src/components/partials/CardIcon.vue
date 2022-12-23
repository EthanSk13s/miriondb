<script lang="ts">
import { RouterLink } from 'vue-router';
import { ICONS_URL } from '@/consts';

export default {
  props: {
    name: String,
    rarity: Number,
    type: Number,
    url: String,
    id: Number
  },
  methods: {
    matchRarity() {
      let url: string;
      switch (this.rarity) {
        case 1:
          url = `${ICONS_URL}/1.png`;
          break;
        case 2:
          url = `${ICONS_URL}/2.png`;
          break;
        case 3:
          url = `${ICONS_URL}/3.png`;
          break;
        case 4:
          url = `${ICONS_URL}/4.png`;
          break;
        default:
          url = `${ICONS_URL}/1.png`;
      }

      return url
    },
    matchType() {
      let url: string;
      switch(this.type) {
        case 1:
          url = `${ICONS_URL}/1_type.png`;
          break;
        case 2:
          url = `${ICONS_URL}/2_type.png`;
          break;
        case 3:
          url = `${ICONS_URL}/3_type.png`;
          break;
        case 5:
          url = `${ICONS_URL}/5_type.png`;
          break;
        default:
          url = `${ICONS_URL}/5_type.png`;
      }

      return url;
    }
  }
}
</script>

<template>
  <RouterLink :to="`/card/${id}`">
    <div class="flex w-fit flex-row rounded bg-slate-700 align-middle hover:opacity-80">
    <div class="w-12">
      <img class="absolute h-12 w-12" :src="matchType()" alt="" />
      <img class="absolute h-12 w-12" :src="matchRarity()" alt="" />
      <img class="h-12 w-12" :src="url" alt="" srcset="" />
    </div>
    <div class="self-center px-1 text-xs text-white">
      {{ name }}
    </div>
  </div>
</RouterLink>
</template>
