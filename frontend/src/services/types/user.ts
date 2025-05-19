type User = {
	userNo: number;
	userID: string;
	userName: string;
	pwd: string;
	email: string;
	levelNo: number;
	remark: string;
	creatorNo: number;
	modifierNo: number;
	accessPermission: AccessPermission;
	createTime: string;
	updateTime: string;
};

type AccessPermission = {
	levelNo: number;
	levelName: string;
	accessList: object | string;
	levelInfo: string;
	remark: string;
	creatorNo: number;
	modifierNo: number;
	createTime: string;
	updateTime: string;
};

type UserFilters = {
	isActive: boolean;
	search: string;
};

type UserSessions = {
	loginTime: Date;
	access: string;
};

type UserRole = "admin" | "user" | "guest";

export { User, AccessPermission, UserFilters, UserSessions, UserRole };
