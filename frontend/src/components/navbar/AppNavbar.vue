<template>
	<VaNavbar class="app-layout-navbar py-2 px-0 h-16" color="primary">
		<template #left>
			<div class="left">
				<Transition v-if="isMobile" name="icon-fade" mode="out-in">
					<VaIcon
						size="24px"
						:component="VaIconComponent"
						:icon="isSidebarMinimized ? 'menu' : 'close'"
						@click="isSidebarMinimized = !isSidebarMinimized"
					/>
				</Transition>
				<div
					class="logo"
					:class="!isMobile ? 'text-3xl' : ''"
					@click="GlobalStore.toggleSidebar()"
				>
					<VaIcon
						size="20px"
						class="pr-1"
						:component="VaIconComponent"
						:icon="'talentlabs-logo-thicker'"
					/>
				</div>
			</div>
		</template>
		<template #right>
			<div class="right">
				<AppNavbarActions
					class="app-navbar__actions"
					:is-mobile="isMobile"
				/>
			</div>
		</template>
	</VaNavbar>
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia";
import { useGlobalStore } from "@/stores/global-store";
import AppNavbarActions from "./components/AppNavbarActions.vue";
import VaIconComponent from "@/components/icons/VaIconComponent.vue";
// import VuesticLogo from '../VuesticLogo.vue'

defineProps({
	isMobile: { type: Boolean, default: false },
});

const GlobalStore = useGlobalStore();

const { isSidebarMinimized } = storeToRefs(GlobalStore);
</script>

<style lang="scss" scoped>
@import "@/scss/main.scss";
.va-navbar {
	z-index: 2;
	.logo {
		cursor: pointer;
		transition: font-size 0.2s;
	}

	@media screen and (max-width: 950px) {
		.left {
			width: 100%;
			.logo {
				font-size: 1.1rem;
			}
		}
		.app-navbar__actions {
			display: flex;
			justify-content: flex-end;
			width: 100%;
		}
	}
	@media screen and (max-width: 600px) {
		.left {
			margin-left: 0.5rem;
			.logo {
				font-size: 1rem;
			}
		}
		.right {
			margin-right: 0.5rem;
		}
		.va-navbar {
			padding-left: 0.2rem;
			padding-right: 0.2rem;
			height: 48px;
		}
	}
	@media screen and (max-width: 400px) {
		.left .logo {
			font-size: 0.9rem;
		}
	}
}

.left,
.right {
	display: flex;
	align-items: center;
}

.left {
	margin-left: 1rem;
	& > * {
		margin-right: 1rem;
	}
	& > *:last-child {
		margin-right: 0;
	}
}
.right {
	margin-right: 1rem;
}

.icon-fade-enter-active,
.icon-fade-leave-active {
	transition: transform 0.5s ease;
}

.icon-fade-enter,
.icon-fade-leave-to {
	transform: scale(0.5);
}
</style>
