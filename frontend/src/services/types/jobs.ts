export type SelectOption = {
	text: string;
	value: string;
};

export type JobPosting = {
	id: string;
	title: string;
	company_name: string;
	company_id: string | SelectOption;
	location: string;
	type: string;
	description: string;
	min_salary: number;
	max_salary: number;
	salary_type: string;
	required_skills: string[];
	posting_date: Date;
	expiration_date: Date;
	apply_url: string;
	created_by: string;
	modified_by: string;
	is_active: boolean;
	created_at: string;
	updated_at: string;
};

export type JobPostingCreate = Omit<
	JobPosting,
	"id" | "created_at" | "updated_at" | "created_by" | "modified_by"
>;
export type JobPostingUpdate = Partial<JobPostingCreate>;
