<template>
	<VaCollapse :value="isExpanded" @toggle="toggle">
		<template #header="{ value: isCollapsed }">
			<VaSidebarItem
				:to="
					navigationRoute.children
						? undefined
						: { name: navigationRoute.name }
				"
				:active="routeHasActiveChild(nowRoute, navigationRoute)"
				:active-color="activeColor"
				:text-color="textColor(navigationRoute)"
				:aria-label="`${
					navigationRoute.children ? 'Open category ' : 'Visit'
				} ${$t(navigationRoute.displayName)}`"
				role="button"
				hover-opacity="0.10"
			>
				<VaSidebarItemContent class="py-3 pr-2 pl-4 item-content">
					<VaIcon
						v-if="
							'meta' in navigationRoute &&
							navigationRoute.meta.icon
						"
						aria-hidden="true"
						size="20px"
						:color="iconColor(navigationRoute)"
						:component="VaIconComponent"
						:icon="navigationRoute.meta.icon"
					/>
					<VaSidebarItemTitle
						class="flex justify-between items-center leading-5 font-semibold"
					>
						{{ $t(navigationRoute.displayName) }}
						<VaIcon
							v-if="navigationRoute.children"
							:name="
								arrowDirection(
									isCollapsed,
									navigationRoute.displayName
								)
							"
							size="20px"
						/>
					</VaSidebarItemTitle>
				</VaSidebarItemContent>
			</VaSidebarItem>
		</template>
		<template #body>
			<VaAccordion
				v-if="navigationRoute.children"
				v-model="itemsRoutingMenuStatus"
				multiple
			>
				<AppSidebarItems
					v-for="(childRoute, index) in navigationRoute.children"
					:key="index"
					:navigationRoute="childRoute"
					class="pl-11 is-children"
				/>
			</VaAccordion>
		</template>
	</VaCollapse>
</template>

<script lang="ts">
import { defineComponent, ref, computed, watch } from "vue";
import { useColors } from "vuestic-ui";
import { useRoute } from "vue-router";
import { storeToRefs } from "pinia";

import VaIconComponent from "@/components/icons/VaIconComponent.vue";
import { useGlobalStore } from "@/stores/global-store";

import { routeHasActiveChild, type INavigationRoute } from "./NavigationRoutes";

export default defineComponent({
	name: "AppSidebarItems",
	components: {
		VaIconComponent,
	},
	props: {
		navigationRoute: { type: Object, required: true },
		mobile: { type: Boolean, default: false },
	},
	emits: ["update:visible"],
	setup(props) {
		const { getColor, colorToRgba } = useColors();

		const GlobalStore = useGlobalStore();
		const { isSidebarMinimized } = storeToRefs(GlobalStore);

		const isExpanded = ref(false);
		const nowRoute = useRoute();

		const itemsRoutingMenuStatus = ref<boolean[]>([]);

		const toggle = () => {
			isExpanded.value = !isExpanded.value;
		};

		const arrowDirection = (state: boolean) =>
			state ? "va-arrow-up" : "va-arrow-down";

		const iconColor = (route: any) =>
			routeHasActiveChild(nowRoute, route) ? "primary" : "secondary";

		const textColor = (route: any) =>
			routeHasActiveChild(nowRoute, route) ? "#000" : "textPrimary";

		const activeColor = computed(() =>
			colorToRgba(getColor("primary"), 0.1)
		);

		const setActiveExpand = () => {
			if ("children" in props.navigationRoute) {
				itemsRoutingMenuStatus.value =
					props.navigationRoute.children.map(
						(route: INavigationRoute) =>
							routeHasActiveChild(nowRoute, route)
					);
			}
		};

		const isMobile = computed(() => props.mobile);

		const sidebarAction = () => {
			if (isMobile.value) {
				GlobalStore.toggleSidebar();
				return;
			}
			if (
				isSidebarMinimized.value &&
				[...new Set(itemsRoutingMenuStatus.value)].length == 1 &&
				![...new Set(itemsRoutingMenuStatus.value)][0]
			) {
				GlobalStore.toggleSidebar();
			}
		};

		watch(() => nowRoute.fullPath, setActiveExpand, { immediate: true });
		// watch(() => itemsRoutingMenuStatus.value, sidebarAction, {
		// 	immediate: true,
		// 	deep: true,
		// })

		return {
			itemsRoutingMenuStatus,
			isExpanded,
			toggle,
			arrowDirection,
			nowRoute,
			routeHasActiveChild,
			activeColor,
			iconColor,
			textColor,
			VaIconComponent,
		};
	},
});
</script>

<style lang="scss" scoped>
// .is-children{
// 	padding-left: 2.75rem !important;
// }
</style>
