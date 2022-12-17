<script lang="ts">
import type { PropType } from 'vue'

export default {
    data() {
        return {
            searchString: ''
        }
    },
    props: {
        placeholder: String,
        resultList: {
            type: [] as PropType<String[]>
        }
    },
    methods: {
        matchResult() {
            let filtered = this.resultList!.filter((result) => {
                return result.substring(0, this.searchString.length).toLowerCase() == this.searchString.toLowerCase()
            })

            return filtered;
        }
    },
    mounted() {
        let searchBar = this.$refs.search as HTMLInputElement;

        searchBar.addEventListener('input', () => {
            this.searchString = searchBar.value;
        })
    },
    updated() {
        if (this.searchString) {
            let items = this.$refs.items as HTMLElement[];
            let searchBar = this.$refs.search as HTMLInputElement;

            items.forEach((item) => {
                item.addEventListener('click', () => {
                    searchBar.value = item.getElementsByTagName('input')[0].value;

                    this.searchString = '';
                })
            })
        }
    }
}
</script>

<template>
    <div class="flex flex-col relative">
        <input ref="search" type="text"
            class="w-full py-1 pl-2 bg-slate-800 text-white rounded focus:outline-none focus:ring focus:ring-violet-400"
            :placeholder="placeholder">
        <div v-if="searchString"
            class="top-full inset-x-0 p-1 my-2 bg-slate-800 text-white rounded-lg z-50 drop-shadow-2xl absolute">
            <div ref="items" class="pl-2 py-1 cursor-pointer hover:bg-slate-900 hover:rounded" v-for="result in matchResult()">
                <strong>{{ result.substring(0, searchString.length) }}</strong>{{ result.substring(searchString.length) }}
                <input type="hidden" :value="result">
            </div>
        </div>
    </div>
</template>