<script lang="ts">
export default {
    props: {
        disabled: Boolean,
        direction: {
            type: String,
            validator(value: string) {
                return ['left', 'right'].includes(value)
            }
        }
    },
    methods: {
        addClass() {
            let className = '';
            if (this.disabled) {
                className = "text-white rounded-full border-2 border-blue-900 bg-slate-800 p-1 opacity-50";
            } else {
                className = "text-white rounded-full border-2 border-blue-900 bg-slate-800 p-1";
            }

            return className;
        },
        click() {
            this.$emit('click');
        }
    },
    emits: ['click']
}
</script>

<template>
    <button :class="addClass()" :disabled="disabled" @click="click()">
        <svg v-if="direction === 'left'" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
            stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 12h-15m0 0l6.75 6.75M4.5 12l6.75-6.75" />
        </svg>
        <svg v-else-if="direction === 'right'" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
            stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12h15m0 0l-6.75-6.75M19.5 12l-6.75 6.75" />
        </svg>
    </button>
</template>