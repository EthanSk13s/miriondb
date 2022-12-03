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
    }
};
</script>

<template>
    <div class="mx-1 md:mx-0 flex flex-col flex-wrap">
        <div>
            <div :class="headerClass">
                <b>{{ label }}</b>
            </div>
        </div>
        <div :class="borderClass">
            <CardIcon />
            <CardIcon />
            <CardIcon />
            <CardIcon />
        </div>
    </div>
</template>
