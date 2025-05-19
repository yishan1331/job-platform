export type EpowerMeter = {
	voltage_avg: number
	amper_avg: number
	accumulated_energy: number
	upload_at: string
}

export type AllEpowerMeterLastData = {
	gateway_energymeter1: EpowerMeter | []
	gateway_energymeter2: EpowerMeter | []
	gateway_energymeter3: EpowerMeter | []
	gateway_energymeter4: EpowerMeter | []
	gateway_energymeter5: EpowerMeter | []
}
