<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
import { ref, onMounted } from "vue";

const menuButton = ref(null);
const menuDiv = ref(null);

onMounted(() => {
  let button = menuButton.value as unknown as HTMLInputElement;
  let menu = menuDiv.value as unknown as HTMLElement;

  button.addEventListener('click', () => {
    menu.classList.toggle('hidden');
    menu.classList.toggle('flex');
  })
})
</script>

<template>
  <header>
    <nav
      class="bg-gray-800 flex md:flex-row flex-wrap gap-2 align-middle justify-between md:justify-around text-white text-center p-5 border-slate-700 border-b">
      <RouterLink to="" class="text-lg"><b>MirionDB</b></RouterLink>
      <div class="md:hidden flex items-center justify-self-end">
        <button ref="menuButton"
          class="border-slate-700 border-2 rounded p-0.5 focus:outline-none focus:ring focus:ring-slate-900">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6">
            <path fill-rule="evenodd"
              d="M3 6.75A.75.75 0 013.75 6h16.5a.75.75 0 010 1.5H3.75A.75.75 0 013 6.75zM3 12a.75.75 0 01.75-.75h16.5a.75.75 0 010 1.5H3.75A.75.75 0 013 12zm0 5.25a.75.75 0 01.75-.75h16.5a.75.75 0 010 1.5H3.75a.75.75 0 01-.75-.75z"
              clip-rule="evenodd" />
          </svg>
        </button>
      </div>
      <div ref="menuDiv"
        class="hidden md:flex basis-full md:basis-0 flex-col md:flex-row gap-8 justify-center align-middle self-center">
        <RouterLink to="/" class="self-center hover:opacity-80 w-max">Cards</RouterLink>
        <RouterLink to="/card" class="self-center hover:opacity-80 w-max">Example Card View</RouterLink>
        <RouterLink to="/about" class="self-center hover:opacity-80 w-max">History</RouterLink>
      </div>
    </nav>
  </header>
  <RouterView />
  <footer
    class="flex flex-col justify-center m-auto md:w-7/12 my-5 align-middle border-t-2 border-slate-800 text-slate-500 text-xs text-center">
    <div>Data is provided by <a class="text-teal-700 hover:text-teal-800" href="https://api.matsurihi.me/docs/">matsurihi.me</a></div>
    <div>Copyright of THE IDOLM@STER content belongs to BANDAI NAMCO Entertainment Inc.</div>
  </footer>
</template>
