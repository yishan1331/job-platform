export type ProdCO2 = {
	prodID: string
	qty: number
	remark: string
	creatorNo: number
	modifierNo: number
	createTime: string
	updateTime: string
}

export interface DynamicQtyData {
	[key: `QTY${string}`]: number
}

export interface CO2DataEntry {
	qty: number
}
