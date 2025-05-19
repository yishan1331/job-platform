import { useI18n } from "vue-i18n";

export const getJobTypeOptions = () => {
	const { t } = useI18n();
	return [
		{ text: t("job.typeOptions.full_time"), value: "full-time" },
		{ text: t("job.typeOptions.part_time"), value: "part-time" },
		{ text: t("job.typeOptions.internship"), value: "internship" },
	];
};

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

export const getSalaryTypeOptions = () => {
	return [
		{ text: "Annual", value: "annual" },
		{ text: "Monthly", value: "monthly" },
		{ text: "Hourly", value: "hourly" },
	];
};

export const getStatusOptions = () => {
	const { t } = useI18n();
	return [
		{ text: t("job.statusOptions.active"), value: "Active" },
		{ text: t("job.statusOptions.expired"), value: "Expired" },
		{ text: t("job.statusOptions.scheduled"), value: "Scheduled" },
	];
};
