<script lang="ts">
export default {
    props: {
        label: String,
        color: String,
        isTextWhite: Boolean,
        bold: Boolean
    },
    methods: {
        constructHeaderClass() {
            let textColor: string = 'text-black';
            if (this.isTextWhite) {
                textColor = 'text-white';
            }
            return `mx-1 rounded-t p-1 ${textColor} bg-${this.color}`
        },
        constructBodyClass() {
            return `mx-1 bg-slate-800 p-1 flex flex-col text-white lg:flex-row gap-2 flex-wrap border rounded-b border-${this.color}`
        }
    }
};
</script>

<template>
    <div class="mx-1 md:mx-0 flex flex-col flex-wrap">
        <div>
            <div :class="constructHeaderClass()">
                <b v-if="bold">{{ label }}</b>
                <p v-else>{{ label }}</p>
            </div>
        </div>
        <div :class="constructBodyClass()">
            <slot></slot>
        </div>
    </div>
</template>
