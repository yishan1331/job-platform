<template>
	<div class="flex items-center justify-between">
		<p>{{ $t("settings.language") }}</p>
		<div class="w-40">
			<VaSelect v-model="model" :options="options" />
		</div>
	</div>
</template>
<script lang="ts" setup>
import { computed } from "vue";

import { useI18n } from "vue-i18n";

type LanguageMap = Record<string, string>;

const { t, locale } = useI18n();

const languages: LanguageMap = {
	english: t("language.english"),
	// spanish: t('language.spanish'),
	// brazilian_portuguese: t('language.brazilian_portuguese'),
	tradionnal_chinese: t("language.tradionnal_chinese"),
	simplified_chinese: t("language.simplified_chinese"),
	// persian: t('language.persian'),
};

const languageCodes: LanguageMap = {
	gb: languages.english,
	tw: languages.tradionnal_chinese,
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
	},
});
</script>
