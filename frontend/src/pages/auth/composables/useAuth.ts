import { Ref, ref, unref } from "vue";

import { type Filters } from "@/services/utils";
import { login, logout, authMe } from "@/APIs/auth";

const makeFiltersRef = () =>
	ref<Partial<Filters>>({ isActive: true, search: "" });

export const useAuth = (
	formData?: { email: string; password: string },
	options?: {
		filters?: Ref<Partial<Filters>>;
	}
) => {
	const isLoading = ref(false);
	let users = ref({});
	const statusCode = ref<number>(0);
	let sessions = ref({});

	const { filters = makeFiltersRef() } = options || {};

	const logIn = async () => {
		isLoading.value = true;
		const loginResult = await login(formData, {
			...unref(filters),
		});

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
		// isLoading,

		// filters,

		// statusCode,
		// response,
		// users,

		logIn,
		logOut,
		getAuthMe,
	};
};
