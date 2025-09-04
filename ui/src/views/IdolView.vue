<script setup lang="ts">
import { inject, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import type { AxiosError, AxiosResponse } from 'axios';

import CardVue from "@/components/Card.vue";
import { Card } from '@/models';
import { API_URL } from '@/consts';

const route = useRoute();
const router = useRouter();
const axios: any = inject('axios');

let cardList: Card[] = [];
let refCard = ref(cardList)

function getCards(response: AxiosResponse) {
    let data = response.data.data as any[];

    if (data.length > 0) {
        data.forEach((card) => {
            refCard.value.push(new Card(card));
        })
    } else {
        router.push({ 'name': 'NotFound' })
    }
}

function handleResponseError(error: AxiosError) {
    if (error.response) {
        if (error.response.status == 404) {
            router.push({ 'name': 'NotFound' })
        }
    } else if (error.request) {
        console.log(error.request)
    } else {
        console.log(error.config)
    }
}

if (route.params.id && !route.params.rarity) {
    axios.get(`${API_URL}/idol/${route.params.id}`)
        .then(getCards)
        .catch(handleResponseError)
} else if (route.params.id && route.params.rarity) {
    axios.get(`${API_URL}/idol/${route.params.id}?rarity=${route.params.rarity}`)
        .then(getCards)
        .catch(handleResponseError)
}
</script>

<template>
    <CardVue v-for="card in refCard" :template="(card as Card)" />
</template>
