import * as XLSX from 'xlsx'
import { saveAs } from 'file-saver'
import { getNow } from '@/components/timer/Timer'

export const downloadToExcel = (
	t: Function,
	data: Record<string, any>[],
	filename: string,
	i18nKey: string,
	xlsxColumnOrder?: any[]
) => {
	// 建立工作表
	const worksheet = XLSX.utils.json_to_sheet([], { skipHeader: true });

	// 生成新的表頭
	let newHeaderEN = [] as any[]; // 英文表頭
	let newHeaderTC = [] as any[]; // 中文表頭
	const existingFields = new Set(xlsxColumnOrder?.map(item => Array.isArray(item) ? item[0] : item)); // 已存在的header

	// 如果提供了 xlsxColumnOrder，按其順序生成表頭
	if (xlsxColumnOrder && xlsxColumnOrder.length > 0) {
		xlsxColumnOrder.forEach((col) => {
			if (Array.isArray(col)) {
				const colEN = col[0] ?? '';
				const colTC = col[1] ?? '';
				newHeaderEN.push({ v: colEN, t: 's', r: `<t>${colEN}</t>` });
				newHeaderTC.push({ v: colTC, t: 's', r: `<t>${colTC}</t>` });
			} else {
				newHeaderEN.push({ v: col, t: 's', r: `<t>${col}</t>` });
				// const i18nValue = t(`${i18nKey}.${col}`, col); // 沒找到就回傳col
				const translation = t(`${i18nKey}.${col}`);
				const i18nValue = translation === `${i18nKey}.${col}` ? '' : translation; // 沒找到就回傳空
				newHeaderTC.push({ v: i18nValue, t: 's', r: `<t>${i18nValue}</t>` });
			}
		});
	}

	// 添加未在 xlsxColumnOrder 中列出的字段到表头
	Object.keys(data[0]).forEach((key) => {
		if (!existingFields.has(key)) {
			newHeaderEN.push({ v: key, t: 's', r: `<t>${key}</t>` });
			// const i18nValue = t(`${i18nKey}.${key}`, key); // 沒找到就回傳key
			const translation = t(`${i18nKey}.${key}`);
			const i18nValue = translation === `${i18nKey}.${key}` ? '' : translation; // 沒找到就回傳空
			newHeaderTC.push({ v: i18nValue, t: 's', r: `<t>${i18nValue}</t>` }); // v:單元格的實際值 t:單元格的資料類型(s字串,n數字,b布林,d日期) r:定義儲存格內容的格式，如字體、顏色等。
		}
	});

	// 添加新的表頭到工作表
	XLSX.utils.sheet_add_aoa(worksheet, [newHeaderTC, newHeaderEN], { origin: 'A1' });

	// 生成數據行，包括所有表頭
	const orderedData = data.map((item) => {
		const orderedItem: { [key: string]: string } = {};
		newHeaderEN.forEach((key) => {
			orderedItem[key.v] = item[key.v] ?? '';
		})
		return orderedItem;
	});

	// 添加數據從 A3 开始
	XLSX.utils.sheet_add_json(worksheet, orderedData, { skipHeader: true, origin: 'A3' });

	// 動態設置列寬
	const columnWidths = newHeaderEN.map((header, index) => {
		// 取得對應列的數據
		const columnData = orderedData.map(item => item[header.v]);

		// 計算每一列的最大長度
		const maxLength = Math.max(...columnData.map(value => (value ? value.toString().length : 0)));

		// 傳回列寬對象
		return { wch: Math.max(maxLength, header.v.length, (newHeaderTC[index].v.length)*2) +5 }; // 比較資料長度和中英表頭長度（中文長度*2），取最大值，避免寬度太剛好再+5
	});
	// 設置列寬
	worksheet['!cols'] = columnWidths;

	// 创建工作簿
	const workbook = XLSX.utils.book_new()
	XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1')

	// 导出Excel文件
	const excelBuffer = XLSX.write(workbook, {
		bookType: 'xlsx',
		type: 'array',
	})
	const blob = new Blob([excelBuffer], { type: 'application/octet-stream' })
	saveAs(blob, `${filename}_${getNow().nowFormat.split(' ')[0]}.xlsx`)
}
