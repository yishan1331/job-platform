import { storeToRefs } from "pinia";

import {
	type Filters,
	Pagination,
	Sorting,
	APIsResponse,
} from "@/services/utils";
import { type JobPosting } from "@/services/types/jobs";
import { useGlobalStore } from "@/stores/global-store";
import { axiosAPI } from "@/services/axios-api";
import { useUserAuthStore } from "@/stores/user-auth";
import { conditionsManagement } from "@/APIs/composables/condition";

const convertFilterParams = (filters: Partial<Filters>) => {
	const queryParams: Record<string, string> = {};

	if (filters.attr && filters.attrValue) {
		const attrs = filters.attr.split("||");
		const values = filters.attrValue.split("||");

		attrs.forEach((attr, index) => {
			if (values[index]) {
				queryParams[attr] = values[index];
			}
		});
	}

	if (filters.search) {
		queryParams.search = filters.search;
	}

	return queryParams;
};

const convertSortParams = (sortBy?: string, sortOrder?: string) => {
	if (!sortBy) return "";
	return `${sortOrder === "asc" ? "" : "-"}${sortBy}`;
};

const buildQueryString = (params: Record<string, any>) => {
	const queryParts = Object.entries(params)
		.filter(([_, value]) => value !== undefined && value !== "")
		.map(
			([key, value]) =>
				`${encodeURIComponent(key)}=${encodeURIComponent(value)}`
		);
	return queryParts.length > 0 ? `?${queryParts.join("&")}` : "";
};

export const getJobsConditions = async (
	conditions?: Partial<Filters & Pagination & Sorting> | undefined
) => {
	let apiResult: APIsResponse = {
		statusCode: 200,
		response: {
			message: "",
			code: "",
			detail: "",
			items: [],
			count: 0,
		},
	};

	const { page, perPage, pageParams, filterParams } =
		conditionsManagement(conditions);

	let filteredDatas: JobPosting[] = [];

	const queryParams = {
		page: pageParams.page,
		page_size: pageParams.perPage,
		order_by: convertSortParams(
			conditions?.sortBy as string,
			conditions?.sortingOrder as string
		),
		...convertFilterParams(filterParams),
	};

	const queryString = buildQueryString(queryParams);

	apiResult = (await axiosAPI({
		url: `jobs${queryString}`,
		method: "get",
	})) as APIsResponse;
	filteredDatas = apiResult.response.items as JobPosting[];

	apiResult.response.items = filteredDatas;
	return apiResult;
};

export const addJob = async (data: JobPosting) => {
	let apiResult: APIsResponse = {
		statusCode: 200,
		response: {
			message: "",
			code: "",
			detail: "",
			items: [],
			count: 0,
		},
	};

	apiResult = (await axiosAPI({
		url: "jobs",
		method: "post",
		data: data,
	})) as APIsResponse;
	return apiResult;
};

export const updateJob = async (data: JobPosting) => {
	let apiResult: APIsResponse = {
		statusCode: 200,
		response: {
			message: "",
			code: "",
			detail: "",
			items: [],
			count: 0,
		},
	};

	apiResult = (await axiosAPI({
		url: `jobs/${data.id}`,
		method: "put",
		data: data,
	})) as APIsResponse;
	return apiResult;
};

export const removeJob = async (id: string) => {
	let apiResult: APIsResponse = {
		statusCode: 200,
		response: {
			message: "",
			code: "",
			detail: "",
			items: [],
			count: 0,
		},
	};

	apiResult = (await axiosAPI({
		url: `jobs/${id}`,
		method: "delete",
	})) as APIsResponse;
	return apiResult;
};
