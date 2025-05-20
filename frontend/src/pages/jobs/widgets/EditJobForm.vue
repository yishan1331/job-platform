<template>
	<VaForm
		v-slot="{ isValid }"
		ref="add-data-form"
		class="flex-col justify-start items-start gap-4 inline-flex w-full"
	>
		<div class="self-stretch flex-col justify-start items-start gap-4 flex">
			<div class="flex gap-4 flex-col sm:flex-row w-full">
				<VaInput
					v-model="formData.title"
					:label="t('job.title')"
					:rules="[validators.required]"
					class="w-full sm:w-1/2"
				/>

				<VaSelect
					v-model="formData.company_id"
					:label="t('job.company_name')"
					:options="props.allCompaniesList"
					:rules="[validators.required]"
					class="w-full sm:w-1/2"
					track-by="value"
					:disabled="!!props.job"
				/>
			</div>

			<div class="flex gap-4 flex-col sm:flex-row w-full">
				<VaInput
					v-model="formData.location"
					:label="t('job.location')"
					:rules="[validators.required]"
					class="w-full sm:w-1/2"
				/>

				<VaSelect
					v-model="formData.type"
					:label="t('job.type')"
					:options="jobTypeOptions"
					:rules="[validators.required]"
					class="w-full sm:w-1/2"
					track-by="value"
				/>
			</div>

			<div class="flex gap-4 flex-col sm:flex-row w-full">
				<VaTextarea
					v-model="formData.description"
					:label="t('job.description')"
					:rules="[validators.required]"
					class="w-full"
				/>
			</div>

			<div class="flex gap-4 flex-col sm:flex-row w-full">
				<VaSelect
					v-model="formData.salary_type"
					:label="t('job.salary_type')"
					:options="salaryTypeOptions"
					:rules="[validators.required]"
					class="w-full sm:w-1/3"
					track-by="value"
				/>
				<VaInput
					v-model="formData.min_salary"
					type="number"
					:label="t('job.min_salary')"
					class="w-full sm:w-1/3"
				/>

				<VaInput
					v-model="formData.max_salary"
					type="number"
					:label="t('job.max_salary')"
					class="w-full sm:w-1/3"
				/>
			</div>

			<div class="flex gap-4 flex-col sm:flex-row w-full">
				<VaSelect
					v-model="formData.required_skills"
					:label="t('job.required_skills')"
					:rules="[validators.requiredArray]"
					class="w-full sm:w-1/2"
					multiple
					:options="getSkillOptions()"
					track-by="value"
				/>
				<VaInput
					v-model="formData.apply_url"
					:label="t('job.apply_url')"
					class="w-full sm:w-1/2"
				/>
			</div>

			<div class="flex gap-4 flex-col sm:flex-row w-full">
				<VaDateInput
					v-model="formData.posting_date"
					:label="t('job.posting_date')"
					:rules="[validators.required]"
					class="w-full sm:w-1/2"
				/>

				<VaDateInput
					v-model="formData.expiration_date"
					:label="t('job.expiration_date')"
					class="w-full sm:w-1/2"
				/>
			</div>

			<VaCheckbox
				v-if="props.job"
				v-model="formData.is_active"
				:label="t('job.is_active')"
				class="mb-4"
			/>
		</div>

		<div
			class="flex gap-2 flex-col-reverse items-stretch justify-end w-full sm:flex-row sm:items-center"
		>
			<VaButton @click="$emit('close')" preset="secondary">
				{{ t("table.cancel") }}
			</VaButton>
			<VaButton :disabled="!isValid" @click="onSave">
				{{ saveButtonLabel }}
			</VaButton>
		</div>
	</VaForm>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useForm } from "vuestic-ui";
import { useI18n } from "vue-i18n";
import { type JobPosting } from "@/services/types/jobs";
import { validators } from "@/services/utils";
import {
	jobTypeOptions,
	getSkillOptions,
	salaryTypeOptions,
} from "@/services/utils/jobOptions";

const { t } = useI18n();

const props = defineProps<{
	job: JobPosting | null;
	saveButtonLabel: string;
	allCompaniesList: Array<{ text: string; value: string }>;
}>();

const emit = defineEmits<{
	(e: "close"): void;
	(e: "save", job: JobPosting): void;
}>();

const form = useForm("add-data-form");

const formData = ref<Partial<JobPosting>>({
	title: "",
	company_id: "",
	location: "",
	type: "",
	description: "",
	min_salary: 1,
	max_salary: 1,
	salary_type: "",
	required_skills: [],
	posting_date: new Date(),
	expiration_date: new Date(),
	apply_url: "",
	is_active: true,
});

onMounted(() => {
	if (props.job) {
		formData.value = { ...props.job };
	}
});

const onSave = async () => {
	if (form.validate()) {
		const data = { ...formData.value };

		// 處理 company_id
		if (typeof data.company_id === "object" && data.company_id !== null) {
			data.company_id = (data.company_id as { value: string }).value;
		}

		// 處理 type
		if (typeof data.type === "object" && data.type !== null) {
			data.type = (data.type as { value: string }).value;
		}

		// 處理 salary_type
		if (typeof data.salary_type === "object" && data.salary_type !== null) {
			data.salary_type = (data.salary_type as { value: string }).value;
		}

		// 處理 required_skills
		if (Array.isArray(data.required_skills)) {
			data.required_skills = data.required_skills.map((skill) =>
				typeof skill === "object"
					? (skill as { value: string }).value
					: skill
			);
		}

		emit("save", data as JobPosting);
	}
};
</script>
