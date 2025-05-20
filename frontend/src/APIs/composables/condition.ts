import { ref } from "vue";

import { type Filters, Pagination, Sorting } from "@/services/utils";
import { getNow } from "@/components/timer/Timer";

export const makePaginationRef = () =>
	ref<Pagination>({ page: 1, perPage: 20, total: 0 });
export const makeSortingRef = () =>
	ref<Sorting>({ sortBy: "posting_date", sortingOrder: "desc" });
export const makeFiltersRef = () =>
	ref<Partial<Filters>>({ category: [], search: "", fuzzy: false });

export const conditionsManagement = (
	conditions?: Partial<Filters & Pagination & Sorting> | undefined
) => {
	let page = 0;
	let perPage = 0;
	let search = "";
	let category = "";
	let fuzzy = false;

	const isFilters = typeof conditions !== "undefined";
	if (isFilters) {
		const {
			page: _page,
			perPage: _perPage,
			search: _search,
			category: _category,
			fuzzy: _fuzzy,
		} = conditions as Partial<Filters & Pagination & Sorting>;
		page = _page as number;
		perPage = _perPage as number;
		search = String(_search) as string;
		category = (
			Array.isArray(_category)
				? _category.length > 1 && _category[1] != ""
					? _category.join("||")
					: _category[0]
				: _category
		) as string;
		fuzzy = _fuzzy as boolean;
	}

	const pageParams = isFilters
		? {
				page: page,
				perPage: perPage,
		  }
		: {};

	if (search != "") {
		let searchArray = search.split("||").map((e) => {
			if (e.split("^_^").length > 1) {
				let parts = e.split("^_^");
				parts[0] =
					parts[0] != "null"
						? getNow(new Date(parts[0])).nowFormat.split(" ")[0]
						: "";
				parts[1] =
					parts[1] != "null"
						? getNow(new Date(parts[1])).nowFormat.split(" ")[0]
						: "";
				if (parts[0] == "" && parts[1])
					[parts[0], parts[1]] = [parts[1], parts[0]];
				return parts.join("^_^");
			}
			return e;
		});

		search = searchArray.join("||");
	}
	const filterParams =
		search != ""
			? {
					attr: category,
					attrValue: search,
					fuzzy: fuzzy,
			  }
			: {};

	const sortingParams = {
		sortBy: conditions?.sortBy,
		sortingOrder: conditions?.sortingOrder,
	};
	return {
		page,
		perPage,
		pageParams,
		filterParams,
		sortingParams,
	};
};
