import { defineStore } from "pinia";
import { cloneDeep } from "lodash";

interface LoginDetails {
	login_email: string;
	login_username: string;
	login_status: boolean;
	login_token: string;
	login_role: string;
	login_id: string;
}

interface UserAuthData {
	email: string;
	username: string;
	status: boolean;
	token: string;
	role: string;
	id: string;
}

type RouteRemover = () => void;

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
			} as LoginDetails,

			DEFAULT_login_details: {
				login_email: "",
				login_username: "",
				login_status: false,
				login_token: "",
				login_role: "",
				login_id: "",
			} as LoginDetails,
			added_route_to_remove: [] as RouteRemover[],

			language: "gb",
		};
	},

	getters: {
		userAuthData: (state): UserAuthData => {
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
		setUserAuthData(obj: Omit<UserAuthData, "token">) {
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

		setAddedRouteToRemove(func: RouteRemover) {
			this.added_route_to_remove.push(func);
		},

		setLanguage(language: string) {
			this.language = language;
		},
	},
});
