<script setup lang="ts">
import { inject, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import type { AxiosResponse } from 'axios';

import CardVue from "@/components/Card.vue";
import { Card } from '@/models';

const route = useRoute();
const router = useRouter();
const axios: any = inject('axios');

let cardList: Card[] = [];
let refCard = ref(cardList)

if (route.params.id) {
    axios.get(`http://127.0.0.1:5500/idol/${route.params.id}`)
        .then((response: AxiosResponse) => {
            let data = response.data.data as any[];

            if (data.length > 0) {
                data.forEach((card) => {
                    refCard.value.push(new Card(card));
                })
            } else {
                router.push({'name': 'NotFound'})
            }
        })
}
</script>

<template>
    <CardVue v-for="card in refCard" :template="(card as Card)" />
</template>
