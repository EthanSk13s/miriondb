<script lang="ts">
import { RouterLink } from 'vue-router';

import ItemContainer from '@/components/partials/ItemContainer.vue';
import DigitTextInput from '@/components/partials/DigitTextInput.vue';

import { Card, CardStatType } from '@/models';
import { API_URL } from '@/consts';

export default {
    data() {
        return {
            card: new Card(),
            isAwaken: false,
            currentLevel: 1,
            currentRank: 0,
            currentVocal: 0,
            currentDance: 0,
            currentVisual: 0,
            maxLevel: 0,
            hasNoBaseImg: false
        }
    },
    props: {
        cardId: Number,
        template: Card
    },
    components: {
        ItemContainer,
        DigitTextInput
    },
    methods: {
        fetchCard(id: string) {
            this.$http.get(`${API_URL}/card/${id}`)
                .then((response) => {
                    if (!response.data.data.error) {
                        this.$data.card = new Card(response.data.data);

                        this.setData(this.$data.card);
                    } else {
                        this.$router.push({ 'name': 'NotFound' })
                    }
                })
        },
        mapRarity(rarity: number) {
            let rarityShort: string;
            switch (rarity) {
                case 1:
                    rarityShort = 'N';
                    break;
                case 2:
                    rarityShort = 'R';
                    break;
                case 3:
                    rarityShort = 'SR';
                    break;
                case 4:
                    rarityShort = 'SSR';
                    break;
                default:
                    rarityShort = '??';
            }

            return rarityShort;
        },
        constructColorType(idolType: number) {
            let className: string;
            switch (idolType) {
                case 1:
                    className = 'flex flex-row rounded-t-lg bg-pink-600 p-2 text-2xl text-white';
                    break;
                case 2:
                    className = 'flex flex-row rounded-t-lg bg-blue-600 p-2 text-2xl text-white';
                    break;
                case 3:
                    className = 'flex flex-row rounded-t-lg bg-yellow-500 p-2 text-2xl text-white';
                    break;
                case 5:
                    className = 'flex flex-row rounded-t-lg bg-green-400 p-2 text-2xl text-white';
                    break;
                default:
                    className = 'flex flex-row rounded-t-lg p-2 text-2xl text-white';
            }

            return className;
        },
        updateRank(newRank: number) {
            this.currentRank = newRank;
            this.changeStats();
        },
        updateLevel(newLevel: number) {
            this.currentLevel = newLevel;
            this.changeStats();
        },
        changeStats() {
            let level = this.currentLevel;
            let rank = this.currentRank;

            let newVocal = this.card.calcStatAtX(this.isAwaken, level, this.maxLevel, CardStatType.VOCAL);
            let newDance = this.card.calcStatAtX(this.isAwaken, level, this.maxLevel, CardStatType.DANCE);
            let newVisual = this.card.calcStatAtX(this.isAwaken, level, this.maxLevel, CardStatType.VISUAL);

            this.currentVocal = newVocal! + this.calcRankBonus(rank, this.card.stats?.vocalRankBonus!);
            this.currentDance = newDance! + this.calcRankBonus(rank, this.card.stats?.danceRankBonus!);
            this.currentVisual = newVisual! + this.calcRankBonus(rank, this.card.stats?.visualRankBonus!);
        },
        calcRankBonus(rank: number, value: number) {
            return rank * value;
        },
        setData(card: Card) {
            switch (card.rarity) {
                case 1:
                    this.maxLevel = 20;
                    break;
                case 2:
                    this.maxLevel = 40;
                    break;
                case 3:
                    this.maxLevel = 60;
                    break;
                case 4:
                    this.maxLevel = 80;
                    break;
                default:
                    this.maxLevel = 0;
            }

            this.currentVocal = card.stats?.vocal!;
            this.currentDance = card.stats?.dance!;
            this.currentVisual = card.stats?.visual!;
        },
        onBaseCardFail() {
            this.isAwaken = true;
            this.hasNoBaseImg = true;

            let cardImage = this.$refs.cardImage as HTMLImageElement;
            cardImage.src = this.card.getCardImageUrl(this.isAwaken);
        }
    },
    mounted() {
        if (this.cardId) {
            this.fetchCard(String(this.cardId))
        }

        if (this.template) {
            this.card = this.template;

            this.setData(this.$data.card);
        }

        let awakenButton = this.$refs.awakenButton as HTMLElement;
        awakenButton.addEventListener('click', () => {
            if (this.isAwaken) {
                this.isAwaken = false;
                this.maxLevel -= 10;
            } else {
                this.isAwaken = true;
                this.maxLevel += 10;
            }

            this.changeStats();
        });
    },
    computed: {
        isDisabled() {
            return this.hasNoBaseImg;
        }
    }
}
</script>

<template>
    <main class="flex flex-col justify-center bg-slate-800 m-auto lg:w-7/12 mt-5 rounded-t-lg">
        <div :class="constructColorType(card.idolType)">
            <h1>{{ `[${mapRarity(card.rarity)}] ` + card.name }}</h1>
        </div>
        <div class="flex flex-row flex-wrap justify-center gap-1 align-middle">
            <div>
                <div class="flex flex-row absolute">
                    <div v-if="!isDisabled">
                        <button ref="awakenButton"
                            class="m-1 rounded bg-stone-900 p-1 text-sm text-white hover:bg-stone-800 transition-colors duration-200">
                            Awaken
                        </button>
                    </div>
                    <div v-if="cardId">
                        <RouterLink :to="`/idol/${card.idolId}`">
                            <button
                                class="m-1 rounded bg-stone-900 p-1 text-sm text-white hover:bg-stone-800 transition-colors duration-200">
                                Other Cards
                            </button>
                        </RouterLink>
                    </div>
                </div>
                <img ref="cardImage" class="h-auto w-fit md:h-auto md:w-96" @error="onBaseCardFail" v-lazy="{ src: card.getCardImageUrl(isAwaken) }" alt="" />
            </div>
            <div class="m-1 flex flex-1 flex-col gap-2">
                <div class="flex flex-row">
                    <div>
                        <span class="m-1 rounded bg-slate-600 px-1 py-0.5 font-bold text-white">Level</span>
                        <DigitTextInput v-model:input-value="currentLevel" @update:input-value="updateLevel" :min="1"
                            :max="maxLevel" />
                    </div>
                    <div>
                        <span class="m-1 rounded bg-slate-600 px-1 py-0.5 font-bold text-white">Master Rank</span>
                        <DigitTextInput v-model:input-value="currentRank" @update:input-value="updateRank" :min="0"
                            :max="card.stats?.maxMasterRank" />
                    </div>
                </div>
                <div class="flex flex-row gap-3">
                    <div class="text-white">
                        <span class="m-1 rounded bg-green-500 px-1 py-0.5 font-bold">Life</span>{{ card.stats?.life }}
                    </div>
                    <div class="text-white">
                        <span class="m-1 rounded bg-red-500 px-1 py-0.5 font-bold">Vocal</span>{{ currentVocal }}
                    </div>
                    <div class="text-white">
                        <span class="m-1 rounded bg-blue-500 px-1 py-0.5 font-bold">Dance</span>{{ currentDance }}
                    </div>
                    <div class="text-white">
                        <span class="m-1 rounded bg-yellow-500 px-1 py-0.5 font-bold">Visual</span>{{ currentVisual }}
                    </div>
                </div>
                <div class="flex flex-col">
                    <ItemContainer :label='("Skill: " + card.skill?.name)' color="yellow">
                        {{ card.skill?.description }}
                    </ItemContainer>
                </div>
                <div class="flex flex-col">
                    <ItemContainer label="Center Skill" color="yellow">
                        {{ card.centerSkill?.description }}
                    </ItemContainer>
                </div>
                <div v-if="card.costumes" class="flex flex-col gap-2">
                    <div class="m-1 w-min rounded bg-cyan-400 px-1 py-0.5 font-bold text-white">
                        Costumes
                    </div>
                    <div class="mx-2 flex flex-row flex-wrap gap-3">
                        <img v-for="url in card.getCostumesUrl()" class="h-auto w-1/4 rounded md:h-auto md:w-24"
                            alt="" v-lazy="{ src: url }"/>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="(card.rarity == 4 && !([5, 7, 10, 13, 16].indexOf(card.exType, 0) >= 0))">
            <img class="w-screen h-auto" v-lazy="{ src: card.getBgImageUrl(isAwaken)! }" alt="" />
        </div>
    </main>
</template>
