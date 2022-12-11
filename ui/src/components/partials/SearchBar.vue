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

        searchBar.addEventListener('input', (ev) => {
            this.searchString = searchBar.value;
        })
    }
}
</script>

<template>
    <div class="flex flex-col relative">
        <input ref="search" type="text"
            class="w-full py-1 pl-2 bg-slate-800 text-white rounded focus:outline-none focus:ring focus:ring-violet-400"
            :placeholder="placeholder">
        <div v-if="searchString" class="top-full inset-x-0 py-1 pl-2 bg-slate-800 text-white rounded-b z-50 shadow-lg absolute">
            <div class="py-1 cursor-pointer" v-for="result in matchResult()">
                {{result}}
            </div>
        </div>
    </div>
</template>