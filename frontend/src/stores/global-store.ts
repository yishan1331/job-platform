import { defineStore } from "pinia";

export const useGlobalStore = defineStore("global", {
	state: () => {
		return {
			isSidebarMinimized: false,
			dataTableHeight: 550,
			isTesting: process.env.NODE_ENV === "development",
			updateTime: 60000,
			version: "1.0",
		};
	},

	actions: {
		toggleSidebar(status: boolean | null = null) {
			if (status !== null) {
				this.isSidebarMinimized = status;
			} else {
				this.isSidebarMinimized = !this.isSidebarMinimized;
			}
		},
	},
});
