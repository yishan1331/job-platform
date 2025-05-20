import { useI18n } from "vue-i18n";
import { computed } from "vue";

export const jobTypeOptions = computed(() => {
	const { t } = useI18n();
	return [
		{ text: t("job.typeOptions.full_time"), value: "full-time" },
		{ text: t("job.typeOptions.part_time"), value: "part-time" },
		{ text: t("job.typeOptions.internship"), value: "internship" },
	];
});

export const getSkillOptions = () => {
	return [
		{ text: "JavaScript", value: "javascript" },
		{ text: "TypeScript", value: "typescript" },
		{ text: "Vue.js", value: "vue" },
		{ text: "React", value: "react" },
		{ text: "Node.js", value: "node" },
		{ text: "Python", value: "python" },
		{ text: "Java", value: "java" },
		{ text: "C#", value: "csharp" },
		{ text: "PHP", value: "php" },
		{ text: "Ruby", value: "ruby" },
	];
};

export const salaryTypeOptions = computed(() => {
	const { t } = useI18n();
	return [
		{ text: t("job.salaryTypeOptions.annual"), value: "annual" },
		{ text: t("job.salaryTypeOptions.monthly"), value: "monthly" },
		{ text: t("job.salaryTypeOptions.hourly"), value: "hourly" },
	];
});

export const statusOptions = computed(() => {
	const { t } = useI18n();
	return [
		{ text: t("job.statusOptions.active"), value: "Active" },
		{ text: t("job.statusOptions.expired"), value: "Expired" },
		{ text: t("job.statusOptions.scheduled"), value: "Scheduled" },
	];
});
