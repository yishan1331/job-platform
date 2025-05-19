import { ref, computed, Ref, watch } from "vue";
import { watchIgnorable } from "@vueuse/core";
import { type Filters, type Sorting, type Pagination } from "@/services/utils";
import {
	type JobPosting,
	type JobPostingCreate,
	type JobPostingUpdate,
} from "@/services/types/jobs";
import { getJobsConditions, addJob, updateJob, removeJob } from "@/APIs/jobs";
import { axiosAPI } from "@/services/axios-api";

import {
	makePaginationRef,
	makeSortingRef,
	makeFiltersRef,
} from "@/APIs/composables/condition";

export const useJobs = (options?: {
	pagination?: Ref<Pagination>;
	sorting?: Ref<Sorting>;
	filters?: Ref<Partial<Filters>>;
}) => {
	const jobs = ref<JobPosting[]>([]);
	const statusCode = ref<number>(0);
	const response = ref<string>("");
	const isLoading = ref(false);

	const {
		filters = makeFiltersRef(),
		sorting = makeSortingRef(),
		pagination = makePaginationRef(),
	} = options || {};

	const fetch = async () => {
		isLoading.value = true;
		const result = await getJobsConditions({
			...filters.value,
			...sorting.value,
			...pagination.value,
		});

		statusCode.value = result.statusCode;
		response.value = result.response.message;

		if (result.statusCode === 200) {
			jobs.value = result.response.items || [];
			pagination.value.total = result.response.count || 0;
		}

		isLoading.value = false;
	};

	watch(
		filters,
		() => {
			// Reset pagination to first page when filters changed
			pagination.value.page = 1;
			// filterFn('filters')
		},
		{ deep: true }
	);
	watch(
		sorting,
		() => {
			// Reset pagination to first page when filters changed
			pagination.value.page = 1;
			// filterFn('filters')
		},
		{ deep: true }
	);

	const { ignoreUpdates } = watchIgnorable(
		[pagination, filters, sorting],
		fetch,
		{
			deep: true,
		}
	);

	const add = async (job: JobPostingCreate) => {
		isLoading.value = true;
		const result = await addJob(job as JobPosting);

		statusCode.value = result.statusCode;
		response.value = result.response.message;
		if (statusCode.value === 201) await fetch();
		isLoading.value = false;
	};

	const update = async (job: JobPostingUpdate & { id: string }) => {
		isLoading.value = true;
		const result = await updateJob(job as JobPosting);

		statusCode.value = result.statusCode;
		response.value = result.response.message;
		if (statusCode.value === 201) await fetch();
		isLoading.value = false;
	};

	const remove = async (id: string) => {
		isLoading.value = true;
		const result = await removeJob(id);

		statusCode.value = result.statusCode;
		response.value = result.response.message;
		if (statusCode.value === 201) await fetch();
		isLoading.value = false;
	};

	const getCompanies = async () => {
		const allCompaniesList = ref([]);
		const result = await axiosAPI({
			url: "companies",
			method: "get",
			params: {},
		});

		allCompaniesList.value = result?.response.items;
		return { allCompaniesList };
	};

	return {
		jobs,
		statusCode,
		response,
		isLoading,
		filters,
		sorting,
		pagination,
		fetch,
		add,
		update,
		remove,
		getCompanies,
	};
};
