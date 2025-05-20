import { storeToRefs } from "pinia";
import router from "@/router";

import { type APIsResponse } from "@/services/utils";
import { axiosAPI } from "@/services/axios-api";
import { useUserAuthStore } from "@/stores/user-auth";

const AuthStore = useUserAuthStore();
const { addedRouteToRemove } = storeToRefs(AuthStore);

export const login = async (formData: { email: string; password: string }) => {
	const apiResult = (await axiosAPI({
		method: "post",
		url: "token/pair",
		params: {
			email: formData.email,
			password: formData.password,
		},
	})) as APIsResponse;
	return apiResult;
};

export const authMe = async () => {
	const apiResult = (await axiosAPI({
		method: "get",
		url: "auth/me",
	})) as APIsResponse;
	return apiResult;
};

export const logout = async () => {
	AuthStore.resetUserAuthData();
	addedRouteToRemove.value;
	router.push({ name: "login" });
};
