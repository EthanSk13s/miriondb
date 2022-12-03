<script lang="ts">
import ItemContainer from '@/components/partials/ItemContainer.vue';

export default {
  components: {
    ItemContainer
  }
}
</script>

<template>
  <main class="flex flex-col justify-center bg-slate-800 m-auto md:w-7/12 mt-5">
    <div class="flex flex-row rounded-t-lg bg-pink-600 p-2 text-2xl text-white">
      <h1>[SR] RisingLight Tanaka Kotoha</h1>
    </div>
    <div class="flex flex-row flex-wrap justify-center gap-1 align-middle">
      <div>
        <div class="flex flex-row">
          <div>
            <button
              class="absolute m-1 rounded bg-stone-900 p-1 text-sm text-white hover:bg-stone-800"
            >
              Awaken
            </button>
          </div>
        </div>
        <img
          class="h-auto w-fit md:h-auto md:w-96"
          src="https://theater.miriondb.com/card/017kth0353_0.png"
          alt=""
        />
      </div>
      <div class="m-1 flex flex-1 flex-col gap-2">
        <div class="flex flex-row">
          <div>
            <span
              class="m-1 rounded bg-slate-600 px-1 py-0.5 font-bold text-white"
              >Level</span
            >
            <button class="m-1 rounded bg-yellow-500 px-2 text-white">-</button>
            <input
              class="w-1/12 rounded bg-gray-700 px-0.5 text-center text-white focus:outline-none focus:ring focus:ring-violet-300"
              type="text"
              maxlength="2"
              name=""
              id=""
              value="1"
            />
            <button class="m-1 rounded bg-yellow-500 px-2 text-white">+</button>
          </div>
          <div>
            <span
              class="m-1 rounded bg-slate-600 px-1 py-0.5 font-bold text-white"
              >Master Rank</span
            >
            <button class="m-1 rounded bg-yellow-500 px-2 text-white">-</button>
            <input
              class="w-1/12 rounded bg-gray-700 px-0.5 text-center text-white focus:outline-none focus:ring focus:ring-violet-300"
              type="text"
              maxlength="1"
              name=""
              id=""
              value="0"
            />
            <button class="m-1 rounded bg-yellow-500 px-2 text-white">+</button>
          </div>
        </div>
        <div class="flex flex-row gap-3">
          <div class="text-white">
            <span class="m-1 rounded bg-green-500 px-1 py-0.5 font-bold"
              >Life</span
            >100
          </div>
          <div class="text-white">
            <span class="m-1 rounded bg-red-500 px-1 py-0.5 font-bold"
              >Vocal</span
            >100
          </div>
          <div class="text-white">
            <span class="m-1 rounded bg-blue-500 px-1 py-0.5 font-bold"
              >Dance</span
            >100
          </div>
          <div class="text-white">
            <span class="m-1 rounded bg-yellow-500 px-1 py-0.5 font-bold"
              >Visual</span
            >100
          </div>
        </div>
        <div class="flex flex-col">
          <ItemContainer label="Skill" color="yellow-300">
            Every 9 seconds, there is a 40% chance that your Perfect/Great score
            will increase by 30. When there are two or more Score Up cards in
            the unit, the score of Perfect/Great is increased to 37, and when
            there are one or more cards that are Fusion Combo, Great/Good is set
            to Perfect for 5 seconds
          </ItemContainer>
        </div>
        <div class="flex flex-col">
          <ItemContainer label="Skill" color="yellow-300">
            Princess idols' visual value is increased by 60%
          </ItemContainer>
        </div>
        <div class="flex flex-col gap-2">
          <div
            class="m-1 w-min rounded bg-cyan-400 px-1 py-0.5 font-bold text-white"
          >
            Costumes
          </div>
          <div class="mx-2 flex flex-row flex-wrap gap-3">
            <img
              class="h-auto w-1/4 rounded md:h-auto md:w-24"
              src="https://theater.miriondb.com/costumes/017kth0353.png"
              alt=""
            />
            <img
              class="h-auto w-1/4 rounded md:h-auto md:w-24"
              src="https://theater.miriondb.com/costumes/017kth0353_v.png"
              alt=""
              srcset=""
            />
          </div>
        </div>
      </div>
    </div>
    <div>
      <img
        class="w-screen h-auto"
        src="https://theater.miriondb.com/card_bg/017kth0324_0.png"
        alt=""
      />
    </div>
  </main>
</template>
