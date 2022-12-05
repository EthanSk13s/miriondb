<script setup lang="ts">
import CardVue from "@/components/Card.vue";
import { useRoute } from 'vue-router'

const route = useRoute();

let cardId: number;

if (route.params.id) {
  cardId = Number(route.params.id);
}
</script>

<template>
  <CardVue :card-id="cardId"/>
</template>
