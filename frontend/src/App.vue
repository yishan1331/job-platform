<template>
	<RouterView class="bg-white" />
</template>

<script setup>
import { useRouter } from "vue-router";
import { useUserAuthStore } from "@/stores/user-auth";
import i18n from "./i18n";

const router = useRouter();
const AuthStore = useUserAuthStore();

setTimeout(function () {
	if (
		sessionStorage.getItem("loginStatus") != null &&
		sessionStorage.getItem("loginStatus") != "undefined"
	) {
		const obj = {
			email: sessionStorage.getItem("loginEmail"),
			status: Boolean(sessionStorage.getItem("loginStatus")),
			username: sessionStorage.getItem("loginUsername"),
			role: sessionStorage.getItem("loginRole"),
			id: sessionStorage.getItem("loginId"),
		};
		AuthStore.setUserAuthData(obj);
		AuthStore.setUserAuthToken(sessionStorage.getItem("loginToken"));
		const language = sessionStorage.getItem("settingLanguage");
		AuthStore.setLanguage(language);
		// 設置 i18n 語言
		if (language) {
			i18n.global.locale.value = language;
		}
		sessionStorage.removeItem("loginStatus");
		sessionStorage.removeItem("loginEmail");
		sessionStorage.removeItem("loginUsername");
		sessionStorage.removeItem("loginToken");
		sessionStorage.removeItem("loginRole");
		sessionStorage.removeItem("loginId");
		sessionStorage.removeItem("settingLanguage");
	} else {
		router.push({ name: "login" });
	}
	// }
}, 0);
</script>

<style lang="scss">
@import "scss/main.scss";

#app {
	font-family: "Inter", Avenir, Helvetica, Arial, sans-serif;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
}

body {
	margin: 0;
	min-width: 20rem;
}
</style>
