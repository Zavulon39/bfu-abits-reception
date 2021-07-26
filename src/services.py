import datetime as dt
import json, xlsxwriter


def write_table(fio: str, date: dt.date, time: dt.time):
    try:
        data = json.load(open('./static/abits.json', 'r'))
        data.append({
            'fio': fio,
            'date': str(date),
            'time': str(time)
        })

        workbook = xlsxwriter.Workbook('./static/abits.xlsx')
        worksheet = workbook.add_worksheet()

        for row, value in enumerate(data):
            worksheet.write(row, 0, value['fio'])
            worksheet.write(row, 1, value['date'])
            worksheet.write(row, 2, value['time'])

        workbook.close()
        json.dump(data, open('./static/abits.json', 'w'))

        return True
    except:
        return False
