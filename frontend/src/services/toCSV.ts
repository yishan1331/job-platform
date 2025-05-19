import { getNow } from '@/components/timer/Timer'
export const toCSV = (data: Record<string, any>[]) => {
	const headers = Object.keys(data[0])
	const escapeCSVValue = (value: string | object) => {
		if (typeof value === 'string') {
			// 如果值中包含逗号或双引号，则将值括在双引号中，并将双引号替换为两个双引号
			if (value.includes(',') || value.includes('"') || value.includes('\n')) {
				return `"${value.replace(/"/g, '""')}"`
			} else {
				return value
			}
		} else {
			return value
		}
	}
	const csv = [
		headers.join(','),
		...data.map((row) =>
			headers.map((fieldName) => escapeCSVValue(row[fieldName])).join(',')
		),
	].join('\r\n')
	return csv
}

export const downloadAsCSV = (
	data: Record<string, any>[],
	filename: string
) => {
	if (typeof data === 'undefined') return
	const csv = toCSV(data)

	const blob = new Blob([csv], { type: 'text/csv' })

	const link = document.createElement('a')
	link.href = window.URL.createObjectURL(blob)
	link.download = `${filename}_${getNow().nowFormat.split(' ')[0]}`
	link.click()
}
