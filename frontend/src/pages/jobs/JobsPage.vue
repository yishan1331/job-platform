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
				@detailData="handleShowDetailModal"
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

	<VaModal
		v-model="showDetailModal"
		size="medium"
		mobile-fullscreen
		close-button
		hide-default-actions
	>
		<h1 class="va-h6 mb-4">{{ $t("table.jobDetail") }}</h1>
		<VaCard v-if="jobDetail" class="mb-4">
			<VaCardContent>
				<div class="space-y-6">
					<!-- 標題區塊 -->
					<div class="border-b pb-4">
						<div class="flex justify-between items-start">
							<div>
								<h2 class="va-h5 mb-2">
									{{ jobDetail.title }}
								</h2>
								<div
									class="flex items-center gap-2 text-sm text-secondary"
								>
									<VaIcon name="business" size="small" />
									<span>{{ jobDetail.company_name }}</span>
								</div>
							</div>
							<div
								class="text-right text-xs text-secondary space-y-1"
							>
								<div class="flex items-center gap-1">
									<VaIcon name="schedule" size="small" />
									<span
										>{{ $t("job.created_at") }}:
										{{
											new Date(
												jobDetail.created_at
											).toLocaleString()
										}}</span
									>
								</div>
								<div class="flex items-center gap-1">
									<VaIcon name="update" size="small" />
									<span
										>{{ $t("job.updated_at") }}:
										{{
											new Date(
												jobDetail.updated_at
											).toLocaleString()
										}}</span
									>
								</div>
							</div>
						</div>
					</div>

					<!-- 主要資訊區塊 -->
					<div class="grid grid-cols-2 gap-6">
						<div class="space-y-4">
							<div>
								<p class="va-text-secondary mb-1">
									{{ $t("job.location") }}
								</p>
								<div class="flex items-center gap-2">
									<VaIcon name="place" size="small" />
									<p class="va-text-primary">
										{{ jobDetail.location }}
									</p>
								</div>
							</div>
							<div>
								<p class="va-text-secondary mb-1">
									{{ $t("job.type") }}
								</p>
								<div class="flex items-center gap-2">
									<VaIcon name="work" size="small" />
									<p class="va-text-primary">
										{{
											t(
												`job.typeOptions.${jobDetail.type}`
											)
										}}
									</p>
								</div>
							</div>
							<div>
								<p class="va-text-secondary mb-1">
									{{ $t("job.salary") }}
								</p>
								<div class="flex items-center gap-2">
									<VaIcon name="payments" size="small" />
									<p class="va-text-primary">
										$ {{ jobDetail.min_salary }} - $
										{{ jobDetail.max_salary }}
										<span
											class="text-sm text-secondary ml-1"
											>{{
												t(
													`job.salaryTypeOptions.${jobDetail.salary_type}`
												)
											}}</span
										>
									</p>
								</div>
							</div>
						</div>

						<div class="space-y-4">
							<div>
								<p class="va-text-secondary mb-1">
									{{ $t("job.posting_date") }}
								</p>
								<div class="flex items-center gap-2">
									<VaIcon name="event" size="small" />
									<p class="va-text-primary">
										{{
											new Date(
												jobDetail.posting_date
											).toLocaleDateString()
										}}
									</p>
								</div>
							</div>
							<div>
								<p class="va-text-secondary mb-1">
									{{ $t("job.expiration_date") }}
								</p>
								<div class="flex items-center gap-2">
									<VaIcon name="event_busy" size="small" />
									<p class="va-text-primary">
										{{
											new Date(
												jobDetail.expiration_date
											).toLocaleDateString()
										}}
									</p>
								</div>
							</div>
							<div>
								<p class="va-text-secondary mb-1">
									{{ $t("job.is_active") }}
								</p>
								<div class="flex items-center gap-2">
									<VaIcon
										:name="
											jobDetail.is_active
												? 'check_circle'
												: 'cancel'
										"
										size="small"
										:color="
											jobDetail.is_active
												? 'success'
												: 'danger'
										"
									/>
									<p class="va-text-primary">
										{{
											jobDetail.is_active
												? $t("job.active")
												: $t("job.inactive")
										}}
									</p>
								</div>
							</div>
						</div>
					</div>

					<!-- 描述區塊 -->
					<div class="border-t pt-4">
						<p class="va-text-secondary mb-2">
							{{ $t("job.description") }}
						</p>
						<p class="va-text-primary whitespace-pre-line">
							{{ jobDetail.description }}
						</p>
					</div>

					<!-- 技能要求區塊 -->
					<div class="border-t pt-4">
						<p class="va-text-secondary mb-2">
							{{ $t("job.required_skills") }}
						</p>
						<div class="flex flex-wrap gap-2">
							<VaChip
								v-for="skill in jobDetail.required_skills"
								:key="skill"
								size="small"
								color="primary"
							>
								{{ skill }}
							</VaChip>
						</div>
					</div>

					<!-- 申請按鈕 -->
					<div class="border-t pt-4 flex justify-end">
						<VaButton
							:disabled="!isValidApplyUrl"
							:color="isValidApplyUrl ? 'primary' : 'secondary'"
							class="w-full sm:w-auto"
							@click="handleApplyClick"
						>
							<template #prepend>
								<VaIcon
									:name="
										isValidApplyUrl
											? 'open_in_new'
											: 'link_off'
									"
								/>
							</template>
							{{ $t("job.apply_now") }}
						</VaButton>
					</div>
				</div>
			</VaCardContent>
		</VaCard>
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
	jobTypeOptions,
	salaryTypeOptions,
	statusOptions,
	getSkillOptions,
} from "@/services/utils/jobOptions";
const AuthStore = useUserAuthStore();
const { userAuthData } = storeToRefs(AuthStore);

const { t } = useI18n();

const doShowEditDataModal = ref(false);
const dataToEdit = ref<JobPosting | null>(null);
const allCompanies = ref<Record<string, string>>({});
const filteredCompaniesList = ref<Array<{ text: string; value: string }>>([]);
const showDetailModal = ref(false);
const jobDetail = ref<JobPosting | null>(null);

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

const categoryConfig = computed(() => ({
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
}));

const searchConfig = ref({
	search: {
		placeholder: t("table.search"),
	},
	status: statusOptions.value,
	type: jobTypeOptions.value,
	skill: getSkillOptions(),
	salary_type: salaryTypeOptions.value,
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

const handleShowDetailModal = async (job: JobPosting) => {
	jobDetail.value = null;
	showDetailModal.value = true;

	try {
		const result = await jobsAPI.getJobDetail(job.id);
		if (result?.response?.items) {
			jobDetail.value = result.response.items as JobPosting;
		}
	} catch (error) {
		errorHandling(error as Error);
	}
};

const isValidApplyUrl = computed(() => {
	if (!jobDetail.value?.apply_url) return false;
	try {
		new URL(jobDetail.value.apply_url);
		return true;
	} catch {
		return false;
	}
});

const handleApplyClick = () => {
	if (isValidApplyUrl.value && jobDetail.value?.apply_url) {
		window.open(jobDetail.value.apply_url, "_blank", "noopener,noreferrer");
	}
};

onMounted(() => {
	_getData();
});
</script>

<style scope lang="scss"></style>
