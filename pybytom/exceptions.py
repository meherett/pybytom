#!/usr/bin/env python
# coding=utf-8

from dataclasses import dataclass


@dataclass()
class ClientError(Exception):
    error_message: str
    error_detail: str = None

    def __str__(self):
        if self.error_detail:
            return f"{self.error_message}, {self.error_detail}"
        else:
            return f"{self.error_message}"


@dataclass()
class APIError(Exception):
    error_message: str
    status_code: int = None

    def __str__(self):
        if self.status_code:
            return f"({self.status_code}), {self.error_message}"
        else:
            return f"{self.error_message}"


@dataclass()
class InvalidURLError(Exception):
    error_message: str

    def __str__(self):
        return f"{self.error_message}"


@dataclass()
class NotFoundError(Exception):
    error_message: str
    error_detail: str = None

    def __str__(self):
        if self.error_detail:
            return f"{self.error_message}, {self.error_detail}"
        else:
            return f"{self.error_message}"


@dataclass()
class AddressError(Exception):
    error_message: str
    error_detail: str = None

    def __str__(self):
        if self.error_detail:
            return f"{self.error_message}, {self.error_detail}"
        return f"{self.error_message}"


@dataclass()
class BalanceError(Exception):
    error_message: str
    error_detail: str = None

    def __str__(self):
        if self.error_detail:
            return f"{self.error_message}, {self.error_detail}"
        return f"{self.error_message}"


@dataclass()
class NetworkError(Exception):
    error_message: str
    error_detail: str = None

    def __str__(self):
        if self.error_detail:
            return f"{self.error_message}, {self.error_detail}"
        return f"{self.error_message}"
