#!/usr/bin/env python
# coding=utf-8


class ClientError(Exception):

    def __init__(self, error_message, error_detail=None):
        self.error_message = error_message
        self.error_detail = error_detail

    def __str__(self):
        if self.error_detail:
            return f"{self.error_message}, {self.error_detail}"
        else:
            return f"{self.error_message}"


class APIError(Exception):

    def __init__(self, error_message, status_code=None):
        self.status_code = status_code
        self.error_message = error_message

    def __str__(self):
        if self.status_code:
            return f"({self.status_code}), {self.error_message}"
        else:
            return f"{self.error_message}"


class InvalidURLError(Exception):

    def __init__(self, error_message):
        self.error_message = error_message

    def __str__(self):
        return f"{self.error_message}"


class NotFoundError(Exception):

    def __init__(self, error_message, error_detail=None):
        self.error_message = error_message
        self.error_detail = error_detail

    def __str__(self):
        if self.error_detail:
            return f"{self.error_message}, {self.error_detail}"
        else:
            return f"{self.error_message}"


class AddressError(Exception):

    def __init__(self, error_message, error_detail=None):
        self.error_message = error_message
        self.error_detail = error_detail

    def __str__(self):
        if self.error_detail:
            return f"{self.error_message}, {self.error_detail}"
        return f"{self.error_message}"


class BalanceError(Exception):

    def __init__(self, error_message, error_detail=None):
        self.error_message = error_message
        self.error_detail = error_detail

    def __str__(self):
        if self.error_detail:
            return f"{self.error_message}, {self.error_detail}"
        return f"{self.error_message}"


class SymbolError(Exception):

    def __init__(self, error_message, error_detail=None):
        self.error_message = error_message
        self.error_detail = error_detail

    def __str__(self):
        if self.error_detail:
            return f"{self.error_message}, {self.error_detail}"
        return f"{self.error_message}"


class DerivationError(Exception):

    def __init__(self, error_message, error_detail=None):
        self.error_message = error_message
        self.error_detail = error_detail

    def __str__(self):
        if self.error_detail:
            return f"{self.error_message}, {self.error_detail}"
        return f"{self.error_message}"


class NetworkError(Exception):

    def __init__(self, error_message, error_detail=None):
        self.error_message = error_message
        self.error_detail = error_detail

    def __str__(self):
        if self.error_detail:
            return f"{self.error_message}, {self.error_detail}"
        return f"{self.error_message}"
