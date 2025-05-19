<template>
	<VaLayout
		:top="{ fixed: true, order: 2 }"
		:left="{
			fixed: true,
			absolute: breakpoints.mdDown,
			order: 1,
			overlay: breakpoints.mdDown && !isSidebarMinimized,
		}"
		@leftOverlayClick="isSidebarMinimized = !isSidebarMinimized"
		class="bg-white"
	>
		<template #top>
			<AppNavbar :is-mobile="isMobile" />
		</template>

		<template #left>
			<AppSidebar
				:minimized="isSidebarMinimized"
				:animated="!isMobile"
				:mobile="isMobile"
				:tablet="isTablet"
				:userAuthData="userAuthData"
			/>
		</template>

		<template #content>
			<div
				:class="{ minimized: isSidebarMinimized }"
				class="app-layout__sidebar-wrapper bg-white"
			>
				<div v-if="isFullScreenSidebar" class="flex justify-end">
					<VaButton
						class="px-4 py-4"
						icon="md_close"
						preset="plain"
						@click="onCloseSidebarButtonClick"
					/>
				</div>
			</div>
			<main
				class="pt-0 p-4 mx-auto"
				style="height: calc(100vh - 4rem); max-width: 1200px"
			>
				<AppLayoutNavigation
					v-if="!isMobile && router.currentRoute.value.path != '/'"
					class="p-4"
				/>
				<article>
					<RouterView class="p-4" :is-mobile="isMobile" />
				</article>
			</main>
		</template>
	</VaLayout>
</template>

<script setup>
import { useRouter } from "vue-router";
import { onBeforeUnmount, onMounted, ref, computed } from "vue";
import { storeToRefs } from "pinia";
import { onBeforeRouteUpdate } from "vue-router";
import { useBreakpoint } from "vuestic-ui";

import { useGlobalStore } from "../stores/global-store";
import { useUserAuthStore } from "@/stores/user-auth";

import AppLayoutNavigation from "../components/app-layout-navigation/AppLayoutNavigation.vue";
import AppNavbar from "../components/navbar/AppNavbar.vue";
import AppSidebar from "../components/sidebar/AppSidebar.vue";
import { useAuth } from "@/pages/auth/composables/useAuth";

const router = useRouter();
const AuthStore = useUserAuthStore();

const GlobalStore = useGlobalStore();

const breakpoints = useBreakpoint();

const sidebarWidth = ref("16rem");
const sidebarMinimizedWidth = ref(undefined);

const isMobile = ref(false);
const isTablet = ref(false);
const { isSidebarMinimized, dataTableHeight } = storeToRefs(GlobalStore);

const { userAuthData, settingLanguage } = storeToRefs(AuthStore);

const onResize = () => {
	GlobalStore.toggleSidebar(breakpoints.mdDown);
	// isSidebarMinimized.value = breakpoints.mdDown
	isMobile.value = breakpoints.smDown;
	isTablet.value = breakpoints.mdDown;
	sidebarMinimizedWidth.value = isMobile.value ? "0" : "4.5rem";
	sidebarWidth.value = isTablet.value ? "100%" : "16rem";
	if (isMobile.value || isTablet.value) {
		GlobalStore.toggleSidebar(true);
	}
	dataTableHeight.value = breakpoints.height / 2;
};

onMounted(() => {
	window.addEventListener("resize", onResize);
	onResize();
});

onBeforeUnmount(() => {
	window.removeEventListener("resize", onResize);
});

onBeforeRouteUpdate(() => {
	if (breakpoints.mdDown) {
		// Collapse sidebar after route change for Mobile
		isSidebarMinimized.value = true;
	}
});

const isFullScreenSidebar = computed(
	() => isTablet.value && !isSidebarMinimized.value
);

const onCloseSidebarButtonClick = () => {
	isSidebarMinimized.value = true;
};

//在頁面重新整理時將vuex裡的資訊儲存到localStorage裡
window.addEventListener("beforeunload", () => {
	if (userAuthData.value.status === true) {
		sessionStorage.setItem("loginEmail", userAuthData.value.email);
		sessionStorage.setItem(
			"loginStatus",
			Boolean(userAuthData.value.status)
		);
		sessionStorage.setItem("loginUsername", userAuthData.value.username);
		sessionStorage.setItem("loginToken", userAuthData.value.token);
		sessionStorage.setItem("loginRole", userAuthData.value.role);
		sessionStorage.setItem("loginId", userAuthData.value.id);
		sessionStorage.setItem("settingLanguage", settingLanguage.value);
	} else {
		if (router.currentRoute.value.path != "/auth/login") {
			useAuth().logOut();
		}
	}
});
</script>

<style lang="scss" scope>
// Prevent icon jump on animation
.va-sidebar {
	width: unset !important;
	min-width: unset !important;
}
</style>
