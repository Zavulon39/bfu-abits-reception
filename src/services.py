import datetime as dt
import xlsxwriter

idx = 0


def write_table(fio: str, datetime: dt.datetime):
    try:
        workbook = xlsxwriter.Workbook('./static/abits.xlsx')
        worksheet = workbook.add_worksheet()

        worksheet.write(idx, 0, fio)
        worksheet.write(idx, 1, f'{datetime.date()} {str(datetime.time()).split(".")[0]}')

        workbook.close()
        return True
    except:
        return False

