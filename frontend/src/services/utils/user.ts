import { computed } from "vue";
import { useUserAuthStore } from "@/stores/user-auth";
import { storeToRefs } from "pinia";

const checkUserRoleIsRecruiter = computed(() => {
	const AuthStore = useUserAuthStore();
	const { userAuthData } = storeToRefs(AuthStore);
	return userAuthData.value.role != "applicant";
});

export { checkUserRoleIsRecruiter };
