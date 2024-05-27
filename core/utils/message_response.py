class APIDetailMessage:
    # API response detail message
    MESSAGE_NO_DATA_CRITERIA = 'No data found for the given criteria'


class APIErrorMessage:
    # API response error messages
    MESSAGE_ERROR_NOT_EXIST = 'Currency not exist'
    MESSAGE_ERROR_IS_ACTIVE_REQUIRED = 'Field is_active is required'
    MESSAGE_ERROR_IS_MONITORING_REQUIRED = 'Field is_monitoring is required'
    MESSAGE_ERROR_CURRENCY_ALREADY_ACTIVE = 'The currency is already active'
    MESSAGE_ERROR_CURRENCY_NOT_ACTIVE = 'The currency is not active'
    MESSAGE_ERROR_ACTIVE_NOT_ALLOWED = 'Field is_active not allowed'
    MESSAGE_ERROR_MONITORING_NOT_ALLOWED = 'Field is_monitoring not allowed'


class APISuccessMessage:
    # API response success messages
    MESSAGE_SUCCESS_CURRENCY_CHANGED = 'Currency changed'
