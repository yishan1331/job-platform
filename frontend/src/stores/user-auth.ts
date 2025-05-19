import { defineStore } from "pinia";
import { cloneDeep } from "lodash";

export const useUserAuthStore = defineStore("user", {
	state: () => {
		return {
			login_details: {
				login_email: "",
				login_username: "",
				login_status: false,
				login_token: "",
				login_role: "",
				login_id: "",
			},

			DEFAULT_login_details: {
				login_email: "",
				login_username: "",
				login_status: false,
				login_token: "",
				login_role: "",
				login_id: "",
			},
			added_route_to_remove: [] as any[],

			language: "gb",
		};
	},

	getters: {
		userAuthData: (state) => {
			return {
				email: state.login_details.login_email,
				username: state.login_details.login_username,
				status: state.login_details.login_status,
				token: state.login_details.login_token,
				role: state.login_details.login_role,
				id: state.login_details.login_id,
			};
		},
		addedRouteToRemove: (state) => state.added_route_to_remove,
		settingLanguage: (state) => state.language,
	},

	actions: {
		setUserAuthData(obj: {
			email: string;
			status: boolean;
			role: string;
			username: string;
			id: string;
		}) {
			this.login_details.login_email = obj.email;
			this.login_details.login_status = obj.status;
			this.login_details.login_role = obj.role;
			this.login_details.login_username = obj.username;
			this.login_details.login_id = obj.id;
		},

		setUserAuthToken(token: string) {
			this.login_details.login_token = token;
		},

		resetUserAuthData() {
			this.login_details = cloneDeep(this.DEFAULT_login_details);
		},

		setAddedRouteToRemove(func: any) {
			this.added_route_to_remove.push(func);
		},

		setLanguage(language: string) {
			this.language = language;
		},
	},
});
