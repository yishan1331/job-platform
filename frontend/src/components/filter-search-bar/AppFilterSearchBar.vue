<template>
	<div class="w-full">
		<button class="collapsible" @click="showCollapseBox">
			{{ $t("search.searchModule") }}
			<VaIcon
				v-if="isCollapsed"
				aria-hidden="true"
				size="20px"
				:component="VaIconComponent"
				icon="keyboard_arrow_down"
			/>
			<VaIcon
				v-else
				aria-hidden="true"
				size="20px"
				:component="VaIconComponent"
				icon="keyboard_arrow_up"
			/>
		</button>
		<div
			ref="collapsiblecontent"
			class="w-full flex xs:flex-col sm:flex-row gap-2 overflow-auto justify-start collapsible-content"
			:style="{ height: isCollapsed ? '0px' : 'auto' }"
		>
			<VaSelect
				v-model="tempFilters.category"
				class="mb-4 sm:w-[25%]"
				:options="categoryConfig.options"
				:label="$t('select.categories')"
				value-by="value"
				:placeholder="$t('select.categories')"
				color="primary"
				multiple
				max-selections="2"
			/>
			<!-- @update:modelValue="clearDatas" -->
			<div
				class="flex gap-5 xs:flex-wrap sm:flex-nowrap"
				v-if="tempFilters.category && (tempCategory1 || tempCategory2)"
			>
				<VaSelect
					v-if="
						tempCategory1 in searchConfig &&
						categoryConfig.types[tempCategory1] == 'select'
					"
					v-model="tempSearch1"
					:label="categoryConfig.label[tempCategory1]"
					class="mb-4"
					:options="searchConfig[tempCategory1]"
					value-by="value"
					:placeholder="$t('select.category')"
					color="primary"
				/>
				<VaSelect
					v-if="
						tempCategory2 in searchConfig &&
						categoryConfig.types[tempCategory2] == 'select'
					"
					v-model="tempSearch2"
					:label="categoryConfig.label[tempCategory2]"
					class="mb-4"
					:options="searchConfig[tempCategory2]"
					value-by="value"
					:placeholder="$t('select.category')"
					color="primary"
				/>
				<VaInput
					v-if="categoryConfig.types[tempCategory1] == 'text'"
					v-model="tempSearch1"
					:label="categoryConfig.label[tempCategory1]"
					color="primary"
				>
					<template #prependInner>
						<VaIcon name="search" color="secondary" size="small" />
					</template>
				</VaInput>
				<VaInput
					v-if="categoryConfig.types[tempCategory2] == 'text'"
					v-model="tempSearch2"
					:label="categoryConfig.label[tempCategory2]"
					color="primary"
				>
					<template #prependInner>
						<VaIcon name="search" color="secondary" size="small" />
					</template>
				</VaInput>
				<div
					v-if="categoryConfig.types[tempCategory1] == 'date'"
					class="w-4/5"
				>
					<p
						class="va-text-primary"
						style="
							font-size: 1rem;
							font-weight: 700;
							line-height: 14px;
							margin-bottom: 4px;
						"
					>
						{{ categoryConfig.label[tempCategory1] }}
					</p>
					<VaDatePicker
						v-model="tempSearch1"
						highlight-weekend
						color="primary"
						mode="range"
					/>
					<div>
						{{ tempSearch1DateDisplay }}
					</div>
				</div>
				<div
					v-if="categoryConfig.types[tempCategory2] == 'date'"
					class="w-4/5"
				>
					<p
						class="va-text-primary"
						style="
							font-size: 1rem;
							font-weight: 700;
							line-height: 14px;
							margin-bottom: 4px;
						"
					>
						{{ categoryConfig.label[tempCategory2] }}
					</p>
					<VaDatePicker
						v-model="tempSearch2"
						highlight-weekend
						color="primary"
						mode="range"
					/>
					<div>
						{{ tempSearch2DateDisplay }}
					</div>
				</div>
			</div>
			<div class="flex">
				<div
					class="items-center"
					:class="
						categoryConfig.types[tempCategory1] == 'date' ||
						categoryConfig.types[tempCategory2] == 'date'
							? ''
							: 'flex'
					"
				>
					<VaButton
						@click.prevent="searchDatas"
						color="primary"
						icon="mso-search"
						preset="secondary"
					/>
				</div>
				<div
					class="items-center"
					:class="
						categoryConfig.types[tempCategory1] == 'date' ||
						categoryConfig.types[tempCategory2] == 'date'
							? ''
							: 'flex'
					"
				>
					<VaButton
						@click.prevent="clearDatas"
						color="danger"
						icon="close"
						preset="secondary"
					/>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { PropType, toRef, ref, watch, computed, Ref, nextTick } from "vue";
import { cloneDeep, isNull } from "lodash";

import { type Filters } from "@/services/utils";
import VaIconComponent from "@/components/icons/VaIconComponent.vue";

const props = defineProps({
	filters: { type: Object as PropType<Partial<Filters>>, required: true },
	categoryConfig: { type: Object, required: true },
	searchConfig: {
		type: Object,
		default: () => ({}),
	},
	showFuzzy: { type: Boolean, required: false, default: true },
	initSearching: { type: Boolean, required: false, default: false },
});

const isCollapsed = ref(true);
const collapsiblecontent: Ref<null | HTMLElement> = ref(null);
const showCollapseBox = () => {
	isCollapsed.value = !isCollapsed.value;
};

const filters = toRef(props, "filters");
const categoryConfig = toRef(props, "categoryConfig");
const searchConfig = toRef(props, "searchConfig");
const showFuzzy = toRef(props, "showFuzzy");
const initSearching = toRef(props, "initSearching");
const tempFilters = ref<Partial<Filters>>(
	!initSearching.value ? cloneDeep(filters.value) : {}
);
const tempCategory1 = ref("");
const tempCategory2 = ref("");
const tempSearch1 = ref("");
const tempSearch2 = ref("");

const tempSearch1DateDisplay = computed(() => {
	if (!tempSearch1.value) return "";
	const startdate = tempSearch1.value.start
		? new Date(tempSearch1.value.start)
		: "";
	const enddate = tempSearch1.value.end
		? new Date(tempSearch1.value.end)
		: "";

	if (startdate && enddate)
		return `區間：${getFullDate(startdate)} 00:00:00 ~ ${getFullDate(
			enddate
		)} 23:59:59`;
	if (startdate) return `區間：${getFullDate(startdate)}`;
	if (enddate) return `區間：${getFullDate(enddate)}`;
});
const tempSearch2DateDisplay = computed(() => {
	if (!tempSearch2.value) return "";
	const startdate = tempSearch2.value.start
		? new Date(tempSearch2.value.start)
		: "";
	const enddate = tempSearch2.value.end
		? new Date(tempSearch2.value.end)
		: "";

	if (startdate && enddate)
		return `區間：${getFullDate(startdate)} 00:00:00 ~ ${getFullDate(
			enddate
		)} 23:59:59`;
	if (startdate) return `區間：${getFullDate(startdate)}`;
	if (enddate) return `區間：${getFullDate(enddate)}`;
});

const getFullDate = (date: Date) => {
	// 獲取年份、月份和日期
	const year = date.getFullYear();
	const month = String(date.getMonth() + 1).padStart(2, "0"); // 月份從 0 開始，所以需要加 1
	const day = String(date.getDate()).padStart(2, "0");

	return `${year}-${month}-${day}`;
};

watch(
	() => tempFilters.value.category,
	(newCategory, oldCategory) => {
		if (newCategory) {
			if (newCategory.length > 1) {
				tempCategory1.value = newCategory[0];
				tempCategory2.value = newCategory[1];
			} else {
				tempCategory1.value = newCategory[0];
				tempCategory2.value = "";
			}
		}
		if (newCategory !== oldCategory) {
			tempFilters.value.search = "";
			tempFilters.value.fuzzy = false;
			tempSearch1.value = "";
			tempSearch2.value = "";
			filters.value.search = "";
		}
	},
	{ deep: true }
);

const searchDatas = () => {
	filters.value.search = "";
	filters.value.category = [tempCategory1.value, tempCategory2.value];
	if (typeof tempSearch1.value === "object") {
		if (isNull(tempSearch1.value.start) && isNull(tempSearch1.value.end)) {
			filters.value.search = "";
			filters.value.category = [tempCategory2.value];
		} else {
			filters.value.search = `${tempSearch1.value.start}^_^${tempSearch1.value.end}`;
		}
	} else if (tempSearch1.value) {
		filters.value.search = tempSearch1.value;
	} else {
		filters.value.category = [tempCategory2.value];
	}
	if (typeof tempSearch2.value === "object") {
		if (isNull(tempSearch2.value.start) && isNull(tempSearch2.value.end)) {
			if (filters.value.search) {
				filters.value.category = [tempCategory1.value];
			} else {
				filters.value.category = [];
			}
		} else {
			if (filters.value.search) {
				filters.value.search = `${filters.value.search}||${tempSearch2.value.start}^_^${tempSearch2.value.end}`;
			} else {
				filters.value.search = `${tempSearch2.value.start}^_^${tempSearch2.value.end}`;
			}
		}
	} else if (tempSearch2.value) {
		if (filters.value.search) {
			filters.value.search = `${filters.value.search}||${tempSearch2.value}`;
		} else {
			filters.value.search = tempSearch2.value;
		}
	} else {
		if (tempSearch1.value) filters.value.category = [tempCategory1.value];
	}
	if (!filters.value.search) {
		filters.value.category = [];
	}
	filters.value.fuzzy = tempFilters.value.fuzzy;
};

const clearDatas = () => {
	tempCategory1.value = "";
	tempCategory2.value = "";
	tempSearch1.value = "";
	tempSearch2.value = "";
	filters.value.category = [];
	filters.value.search = "";
	filters.value.fuzzy = false;
	tempFilters.value.category = [];
	tempFilters.value.search = "";
	tempFilters.value.fuzzy = false;
};
</script>

<style lang="scss" scoped>
.collapsible {
	margin-bottom: 10px;
	width: 100%;
	border: none;
	text-align: left;
	outline: none;
	font-size: 15px;
	display: flex;
	align-items: center;
}

.collapsible-content {
	// overflow: hidden;
}
</style>
