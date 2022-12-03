<script lang="ts">
import CardIcon from "./CardIcon.vue";

export default {
    props: {
        label: String,
        color: String,
        headerClass: String,
        borderClass: String
    },
    components: {
        CardIcon,
    },
    methods: {
        constructHeaderClass() {
            return `mx-1 rounded-t p-1 text-white bg-${this.color}`
        },
        constructBodyClass() {
            return `mx-1 bg-slate-800 p-1 flex flex-col lg:flex-row gap-2 flex-wrap border rounded-b border-${this.color}`
        }
    }
};
</script>

<template>
    <div class="mx-1 md:mx-0 flex flex-col flex-wrap">
        <div>
            <div :class="constructHeaderClass()">
                <b>{{ label }}</b>
            </div>
        </div>
        <div :class="constructBodyClass()">
            <CardIcon />
            <CardIcon />
            <CardIcon />
            <CardIcon />
        </div>
    </div>
</template>
