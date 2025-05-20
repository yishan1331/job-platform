import { computed } from "vue";

import { type APIsResponse, APIsParams } from "@/services/utils";
import { useCommonAxiosStore } from "@/stores/common-axios";
import { errorAuthHandling } from "@/services/utils";

const store = useCommonAxiosStore();
const axiosResult = computed(() => store.axiosResult);

export const axiosAPI = async (params: Partial<APIsParams>) => {
	const result: APIsResponse = {
		statusCode: 401,
		response: {
			message: "",
			code: "",
			detail: "",
		},
	};

	try {
		if (!params.url || !params.method) {
			throw new Error("Missing required parameters: url and method");
		}

		await store.axiosAction(params);
		console.log(axiosResult.value);
		if (axiosResult.value.status !== 200) {
			result.statusCode = axiosResult.value.status;
			result.response = {
				message: axiosResult.value.data.message || "",
				code: axiosResult.value.data.code || "",
				detail: axiosResult.value.data.details || "",
			};

			if (
				axiosResult.value.status === 401 &&
				params.url != "token/pair"
			) {
				errorAuthHandling();
				return;
			}
			return result;
		}

		result.statusCode = 200;
		result.response = {
			message: "Success",
			code: "SUCCESS",
			items: axiosResult.value.data.items || axiosResult.value.data || [],
			count: axiosResult.value.data.count || 0,
			detail: axiosResult.value.data,
		};

		return result;
	} catch (error) {
		console.error("An error occurred:", error);
		result.statusCode = 500;
		result.response = {
			message: "Internal Server Error",
			code: "INTERNAL_ERROR",
			detail: error instanceof Error ? error.message : "Unknown error",
		};
		return result;
	}
};
