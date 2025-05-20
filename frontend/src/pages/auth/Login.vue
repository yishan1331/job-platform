<template>
	<VaForm
		ref="form"
		@submit.prevent="submit"
		@keyup.enter="submit"
		class="login-form"
	>
		<h1
			class="font-semibold mb-4"
			:class="breakpoint.lgUp ? 'text-4xl' : 'text-3xl'"
		>
			Log in
		</h1>
		<VaInput
			v-model="formData.email"
			:rules="[validators.required, validators.email]"
			class="mb-4"
			:label="$t('auth.email')"
			type="text"
			preset="solid"
			color="primary"
		/>
		<VaValue v-slot="isPasswordVisible" :default-value="false">
			<VaInput
				v-model.trim="formData.password"
				:rules="[
					validators.required,
					validators.passwordLength,
					validators.passwordFormat,
				]"
				:type="isPasswordVisible.value ? 'text' : 'password'"
				class="mb-4"
				:label="$t('auth.password')"
				@clickAppendInner.stop="
					isPasswordVisible.value = !isPasswordVisible.value
				"
				maxlength="16"
				preset="solid"
				color="primary"
			>
				<template #appendInner>
					<VaIcon
						:name="
							isPasswordVisible.value
								? 'mso-visibility_off'
								: 'mso-visibility'
						"
						class="cursor-pointer"
						color="secondary"
					/>
				</template>
			</VaInput>
		</VaValue>

		<div class="flex justify-center my-4">
			<VaButton class="w-full" @click="submit" color="primary">
				{{ $t("auth.login") }}
			</VaButton>
		</div>
		<div class="mt-6 text-center" style="color: #6b7280">
			<b>Ver {{ version }}</b>
		</div>
	</VaForm>
</template>

<script lang="ts" setup>
import { reactive } from "vue";
import { useRouter, RouteRecordRaw } from "vue-router";
import { useForm, useToast, useBreakpoint } from "vuestic-ui";
import { storeToRefs } from "pinia";
import { cloneDeep } from "lodash";
import { useI18n } from "vue-i18n";

import { validators } from "../../services/utils";
import { useAuth } from "@/pages/auth/composables/useAuth";
import { useUserAuthStore } from "@/stores/user-auth";
import { useGlobalStore } from "@/stores/global-store";

const breakpoint = useBreakpoint();

const AuthStore = useUserAuthStore();
const { version } = storeToRefs(useGlobalStore());

const { t } = useI18n();
const { validate } = useForm("form");
const router = useRouter();
const { init: notify } = useToast();

const formData = reactive({
	email: "",
	password: "",
});

const submit = async () => {
	if (validate()) {
		const _tempFormData = cloneDeep(formData);
		const { logIn, getAuthMe } = useAuth(_tempFormData);
		const { statusCode, response, sessions } = await logIn();
		const _sessions = sessions.value;

		if (statusCode.value != 200) {
			notify({
				message: t("auth.login_failed"),
				color: "danger",
				duration: 2000,
			});
			return;
		}
		notify({
			message: t("auth.login_success"),
			color: "success",
			duration: 2000,
		});

		AuthStore.setUserAuthToken(_sessions.access);

		const _authMe = await getAuthMe();
		if (_authMe.statusCode != 200) {
			return;
		}

		const obj = {
			email: _authMe.response.items.email,
			status: true,
			role: _authMe.response.items.role,
			username: _authMe.response.items.username,
			id: _authMe.response.items.id,
		};
		AuthStore.setUserAuthData(obj);
		setTimeout(function () {
			router.push({ name: "index" });
		}, 900);
	}
};
</script>

<style scoped lang="scss"></style>
