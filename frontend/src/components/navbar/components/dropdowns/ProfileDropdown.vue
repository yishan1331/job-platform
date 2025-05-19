<template>
	<div class="profile-dropdown-wrapper">
		<VaDropdown :offset="[9, 0]" class="profile-dropdown" stick-to-edges>
			<template #anchor>
				<VaButton preset="secondary" color="textPrimary">
					<span class="profile-dropdown__anchor min-w-max">
						<slot />
						<VaAvatar :size="32" color="#FFFFFFFF"> 👤 </VaAvatar>
					</span>
				</VaButton>
			</template>
			<VaDropdownContent
				class="profile-dropdown__content md:w-60 px-0 py-4 w-full"
				:style="{ '--hover-color': hoverColor }"
			>
				<VaList v-for="group in options" :key="group.name">
					<header
						v-if="group.name"
						class="uppercase text-[var(--va-secondary)] opacity-80 font-bold text-xs px-4"
					>
						{{ $t(`navbar.${group.name}`) }}
					</header>
					<VaListItem
						v-for="item in group.list"
						:key="item.name"
						class="menu-item px-4 text-base cursor-pointer h-8"
						@click="resolveLinkAttribute(item)"
					>
						<VaIcon
							size="20px"
							class="pr-1"
							:component="VaIconComponent"
							:icon="'logout_white'"
						/>
						{{ $t(`navbar.${item.name}`) }}
					</VaListItem>
					<VaListSeparator v-if="group.separator" class="mx-3 my-2" />
				</VaList>
			</VaDropdownContent>
		</VaDropdown>
	</div>
</template>

<script lang="ts" setup>
import { ref, computed } from "vue";
import { useColors } from "vuestic-ui";
import { storeToRefs } from "pinia";

import { useAuth } from "@/pages/auth/composables/useAuth";
import { useUserAuthStore } from "@/stores/user-auth";
import VaIconComponent from "@/components/icons/VaIconComponent.vue";
import VaIconLogout from "@/components/icons/VaIconLogout.vue";

const AuthStore = useUserAuthStore();
const { userAuthData } = storeToRefs(AuthStore);

const { colors, setHSLAColor } = useColors();
const hoverColor = computed(() => setHSLAColor(colors.focus, { a: 0.1 }));

type ProfileListItem = {
	name: string;
	to?: string;
	href?: string;
	icon: string;
};

type ProfileOptions = {
	name: string;
	separator: boolean;
	list: ProfileListItem[];
};

withDefaults(
	defineProps<{
		options?: ProfileOptions[];
	}>(),
	{
		options: () => [
			{
				name: "account",
				separator: true,
				list: [
					{
						name: "users",
						to: "users",
						icon: "group",
					},
					{
						name: "profile",
						to: "preferences",
						icon: "mso-account_circle",
					},
					{
						name: "settings",
						to: "settings",
						icon: "mso-settings",
					},
					{
						name: "billing",
						to: "billing",
						icon: "mso-receipt_long",
					},
					{
						name: "projects",
						to: "projects",
						icon: "mso-favorite",
					},
				],
			},
			{
				name: "explore",
				separator: true,
				list: [
					{
						name: "faq",
						to: "faq",
						icon: "mso-quiz",
					},
					{
						name: "helpAndSupport",
						href: "https://discord.gg/u7fQdqQt8c",
						icon: "mso-error",
					},
				],
			},
			{
				name: "",
				separator: false,
				list: [
					{
						name: "logout",
						to: "login",
						icon: "mso-logout",
					},
				],
			},
		],
	}
);

const isShown = ref(false);

const resolveLinkAttribute = (item: ProfileListItem) => {
	if (item.name === "logout") {
		useAuth({
			userID: userAuthData.value.account,
			userNo: userAuthData.value.userno,
		}).logOut();
		return;
	}
	return item.to
		? { to: { name: item.to } }
		: item.href
		  ? { href: item.href, target: "_blank" }
		  : {};
};
</script>

<style lang="scss">
.profile-dropdown {
	cursor: pointer;

	&__content {
		.menu-item:hover {
			background: var(--hover-color);
		}
	}

	&__anchor {
		display: inline-block;
	}
}
</style>
