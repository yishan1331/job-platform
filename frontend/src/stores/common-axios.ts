import { defineStore } from "pinia";
import axios from "axios";
import { storeToRefs } from "pinia";

import { useUserAuthStore } from "@/stores/user-auth";

const AuthStore = useUserAuthStore();
const { userAuthData } = storeToRefs(AuthStore);

export type AxiosResult = {
	data: any;
	status: number;
};

const BASE_URL = "http://127.0.0.1:8000/api/v1";

// state 和 getters 直接解構會失去響應性，需要從 storeToRefs(store) 解構
// const { isTesting } = storeToRefs(xxxStore())

// action 可以直接從原 store 解構，從 storeToRefs(store) 解構反而會失去響應性
// const store = xxxStore()
// const axiosResult = computed(() => store.axiosResult)

export const useCommonAxiosStore = defineStore("commonAxios", {
	state: () => {
		return {
			axios_result: {} as AxiosResult,
		};
	},

	getters: {
		axiosResult: (state) => state.axios_result,
	},

	actions: {
		async axiosAction(data: {
			url: string;
			params: object;
			method: string;
		}) {
			const api = axios.create({
				headers: {
					Authorization: `Bearer ${userAuthData.value.token}`,
				},
			});
			const method = data.method as "get" | "post" | "put" | "delete";
			await api[method](`${BASE_URL}/${data.url}`, data.params)
				.then((res) => {
					this.axios_result = {
						data: res.data,
						status: res.status,
					};
				})
				.catch((err) => {
					this.axios_result = {
						data: err.response.data,
						status: err.response.status,
					};
				});
		},
	},
});
