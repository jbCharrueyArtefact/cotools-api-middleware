class CustomBaseException(BaseException):
    def __init__(self, message, status_code, client):
        self.message = f"{message} from {client}"
        self.status_code = status_code
        self.client = client


class CustomProjectCreationException(CustomBaseException):
    def __init__(self, message, status_code):
        super().__init__(
            message=message, status_code=status_code, client="Project Creation"
        )


class CustomIamManagementError(CustomBaseException):
    def __init__(self, message, status_code):
        super().__init__(
            message=message, status_code=status_code, client="Iam Management"
        )


class CustomIamManagementException(CustomBaseException):
    def __init__(self, message):
        super().__init__(
            message=message, status_code=500, client="Iam Management"
        )


class CustomEssentialContactException(CustomBaseException):
    def __init__(self, message, status_code):
        super().__init__(
            message=message,
            status_code=status_code,
            client="Essential Contact",
        )


class CustomBillingClientException(CustomBaseException):
    def __init__(self, message, status_code):
        super().__init__(
            message=message, status_code=status_code, client="Billing"
        )


class CustomBigQueryClientException(CustomBaseException):
    def __init__(self, message, status_code):
        super().__init__(
            message=message, status_code=status_code, client="Big Query"
        )
