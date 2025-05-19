import i18n from "@/i18n";
import { useToast } from "vuestic-ui";
import { storeToRefs } from "pinia";
import { unref } from "vue";
import { cloneDeep } from "lodash";

import { User, CUDBoxMsg } from "@/services/types/index";
import { UserLogs } from "@/services/types/index";
import { useAuth } from "@/pages/auth/composables/useAuth";
import { useUserAuthStore } from "@/stores/user-auth";

const { init: notify } = useToast();
const AuthStore = useUserAuthStore();
const { userAuthData } = storeToRefs(AuthStore);

const macRegex = /Duplicate entry '(.+?)' for key 'mac'/;
const snRegex = /Duplicate entry '(.+?)' for key 'sn'/;

export const sleep = (ms = 0) => {
	return new Promise((resolve) => setTimeout(resolve, ms));
};

export const errorAuthHandling = () => {
	notify({
		message: t("auth.login_timeout"),
		color: "danger",
	});
	useAuth().logOut();
	return;
};

export const errorCUDHandling = (dataCUDStatus: CUDBoxMsg) => {
	if (dataCUDStatus["errorNum"] > 0) {
		dataCUDStatus["errorMsg"] = dataCUDStatus["errorMsg"].map((error) => {
			if (macRegex.test(error)) {
				const macMatch = error.match(macRegex);
				const macValue = macMatch?.[1]; // 提取重複的 MAC 值
				return `<li>MAC資料：'${macValue}'已重複，無法建立</li>`;
			}
			if (snRegex.test(error)) {
				const snMatch = error.match(snRegex);
				const snValue = snMatch?.[1]; // 提取重複的序號值
				return `<li>序號資料：'${snValue}'已重複，無法建立</li>`;
			}
			return `<li>${error}</li>`;
		});
	}
	notify({
		message: `成功數量：${dataCUDStatus["successNum"]}${
			dataCUDStatus["successNum"] > 0
				? `<br>成功訊息：${dataCUDStatus["successMsg"].join("<br>")}`
				: ""
		}<br>失敗數量：${dataCUDStatus["errorNum"]}${
			dataCUDStatus["errorNum"] > 0
				? `<br>失敗訊息：<ul>${dataCUDStatus["errorMsg"].join("")}</ul>`
				: ""
		}`,
		color: "danger",
		dangerouslyUseHtmlString: true,
	});
};

export const getSortItem = (obj: any, sortBy: string) => {
	return obj[sortBy];
};

export const getFilterItem = (obj: any, condition: Filters) => {
	if (Number.isInteger(parseInt(condition.search))) {
		return obj[condition["category"]] == parseInt(condition.search);
	}
	return obj[condition["category"]]
		.toString()
		.toLowerCase()
		.includes(condition.search.toLowerCase());
};

export const filterSortingFn = (
	type: "filters" | "sorting",
	data: any,
	tempData: any,
	conditions: Partial<Filters> | Partial<Sorting>
) => {
	if (type === "filters") {
		const condition = {
			...unref(conditions),
		} as Filters;
		if (tempData.length > 0) {
			data = tempData;
		} else {
			tempData = data;
		}
		if (condition.search != "" && condition.category) {
			data = data.filter((e) => getFilterItem(e, condition));
		}
	} else {
		const condition = {
			...unref(conditions),
		} as Sorting;
		if (condition.sortBy && condition.sortingOrder) {
			data = data.sort((a, b) => {
				const first = getSortItem(a, condition.sortBy as string);
				const second = getSortItem(b, condition.sortBy as string);
				if (first > second) {
					return condition.sortingOrder === "asc" ? 1 : -1;
				}
				if (first < second) {
					return condition.sortingOrder === "asc" ? -1 : 1;
				}
				return 0;
			});
		}
	}
	return {
		data: data,
		tempData: tempData,
	};
};

export const errorHandling = (response: string, table?: string) => {
	if (response != "ok") {
		let notify_response = response;
		let caseKey = "";
		if (
			response.includes(
				"Cannot delete or update a parent row: a foreign key constraint fails"
			)
		) {
			caseKey = "ForeignKeyConstraintError";
		} else if (response.includes("Duplicate entry")) {
			caseKey = "DuplicateKeyConstraintError";
		}
		switch (caseKey) {
			case "ForeignKeyConstraintError":
				if (
					table == "accessPermission" &&
					response.includes("user_ibfk_1")
				)
					notify_response = "此權限名稱已有帳戶建立，無法做刪除";
				break;
			case "DuplicateKeyConstraintError":
				if (table == "box" && macRegex.test(response)) {
					const macMatch = response.match(macRegex);
					const macValue = macMatch?.[1];
					notify_response = `MAC資料：'${macValue}'已重複，無法建立`;
				}
				if (table == "box" && snRegex.test(response)) {
					const snMatch = response.match(snRegex);
					const snValue = snMatch?.[1];
					notify_response = `序號資料：'${snValue}'已重複，無法建立`;
				}
				if (
					table == "accessPermission" &&
					response.includes("for key 'levelName'")
				)
					notify_response = "權限名稱已重複，無法建立";
				break;
			default:
				break;
		}
		notify({
			message: notify_response,
			color: "danger",
			dangerouslyUseHtmlString: true,
		});
	}
};

const { t } = i18n.global;
// https://blog.csdn.net/weixin_46092505/article/details/126467080

/** Validation */
export const validators = {
	email: (v: string) => {
		if (!v) return true;
		const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
		return pattern.test(v) || t("validation.email");
	},
	numbersandcharacters: (v: string) => {
		const pattern = /^[a-zA-Z0-9]+$/;
		return (
			(pattern.test(v) && v.length >= 4 && v.length <= 8) ||
			t("validation.numbersandcharacters")
		);
	},
	required: (v: any) => !!v || t("validation.required"),
	requiredArray: (v: any[]) => v.length > 0 || t("validation.requiredArray"),
	passwordLength: (v: string) =>
		v == "___NOT_CHANGE_PASSWORD___" ||
		(v.length >= 6 && 17 > v.length) ||
		t("validation.passwordLength"),
	passwordFormat: (v: string) => {
		const allowedSymbols = "!@$_+=-";
		const pattern = new RegExp(`^[A-Za-z0-9${allowedSymbols}]*$`);
		return (
			pattern.test(v) ||
			t("validation.passwordFormat", { allowedSymbols })
		);
	},
	comfirmpassword: (v: string, cv: string) =>
		v === cv || t("validation.confirmpassword"),
};

const isProductionTimeValid = (productionTime: Date) => {
	const today = new Date();
	// 将今天的时间设为当天的最后一刻（23:59:59）
	today.setHours(23, 59, 59, 999);

	const productionDate = new Date(productionTime);
	return productionDate <= today;
};

export type Pagination = {
	page: number;
	perPage: number;
	total: number;
};

export type Sorting = {
	sortBy: keyof User | keyof UserLogs | string | "updateTime" | "createTime";
	sortingOrder: "asc" | "desc" | null;
};

export type Filters = {
	category: string[];
	fuzzy: boolean;
	search: string;
};

export type APIsParams = {
	url: string;
	method: "get" | "post" | "put" | "delete";
	params: object;
	[key: string]: any;
};

export type APIsResponse = {
	statusCode: number;
	response: {
		message: string;
		code?: string;
		detail?: string | object;
		items?: any[] | object;
		count?: number;
	};
};

export const organizeXLSXData = (tableData: any[]) => {
	let xlsxData = cloneDeep(tableData);
	// xlsxData = xlsxData.map((data) => {
	// 	data.creatorNo = users.value[data.creatorNo]
	// 		? users.value[data.creatorNo]
	// 		: data.creatorNo
	// 	data.modifierNo = users.value[data.modifierNo]
	// 		? users.value[data.modifierNo]
	// 		: data.modifierNo
	// 	return data
	// })
	return xlsxData;
};
