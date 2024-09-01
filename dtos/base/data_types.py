from pydantic import constr

# New stricter constraint type aliases
StrPopulated = constr(min_length=1, regex=r'\S+')
DatetimeIso8601 = constr(regex=r"^\d{4}(-\d{2}(-\d{2}(T\d{2}(:\d{2}(:\d{2}(\.\d{1,6})?)?)?(Z|[+-]\d{2}(:?\d{2})?)?)?)?)?$")
DateYmd = constr(regex=r'^\d{4}-\d{2}-\d{2}$')

# Examples to match for DatetimeIso8601
# [
#     "2024-09-01T12:30:45Z",    # Extended format with time and 'Z' timezone
#     "2024-09-01T12:30:45+02:00", # Extended format with time and positive offset
#     "20240901T123045Z",        # Basic format with time and 'Z' timezone
#     "20240901T123045+0200",    # Basic format with time and positive offset
#     "2024-09-01",              # Extended format date only
#     "20240901"                 # Basic format date only
# ]
