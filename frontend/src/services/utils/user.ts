import { computed } from "vue";
import { useUserAuthStore } from "@/stores/user-auth";
import { storeToRefs } from "pinia";

import { UserRole, AccessPermission, User } from "@/services/types/index";

const roleColors: Record<UserRole, string> = {
	admin: "success",
	user: "warning",
	guest: "danger",
};

const getPermissionColor = (data: AccessPermission) => {
	if (data) {
		let authorityNum = 0;
		const accessList = JSON.parse(data.accessList);
		const type_admin_num = Object.keys(accessList).length;
		Object.values(accessList).map((e) => {
			if (e.authority) authorityNum += 1;
		});
		const roleType =
			authorityNum === type_admin_num
				? "admin"
				: authorityNum <= 1
				  ? "guest"
				  : "user";
		return roleColors[roleType];
	}
};

const checkUserRoleIsRecruiter = computed(() => {
	const AuthStore = useUserAuthStore();
	const { userAuthData } = storeToRefs(AuthStore);
	return userAuthData.value.role != "applicant";
});

export {
	roleColors,
	getPermissionColor,
	// getAllUsers,
	checkUserRoleIsRecruiter,
};
