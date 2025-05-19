<template>
	<div class="app-navbar-actions">
		<LanguageSwitcher />

		<VaButton preset="secondary" color="#fff" @click="goLogout()">
			<span class="profile-dropdown__anchor min-w-max">
				<slot />
				<VaIcon
					size="20px"
					class="pr-1"
					:component="VaIconComponent"
					:icon="'logout_white'"
				/>
			</span>
			{{ $t(`navbar.logout`) }}
		</VaButton>
	</div>
</template>

<script lang="ts" setup>
// import NotificationDropdown from './dropdowns/NotificationDropdown.vue'
// import ProfileDropdown from './dropdowns/ProfileDropdown.vue'
import VaIconComponent from "@/components/icons/VaIconComponent.vue";
import LanguageSwitcher from "@/components/language-switcher/LanguageSwitcher.vue";

import { useAuth } from "@/pages/auth/composables/useAuth";
import { useUserAuthStore } from "@/stores/user-auth";
import { storeToRefs } from "pinia";

const AuthStore = useUserAuthStore();
const { userAuthData } = storeToRefs(AuthStore);

defineProps({
	isMobile: { type: Boolean, default: false },
});

const goLogout = () => {
	useAuth({
		userID: userAuthData.value.account,
		userNo: userAuthData.value.userno,
	}).logOut();
};
</script>

<style lang="scss">
.app-navbar-actions {
	display: flex;
	align-items: center;

	.va-dropdown__anchor {
		color: var(--va-primary);
		fill: var(--va-primary);
	}

	&__item {
		padding: 0;
		margin-left: 0.25rem;
		margin-right: 0.25rem;

		svg {
			height: 20px;
		}

		&--profile {
			display: flex;
			justify-content: center;
		}

		.va-dropdown-content {
			background-color: var(--va-white);
		}

		@media screen and (max-width: 640px) {
			margin-left: 0;
			margin-right: 0;

			&:first-of-type {
				margin-left: 0;
			}
		}
	}

	.fa-github {
		color: var(--va-on-background-primary);
	}
}
</style>
