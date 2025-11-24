from datetime import datetime


class DateUtils:
    @staticmethod
    def format_datetime_to_brazilian(date_input: datetime | None) -> str:
        if date_input is None:
            return "-" 

        if isinstance(date_input, datetime):
            return date_input.strftime("%d/%m/%Y %H:%M")
        else:
            raise TypeError("date_input deve ser um objeto datetime ou None.")

    @staticmethod
    def format_date_str_to_brazilian(date_str):
        date = datetime.strptime(date_str, "%Y-%m-%d")
        return date.strftime("%d/%m/%Y")

    @staticmethod
    def get_date_str_from_request(date_str):
        if date_str is None:
            date = datetime.today().date()
            date_str = date.strftime('%Y-%m-%d')
        else:
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else datetime.today().date()
            except ValueError:
                date = datetime.today().date()
                date_str = date.strftime('%Y-%m-%d')

        return date_str

    @staticmethod
    def get_date_year_month_str_from_request(date_str):
        if date_str is None:
            date = datetime.today().date()
            date_str = date.strftime('%Y-%m')
        else:
            try:
                date = datetime.strptime(date_str, "%Y-%m").date() if date_str else datetime.today().date()
            except ValueError:
                date = datetime.today().date()
                date_str = date.strftime('%Y-%m')

        return date_str

    @staticmethod
    def remove_day(date_str):
        date = datetime.strptime(date_str, "%Y-%m-%d")
        return date.strftime("%Y-%m")
