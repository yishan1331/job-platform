<template>
	<div
		class="flex flex-col-reverse md:flex-row gap-2 justify-between items-center py-2"
	>
		<div>
			<b>{{
				locale == "tw"
					? `總共${$props.pagination.total}筆資料`
					: `${$props.pagination.total} result.`
			}}</b>
		</div>

		<div>
			{{ $t("table.perPage") }}
			<VaSelect
				v-model="$props.pagination.perPage"
				class="!w-20"
				:options="[10, 50, 100]"
				color="primary"
			/>
		</div>

		<div class="flex">
			<VaButton
				preset="secondary"
				icon="va-arrow-left"
				color="primary"
				aria-label="Previous page"
				:disabled="$props.pagination.page === 1"
				@click="$props.pagination.page--"
			/>
			<VaPagination
				v-model="$props.pagination.page"
				buttons-preset="secondary"
				:pages="totalPages"
				:visible-pages="5"
				:boundary-links="false"
				:direction-links="false"
				active-page-color="primary"
				color="primary"
			/>
			<VaButton
				class="mr-2"
				preset="secondary"
				color="primary"
				icon="va-arrow-right"
				aria-label="Next page"
				:disabled="$props.pagination.page === totalPages"
				@click="$props.pagination.page++"
			/>
		</div>
	</div>
</template>

<script setup lang="ts">
import { PropType, computed } from "vue";
import { useI18n } from "vue-i18n";

import { type Pagination } from "@/services/utils";

const { locale } = useI18n();

const props = defineProps({
	pagination: { type: Object as PropType<Pagination>, required: true },
});

const totalPages = computed(() =>
	Math.ceil(props.pagination.total / props.pagination.perPage)
);
</script>

<style lang="scss" scoped></style>
