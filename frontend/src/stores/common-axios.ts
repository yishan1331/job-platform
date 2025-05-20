import { defineStore } from "pinia";
import axios, { AxiosResponse, AxiosError } from "axios";
import { storeToRefs } from "pinia";

import { useUserAuthStore } from "@/stores/user-auth";

const AuthStore = useUserAuthStore();
const { userAuthData } = storeToRefs(AuthStore);

export type AxiosResult<T = unknown> = {
	data: T;
	status: number;
};

export type HttpMethod = "get" | "post" | "put" | "delete";

export type AxiosActionParams = {
	url: string;
	params?: Record<string, unknown>;
	data?: Record<string, unknown>;
	method: HttpMethod;
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
		async axiosAction<T = unknown>(data: AxiosActionParams) {
			const api = axios.create({
				headers: {
					Authorization: `Bearer ${userAuthData.value.token}`,
				},
			});

			try {
				let response: AxiosResponse<T>;

				if (data.method === "get" || data.method === "delete") {
					response = await api[data.method]<T>(
						`${BASE_URL}/${data.url}`,
						{ params: data.params }
					);
				} else {
					// POST 和 PUT 請求使用 data 作為請求體
					response = await api[data.method]<T>(
						`${BASE_URL}/${data.url}`,
						data.data || data.params
					);
				}

				this.axios_result = {
					data: response.data,
					status: response.status,
				};
			} catch (error) {
				const axiosError = error as AxiosError<T>;
				this.axios_result = {
					data: axiosError.response?.data as T,
					status: axiosError.response?.status ?? 500,
				};
			}
		},
	},
});
