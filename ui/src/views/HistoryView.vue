<script setup lang="ts">
import { ref, inject, watch } from 'vue';
import type { Ref } from 'vue';
import type { AxiosResponse } from 'axios';

import { useRoute, useRouter } from 'vue-router'

import ItemContainer from "@/components/partials/ItemContainer.vue";
import CardIcon from "@/components/partials/CardIcon.vue";
import ArrowButton from '@/components/partials/ArrowButton.vue';

import { MiniCard } from '@/models';
import { API_URL } from '@/consts';

const route = useRoute();
const router = useRouter();

let refEntries: Ref<any[][]> = ref([]);
let refHasNext: Ref<Boolean> = ref(true);
let refHasPrev: Ref<Boolean> = ref(false);

const axios: any = inject('axios');

function getHistory(page: number) {
    let newList = axios.get(`${API_URL}/history/${page}`)
        .then((response: AxiosResponse) => {
            let data = response.data.data;
            let tempList: any[][] = [];

            data.forEach((date: any) => {
                tempList.push(date)
            })

            tempList.forEach((date: any[]) => {
                let cardList: MiniCard[] = []

                date.forEach((card: any) => {
                    cardList.push(new MiniCard(card));
                })

                date.splice(0, cardList.length, ...cardList)
            })

            return {
                newList: tempList,
                hasPrev: response.data.hasPrev,
                hasNext: response.data.hasNext
            };
        })

    return newList
}

function prevPage() {
    let previous = Number(route.params.page) - 1;
    router.push(`/history/${previous}`);
}

function nextPage() {
    let next = Number(route.params.page) + 1;
    router.push(`/history/${next}`);
}

if (route.params.page) {
    getHistory(Number(route.params.page))
        .then((newInfo: any) => {
            refEntries.value = newInfo.newList;
            refHasNext.value = newInfo.hasNext;
            refHasPrev.value = newInfo.hasPrev;
        })
}

watch(
    () => route.params.page,
    async newPage => {
        getHistory(Number(newPage))
            .then((newInfo: any) => {
                refEntries.value = newInfo.newList;
                refHasNext.value = newInfo.hasNext;
                refHasPrev.value = newInfo.hasPrev;
            })
    }) 
</script>

<template>
    <main class="flex flex-col justify-center m-auto md:w-7/12 mt-5 gap-2">
        <div class="flex flex-row justify-center m-auto md:w-7/12 gap-2">
            <ArrowButton v-if="!refHasPrev" direction="left" @click="prevPage" disabled />
            <ArrowButton v-else direction="left" @click="prevPage" />

            <ArrowButton v-if="!refHasNext" direction="right" @click="prevPage" disabled />
            <ArrowButton v-else direction="right" @click="nextPage" />
        </div>
        <ItemContainer v-for="date in refEntries" :label="date[0].release.toLocaleString()" color="gray" :bold="true"
            :is-text-white="true">
            <CardIcon v-for="card in date" :name="card.name" :rarity="card.rarity" :type="card.idolType"
                :url="card.getIconUrl()" :id="card.id" />
        </ItemContainer>
        <div class="flex flex-row justify-center m-auto md:w-7/12 gap-2">
            <ArrowButton v-if="!refHasPrev" direction="left" @click="prevPage" disabled />
            <ArrowButton v-else direction="left" @click="prevPage" />

            <ArrowButton v-if="!refHasNext" direction="right" @click="prevPage" disabled />
            <ArrowButton v-else direction="right" @click="nextPage" />
        </div>
    </main>
</template>