<template>
	<img :src="iconPath" :alt="icon" />
</template>

<script lang="ts" setup>
import { computed } from 'vue'

const props = withDefaults(
	defineProps<{
		icon?: string
	}>(),
	{
		icon: '',
	}
)

const iconPath = computed(() => new URL(`../../assets/icons/${props.icon}.svg`, import.meta.url).href)
</script>
