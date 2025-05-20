export const getNow = (date: null | Date = null) => {
	const nowDate = date === null ? new Date() : date;
	const returnobj = dateFormat(nowDate);
	const obj = {
		now: "",
		nowFormat: "",
		monthStart: "",
		monthEnd: "",
		currentMonth: 0,
		daysInMonth: 0,
	};
	obj.now = `${returnobj.weekday}, ${returnobj.month}月 ${returnobj.day}, ${returnobj.year}`;

	const timePart = [
		nowDate.getHours(),
		nowDate.getMinutes(),
		nowDate.getSeconds(),
	]
		.map((n) => n.toString().padStart(2, "0"))
		.join(":");

	obj.nowFormat = `${returnobj.year}-${returnobj.month}-${returnobj.day} ${timePart}`;

	// 當前月的第一天和最後一天
	const firstDay = new Date(nowDate.getFullYear(), nowDate.getMonth(), 1);
	const lastDay = new Date(nowDate.getFullYear(), nowDate.getMonth() + 1, 0);

	obj.monthStart = `${firstDay.getFullYear()}-${(firstDay.getMonth() + 1)
		.toString()
		.padStart(2, "0")}-${firstDay.getDate().toString().padStart(2, "0")}`;

	obj.monthEnd = `${lastDay.getFullYear()}-${(lastDay.getMonth() + 1)
		.toString()
		.padStart(2, "0")}-${lastDay.getDate().toString().padStart(2, "0")}`;

	obj.currentMonth = nowDate.getMonth() + 1; // 月份從 0 開始，所以要加 1
	obj.daysInMonth = new Date(
		nowDate.getFullYear(),
		obj.currentMonth,
		0
	).getDate(); // 取得當前月的天數

	return obj;
	// setDate(obj)
};
export const dateFormat = (time: Date) => {
	const weekdays = [
		"星期日",
		"星期一",
		"星期二",
		"星期三",
		"星期四",
		"星期五",
		"星期六",
	];
	const thisDay = time.getDate() < 10 ? `0${time.getDate()}` : time.getDate();
	const thisMonth =
		time.getMonth() + 1 < 10
			? `0${time.getMonth() + 1}`
			: time.getMonth() + 1;
	return {
		year: time.getFullYear(),
		month: thisMonth,
		day: thisDay,
		weekday: weekdays[time.getDay()],
	};
};
