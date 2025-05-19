export type EpowerCO2 = {
	serialNo: number
	arewh: number
	co2: number
	remark: string
	creatorNo: number
	modifierNo: number
	createTime: string
	updateTime: string
}

export interface WHDataEntry {
	arewh: number;
	co2: number;
}
