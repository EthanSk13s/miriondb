<script lang="ts">
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
          url = 'https://chupa.miriondb.com/static/imgs/icon_overlays/1.png';
          break;
        case 2:
          url = 'https://chupa.miriondb.com/static/imgs/icon_overlays/2.png';
          break;
        case 3:
          url = 'https://chupa.miriondb.com/static/imgs/icon_overlays/3.png';
          break;
        case 4:
          url = 'https://chupa.miriondb.com/static/imgs/icon_overlays/4.png';
          break;
        default:
          url = 'https://chupa.miriondb.com/static/imgs/icon_overlays/1.png';
      }

      return url
    },
    matchType() {
      let url: string;
      switch(this.type) {
        case 1:
          url = 'https://chupa.miriondb.com/static/imgs/icon_overlays/1_type.png';
          break;
        case 2:
          url = 'https://chupa.miriondb.com/static/imgs/icon_overlays/2_type.png';
          break;
        case 3:
          url = 'https://chupa.miriondb.com/static/imgs/icon_overlays/3_type.png';
          break;
        case 5:
          url = 'https://chupa.miriondb.com/static/imgs/icon_overlays/5_type.png';
          break;
        default:
          url = 'https://chupa.miriondb.com/static/imgs/icon_overlays/5_type.png';
      }

      return url;
    },
    redirect() {
      this.$router.push(`/card/${this.id}`)
    }
  }
}
</script>

<template>
    <div @click="redirect" class="cursor-pointer flex w-fit flex-row rounded bg-slate-700 align-middle hover:opacity-80">
    <div class="w-12">
      <img class="absolute h-12 w-12" :src="matchType()" alt="" />
      <img class="absolute h-12 w-12" :src="matchRarity()" alt="" />
      <img class="h-12 w-12" :src="url" alt="" srcset="" />
    </div>
    <div class="self-center px-1 text-xs text-white">
      {{ name }}
    </div>
  </div>
</template>
