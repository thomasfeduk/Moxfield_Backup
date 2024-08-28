from pydantic import constr

# New stricter constraint type aliases
StrPopulated = constr(min_length=1, regex=r'\S+')
DatetimeIso8601 = constr(regex=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$")
DateYmd = constr(regex=r'^\d{4}-\d{2}-\d{2}$')
