import { Ref, ref, unref } from "vue";

import { type Filters } from "@/services/utils";
import { login, logout, authMe } from "@/APIs/auth";

export const useAuth = (formData?: { email: string; password: string }) => {
	const isLoading = ref(false);
	let users = ref({});
	const statusCode = ref<number>(0);
	let sessions = ref({});

	const logIn = async () => {
		isLoading.value = true;
		const loginResult = await login(formData);

		if (loginResult) {
			const { statusCode: newStatusCode, response } = loginResult;
			statusCode.value = newStatusCode;
			sessions.value = {
				access: response.items?.access,
				loginTime: new Date(),
			};
		}

		isLoading.value = false;

		return {
			statusCode,
			response: loginResult?.response,
			users,
			sessions,
		};
	};

	const getAuthMe = async () => {
		const authMeResult = await authMe();
		return authMeResult;
	};

	const logOut = async () => {
		await logout();
	};

	return {
		logIn,
		logOut,
		getAuthMe,
	};
};
