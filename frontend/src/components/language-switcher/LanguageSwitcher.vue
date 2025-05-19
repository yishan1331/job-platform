<template>
	<div class="flex items-center justify-between">
		<div class="w-36">
			<VaSelect v-model="model" :options="options" />
		</div>
	</div>
</template>
<script lang="ts" setup>
import { computed } from "vue";

import { useI18n } from "vue-i18n";
import { useUserAuthStore } from "@/stores/user-auth";

type LanguageMap = Record<string, string>;

const { locale } = useI18n();
const AuthStore = useUserAuthStore();

const languages: LanguageMap = {
	english: "English",
	traditional_chinese: "繁體中文",
};

const languageCodes: LanguageMap = {
	gb: languages.english,
	tw: languages.traditional_chinese,
};

const languageName: LanguageMap = Object.fromEntries(
	Object.entries(languageCodes).map(([key, value]) => [value, key])
);

const options = Object.values(languageCodes);

const model = computed({
	get() {
		return languageCodes[locale.value];
	},
	set(value) {
		locale.value = languageName[value];
		AuthStore.setLanguage(locale.value);
	},
});
</script>
