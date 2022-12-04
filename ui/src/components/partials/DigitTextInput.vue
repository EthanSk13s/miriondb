<script lang="ts">
export default {
    props: {
        inputValue: Number,
        min: Number,
        max: Number
    },
    emits: ['update:inputValue'],
    methods: {
        handleDigitInput(event: KeyboardEvent) {
            if (!event.key.match(/^[0-9]+$/) && event.key !== "Backspace"
                && event.key !== "Enter"
                && event.key !== "ArrowLeft" && event.key !== "ArrowRight") {
                event.preventDefault()
            }
        },
        emitInput(event: Event) {
            let element = event.target as HTMLInputElement;
            let value = Number(element.value);
            let newValue: number | null = null;

            if (value < this.min!) {
                newValue = this.min!
            } else if (value > this.max!) {
                newValue = this.max!
            }

            if (newValue) {
                value = newValue;
            }

            this.$emit('update:inputValue', value);
        }
    },
    mounted() {
        let decrease = this.$refs.decrease as HTMLElement;
        let digitInput = this.$refs.digitInput as HTMLInputElement;
        let increase = this.$refs.increase as HTMLElement;

        decrease.addEventListener('click', () => {
            let currentDigit = Number(digitInput.value);
            if (currentDigit > this.min!) {
                digitInput.value = String(currentDigit - 1);
            }

            this.$emit('update:inputValue', Number(digitInput.value))
        })

        increase.addEventListener('click', () => {
            let currentDigit = Number(digitInput.value);
            if (currentDigit < this.max!) {
                digitInput.value = String(currentDigit + 1);
            }

            this.$emit('update:inputValue', Number(digitInput.value))
        })

        digitInput.addEventListener('keydown', this.handleDigitInput);
    }
}
</script>

<template>
    <button ref="decrease" class="m-1 rounded bg-yellow-500 hover:bg-yellow-600 px-2 text-white transition-colors duration-200">-</button>
    <input ref="digitInput" @input="emitInput"
        class="w-1/6 md:w-1/12 rounded bg-gray-700 px-0.5 text-center text-white focus:outline-none focus:ring focus:ring-violet-300"
        type="text" maxlength="2" :value="inputValue" />
    <button ref="increase" class="m-1 rounded bg-yellow-500 hover:bg-yellow-600 px-2 text-white transition-colors duration-200">+</button>
</template>