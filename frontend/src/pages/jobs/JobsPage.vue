<template>
	<p class="va-h4 font-bold">{{ $t("sidebar.jobs") }}</p>

	<VaCard outlined color="backgroundPrimary">
		<VaCardContent>
			<div class="w-full gap-2 mb-2 relative">
				<AppFilterSearchBar
					:filters="filters"
					:categoryConfig="categoryConfig"
					:searchConfig="searchConfig"
				/>
				<div
					v-if="checkUserRoleIsRecruiter"
					class="absolute top-0 right-0"
				>
					<VaButton
						@click="showAddDataModal"
						color="primary"
						icon="add"
						preset="primary"
						style="min-width: 5.5rem"
						>{{ $t("table.add") }}</VaButton
					>
				</div>
			</div>
			<JobsTable
				v-model:sort-by="sorting.sortBy"
				v-model:sorting-order="sorting.sortingOrder"
				:tableData="tableData"
				:loading="isLoading"
				:pagination="pagination"
				@editData="showEditDataModal"
				@deleteData="onDataDelete"
			/>
		</VaCardContent>
	</VaCard>

	<VaModal
		v-slot="{ cancel, ok }"
		v-model="doShowEditDataModal"
		size="small"
		mobile-fullscreen
		close-button
		hide-default-actions
		:before-cancel="beforeEditFormModalClose"
	>
		<h1 class="va-h6">
			{{ dataToEdit ? $t("table.editJob") : $t("table.addJob") }}
		</h1>
		<EditJobForm
			ref="editFormRef"
			:job="dataToEdit"
			:allCompaniesList="filteredCompaniesList"
			:save-button-label="dataToEdit ? $t('table.save') : $t('table.add')"
			@close="cancel"
			@save="
				(job) => {
					onDataSaved(job);
					ok();
				}
			"
		/>
	</VaModal>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useModal, useToast } from "vuestic-ui";
import { useI18n } from "vue-i18n";
import { storeToRefs } from "pinia";

import JobsTable from "./widgets/JobsTable.vue";
import EditJobForm from "./widgets/EditJobForm.vue";
import AppFilterSearchBar from "@/components/filter-search-bar/AppFilterSearchBar.vue";
import { errorHandling, type Sorting, Filters } from "@/services/utils";
import { type JobPosting, type SelectOption } from "@/services/types/jobs";
import { useJobs } from "./composables/useJobs";
import { useUserAuthStore } from "@/stores/user-auth";
import { checkUserRoleIsRecruiter } from "@/services/utils/user";
import {
	getJobTypeOptions,
	getSkillOptions,
	getSalaryTypeOptions,
	getStatusOptions,
} from "@/services/utils/jobOptions";
const AuthStore = useUserAuthStore();
const { userAuthData } = storeToRefs(AuthStore);

const { t } = useI18n();

const doShowEditDataModal = ref(false);
const dataToEdit = ref<JobPosting | null>(null);
const allCompanies = ref<Record<string, string>>({});
const filteredCompaniesList = ref<Array<{ text: string; value: string }>>([]);

const {
	jobs: tableData,
	statusCode,
	response,
	isLoading,
	filters,
	sorting,
	pagination,
	...jobsAPI
} = useJobs();

const categoryConfig = ref({
	options: [
		{
			text: t("job.search"),
			value: "search",
		},
		{
			text: t("job.status"),
			value: "status",
		},
		{
			text: t("job.location"),
			value: "location",
		},
		{
			text: t("job.salary_type"),
			value: "salary_type",
		},
		{
			text: t("job.type"),
			value: "type",
		},
	],
	types: {
		search: "text",
		status: "select",
		location: "text",
		salary_type: "select",
		type: "select",
	},
	label: {
		search: t("job.searchPlaceholder"),
		status: t("job.status"),
		location: t("job.location"),
		salary_type: t("job.salary_type"),
		type: t("job.type"),
	},
});

const searchConfig = ref({
	search: {
		placeholder: t("table.search"),
	},
	status: getStatusOptions(),
	type: getJobTypeOptions(),
	skill: getSkillOptions(),
	salary_type: getSalaryTypeOptions(),
});

const showEditDataModal = (job: JobPosting) => {
	// 將 company_id 轉換為 VaSelect 需要的格式
	const jobWithFormattedCompany = {
		...job,
		company_id: {
			text: job.company_name,
			value: job.company_id as string,
		} as SelectOption,
	};
	dataToEdit.value = jobWithFormattedCompany;
	doShowEditDataModal.value = true;
};

const showAddDataModal = () => {
	dataToEdit.value = null;
	doShowEditDataModal.value = true;
};

const { init: notify } = useToast();

const _getData = async () => {
	await jobsAPI.fetch();
	if (statusCode.value !== 200) {
		errorHandling(response.value);
	}

	if (checkUserRoleIsRecruiter.value) {
		const { allCompaniesList: companies } = await jobsAPI.getCompanies();
		// 將公司資料轉換為 id: name 的格式
		allCompanies.value = companies.value.reduce(
			(
				acc: Record<string, string>,
				company: { id: string; name: string }
			) => {
				acc[company.id] = company.name;
				return acc;
			},
			{}
		);

		// 過濾公司列表
		filteredCompaniesList.value = companies.value
			.filter((company: { owner_id: string }) => {
				// 如果是管理員，顯示所有公司
				if (userAuthData.value?.role === "admin") {
					return true;
				}
				// 如果是招募者，只顯示自己擁有的公司
				return company.owner_id === userAuthData.value?.id;
			})
			.map((company: { name: string; id: string }) => ({
				text: company.name,
				value: company.id,
			}));
	}
};

const onDataSaved = async (job: JobPosting) => {
	if (dataToEdit.value) {
		await jobsAPI.update({
			...job,
			id: dataToEdit.value.id,
		});
	} else {
		await jobsAPI.add(job);
	}
	if (statusCode.value !== 201 && statusCode.value !== 200) {
		errorHandling(response.value);
		return;
	}
	notify({
		message: `${dataToEdit.value ? t("table.update") : t("table.add")} ${t(
			"table.success"
		)}`,
		color: "success",
	});
};

const onDataDelete = async (job: JobPosting) => {
	await jobsAPI.remove(job.id);
	if (
		statusCode.value !== 200 &&
		statusCode.value !== 201 &&
		statusCode.value !== 204
	) {
		errorHandling(response.value);
		return;
	}
	notify({
		message: `${t("table.delete")} ${t("table.success")}`,
		color: "success",
	});
};

const editFormRef = ref();

const { confirm } = useModal();

const beforeEditFormModalClose = async (hide: () => unknown) => {
	if (editFormRef.value.isFormHasUnsavedChanges) {
		const agreed = await confirm({
			maxWidth: "380px",
			message: t("table.beforeEditFormModalClose"),
			size: "small",
			okText: t("table.ok"),
			cancelText: t("table.cancel"),
		});
		if (agreed) {
			hide();
		}
	} else {
		hide();
	}
};

onMounted(() => {
	_getData();
});
</script>

<style scope lang="scss"></style>
