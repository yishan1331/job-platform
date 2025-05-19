<template>
	<div>
		<VaDataTable
			v-model:sort-by="sortByVModel"
			v-model:sorting-order="sortingOrderVModel"
			:items="tableData"
			:columns="columns"
			:loading="loading"
		>
			<template #cell(is_active)="{ rowData }">
				<VaBadge
					:text="rowData.is_active ? 'Active' : 'Inactive'"
					:color="rowData.is_active ? 'success' : 'danger'"
					style="font-size: 18px"
				/>
			</template>
			<template #cell(actions)="{ rowData }">
				<div class="flex gap-2">
					<VaButton
						icon="edit"
						size="small"
						preset="secondary"
						@click="$emit('editData', rowData)"
						:disabled="!checkUserRoleIsRecruiter"
					/>
					<VaButton
						icon="delete"
						size="small"
						color="danger"
						preset="secondary"
						@click="onDataDelete(rowData)"
						:disabled="!checkUserRoleIsRecruiter"
					/>
				</div>
			</template>
		</VaDataTable>

		<AppTablePaginationBar :pagination="$props.pagination" />
	</div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import { storeToRefs } from "pinia";
import { useModal } from "vuestic-ui";
import { useVModel } from "@vueuse/core";
import { type JobPosting } from "@/services/types/jobs";
import { useUserAuthStore } from "@/stores/user-auth";
import { checkUserRoleIsRecruiter } from "@/services/utils/user";
import AppTablePaginationBar from "@/components/table-pagination/AppTablePaginationBar.vue";

const { t } = useI18n();
const AuthStore = useUserAuthStore();
const { userAuthData } = storeToRefs(AuthStore);

const props = defineProps<{
	tableData: JobPosting[];
	loading: boolean;
	sortBy: string;
	sortingOrder: "asc" | "desc" | null;
	pagination: {
		page: number;
		perPage: number;
		total: number;
	};
}>();

const emit = defineEmits<{
	(event: "editData", data: JobPosting): void;
	(event: "deleteData", data: JobPosting): void;
	(event: "update:sort-by", value: string): void;
	(event: "update:sorting-order", value: "asc" | "desc" | null): void;
}>();

const sortByVModel = useVModel(props, "sortBy", emit);
const sortingOrderVModel = useVModel(props, "sortingOrder", emit);

const columns = [
	{
		key: "title",
		label: t("job.title"),
		sortable: false,
	},
	{
		key: "company_name",
		label: t("job.company_name"),
		sortable: false,
	},
	{
		key: "type",
		label: t("job.type"),
		sortable: false,
	},
	{
		key: "location",
		label: t("job.location"),
		sortable: false,
	},
	{
		key: "description",
		label: t("job.description"),
		sortable: false,
	},
	{
		key: "min_salary",
		label: t("job.min_salary"),
		sortable: false,
	},
	{
		key: "max_salary",
		label: t("job.max_salary"),
		sortable: false,
	},
	{
		key: "salary_type",
		label: t("job.salary_type"),
		sortable: false,
	},
	{
		key: "required_skills",
		label: t("job.required_skills"),
		sortable: false,
	},
	{
		key: "posting_date",
		label: t("job.posting_date"),
		sortable: true,
	},
	{
		key: "expiration_date",
		label: t("job.expiration_date"),
		sortable: true,
	},
	{
		key: "apply_url",
		label: t("job.apply_url"),
		sortable: false,
	},
	{
		key: "is_active",
		label: t("job.is_active"),
		sortable: false,
	},
	{
		key: "created_at",
		label: t("job.created_at"),
		sortable: false,
	},
	{
		key: "updated_at",
		label: t("job.updated_at"),
		sortable: false,
	},
	{
		key: "actions",
		label: t("table.actions"),
	},
];

const { confirm } = useModal();

const onDataDelete = async (data: JobPosting) => {
	const agreed = await confirm({
		title: `${t("table.delete")}`,
		message: `${t("table.deleteConfirm")} “${data.title}” ?`,
		okText: t("table.delete"),
		cancelText: t("table.cancel"),
		size: "small",
		maxWidth: "380px",
	});

	if (agreed) {
		emit("deleteData", data);
	}
};
</script>
