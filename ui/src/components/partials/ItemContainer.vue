<script lang="ts">
import { stringifyExpression } from '@vue/compiler-core';

export default {
    props: {
        label: String,
        color: String,
        isTextWhite: Boolean,
        bold: Boolean
    },
    methods: {
        constructHeaderClass() {
            let className: string = '';
            let textColor = 'text-black';

            if (this.isTextWhite) {
                textColor = 'text-white'
            }

            if (this.color === "yellow") {
                className = `mx-1 rounded-t p-1 ${textColor} bg-yellow-300`
            } else if (this.color === "sky") {
                className = `mx-1 rounded-t p-1 ${textColor} bg-sky-500`
            } else if (this.color === "gray") {
                className = `mx-1 rounded-t p-1 ${textColor} bg-gray-700`
            }

            return className;
        },
        constructBodyClass() {
            let className: string = '';

            if (this.color === "yellow") {
                className = "mx-1 bg-slate-800 p-1 flex flex-col text-white lg:flex-row gap-2 flex-wrap border rounded-b border-yellow-300"
            } else if (this.color === "sky") {
                className = "mx-1 bg-slate-800 p-1 flex flex-col text-white lg:flex-row gap-2 flex-wrap border rounded-b border-sky-500"
            } else if (this.color === "gray") {
                className = "mx-1 bg-slate-800 p-1 flex flex-col text-white lg:flex-row gap-2 flex-wrap border rounded-b border-gray-700"
            }

            return className;
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
