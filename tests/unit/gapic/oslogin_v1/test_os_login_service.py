# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import mock
import packaging.version

import grpc
from grpc.experimental import aio
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule


from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.oslogin_v1 import common  # type: ignore
from google.cloud.oslogin_v1.services.os_login_service import OsLoginServiceAsyncClient
from google.cloud.oslogin_v1.services.os_login_service import OsLoginServiceClient
from google.cloud.oslogin_v1.services.os_login_service import transports
from google.cloud.oslogin_v1.services.os_login_service.transports.base import (
    _API_CORE_VERSION,
)
from google.cloud.oslogin_v1.services.os_login_service.transports.base import (
    _GOOGLE_AUTH_VERSION,
)
from google.cloud.oslogin_v1.types import oslogin
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
import google.auth


# TODO(busunkim): Once google-api-core >= 1.26.0 is required:
# - Delete all the api-core and auth "less than" test cases
# - Delete these pytest markers (Make the "greater than or equal to" tests the default).
requires_google_auth_lt_1_25_0 = pytest.mark.skipif(
    packaging.version.parse(_GOOGLE_AUTH_VERSION) >= packaging.version.parse("1.25.0"),
    reason="This test requires google-auth < 1.25.0",
)
requires_google_auth_gte_1_25_0 = pytest.mark.skipif(
    packaging.version.parse(_GOOGLE_AUTH_VERSION) < packaging.version.parse("1.25.0"),
    reason="This test requires google-auth >= 1.25.0",
)

requires_api_core_lt_1_26_0 = pytest.mark.skipif(
    packaging.version.parse(_API_CORE_VERSION) >= packaging.version.parse("1.26.0"),
    reason="This test requires google-api-core < 1.26.0",
)

requires_api_core_gte_1_26_0 = pytest.mark.skipif(
    packaging.version.parse(_API_CORE_VERSION) < packaging.version.parse("1.26.0"),
    reason="This test requires google-api-core >= 1.26.0",
)


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert OsLoginServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        OsLoginServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        OsLoginServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        OsLoginServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        OsLoginServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        OsLoginServiceClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [OsLoginServiceClient, OsLoginServiceAsyncClient,]
)
def test_os_login_service_client_from_service_account_info(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "oslogin.googleapis.com:443"


@pytest.mark.parametrize(
    "client_class", [OsLoginServiceClient, OsLoginServiceAsyncClient,]
)
def test_os_login_service_client_from_service_account_file(client_class):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == "oslogin.googleapis.com:443"


def test_os_login_service_client_get_transport_class():
    transport = OsLoginServiceClient.get_transport_class()
    available_transports = [
        transports.OsLoginServiceGrpcTransport,
    ]
    assert transport in available_transports

    transport = OsLoginServiceClient.get_transport_class("grpc")
    assert transport == transports.OsLoginServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (OsLoginServiceClient, transports.OsLoginServiceGrpcTransport, "grpc"),
        (
            OsLoginServiceAsyncClient,
            transports.OsLoginServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    OsLoginServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(OsLoginServiceClient),
)
@mock.patch.object(
    OsLoginServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(OsLoginServiceAsyncClient),
)
def test_os_login_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(OsLoginServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=ga_credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(OsLoginServiceClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class()

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class()

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (OsLoginServiceClient, transports.OsLoginServiceGrpcTransport, "grpc", "true"),
        (
            OsLoginServiceAsyncClient,
            transports.OsLoginServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (OsLoginServiceClient, transports.OsLoginServiceGrpcTransport, "grpc", "false"),
        (
            OsLoginServiceAsyncClient,
            transports.OsLoginServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    OsLoginServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(OsLoginServiceClient),
)
@mock.patch.object(
    OsLoginServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(OsLoginServiceAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_os_login_service_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client.DEFAULT_ENDPOINT
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                with mock.patch(
                    "google.auth.transport.mtls.default_client_cert_source",
                    return_value=client_cert_source_callback,
                ):
                    if use_client_cert_env == "false":
                        expected_host = client.DEFAULT_ENDPOINT
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class()
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class()
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (OsLoginServiceClient, transports.OsLoginServiceGrpcTransport, "grpc"),
        (
            OsLoginServiceAsyncClient,
            transports.OsLoginServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_os_login_service_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(scopes=["1", "2"],)
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (OsLoginServiceClient, transports.OsLoginServiceGrpcTransport, "grpc"),
        (
            OsLoginServiceAsyncClient,
            transports.OsLoginServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_os_login_service_client_client_options_credentials_file(
    client_class, transport_class, transport_name
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_os_login_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.oslogin_v1.services.os_login_service.transports.OsLoginServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = OsLoginServiceClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_delete_posix_account(
    transport: str = "grpc", request_type=oslogin.DeletePosixAccountRequest
):
    client = OsLoginServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_posix_account), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_posix_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == oslogin.DeletePosixAccountRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_posix_account_from_dict():
    test_delete_posix_account(request_type=dict)


def test_delete_posix_account_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = OsLoginServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_posix_account), "__call__"
    ) as call:
        client.delete_posix_account()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == oslogin.DeletePosixAccountRequest()


@pytest.mark.asyncio
async def test_delete_posix_account_async(
    transport: str = "grpc_asyncio", request_type=oslogin.DeletePosixAccountRequest
):
    client = OsLoginServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_posix_account), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_posix_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == oslogin.DeletePosixAccountRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_posix_account_async_from_dict():
    await test_delete_posix_account_async(request_type=dict)


def test_delete_posix_account_field_headers():
    client = OsLoginServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oslogin.DeletePosixAccountRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_posix_account), "__call__"
    ) as call:
        call.return_value = None
        client.delete_posix_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_posix_account_field_headers_async():
    client = OsLoginServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oslogin.DeletePosixAccountRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_posix_account), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_posix_account(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_posix_account_flattened():
    client = OsLoginServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_posix_account), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_posix_account(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_posix_account_flattened_error():
    client = OsLoginServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_posix_account(
            oslogin.DeletePosixAccountRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_posix_account_flattened_async():
    client = OsLoginServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_posix_account), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_posix_account(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_posix_account_flattened_error_async():
    client = OsLoginServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_posix_account(
            oslogin.DeletePosixAccountRequest(), name="name_value",
        )


def test_delete_ssh_public_key(
    transport: str = "grpc", request_type=oslogin.DeleteSshPublicKeyRequest
):
    client = OsLoginServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_ssh_public_key), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        response = client.delete_ssh_public_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == oslogin.DeleteSshPublicKeyRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_ssh_public_key_from_dict():
    test_delete_ssh_public_key(request_type=dict)


def test_delete_ssh_public_key_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = OsLoginServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_ssh_public_key), "__call__"
    ) as call:
        client.delete_ssh_public_key()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == oslogin.DeleteSshPublicKeyRequest()


@pytest.mark.asyncio
async def test_delete_ssh_public_key_async(
    transport: str = "grpc_asyncio", request_type=oslogin.DeleteSshPublicKeyRequest
):
    client = OsLoginServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_ssh_public_key), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        response = await client.delete_ssh_public_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == oslogin.DeleteSshPublicKeyRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_ssh_public_key_async_from_dict():
    await test_delete_ssh_public_key_async(request_type=dict)


def test_delete_ssh_public_key_field_headers():
    client = OsLoginServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oslogin.DeleteSshPublicKeyRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_ssh_public_key), "__call__"
    ) as call:
        call.return_value = None
        client.delete_ssh_public_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_ssh_public_key_field_headers_async():
    client = OsLoginServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oslogin.DeleteSshPublicKeyRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_ssh_public_key), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        await client.delete_ssh_public_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_ssh_public_key_flattened():
    client = OsLoginServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_ssh_public_key), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_ssh_public_key(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_ssh_public_key_flattened_error():
    client = OsLoginServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_ssh_public_key(
            oslogin.DeleteSshPublicKeyRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_ssh_public_key_flattened_async():
    client = OsLoginServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_ssh_public_key), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_ssh_public_key(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_ssh_public_key_flattened_error_async():
    client = OsLoginServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_ssh_public_key(
            oslogin.DeleteSshPublicKeyRequest(), name="name_value",
        )


def test_get_login_profile(
    transport: str = "grpc", request_type=oslogin.GetLoginProfileRequest
):
    client = OsLoginServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_login_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oslogin.LoginProfile(name="name_value",)
        response = client.get_login_profile(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == oslogin.GetLoginProfileRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, oslogin.LoginProfile)
    assert response.name == "name_value"


def test_get_login_profile_from_dict():
    test_get_login_profile(request_type=dict)


def test_get_login_profile_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = OsLoginServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_login_profile), "__call__"
    ) as call:
        client.get_login_profile()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == oslogin.GetLoginProfileRequest()


@pytest.mark.asyncio
async def test_get_login_profile_async(
    transport: str = "grpc_asyncio", request_type=oslogin.GetLoginProfileRequest
):
    client = OsLoginServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_login_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oslogin.LoginProfile(name="name_value",)
        )
        response = await client.get_login_profile(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == oslogin.GetLoginProfileRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, oslogin.LoginProfile)
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_get_login_profile_async_from_dict():
    await test_get_login_profile_async(request_type=dict)


def test_get_login_profile_field_headers():
    client = OsLoginServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oslogin.GetLoginProfileRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_login_profile), "__call__"
    ) as call:
        call.return_value = oslogin.LoginProfile()
        client.get_login_profile(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_login_profile_field_headers_async():
    client = OsLoginServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oslogin.GetLoginProfileRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_login_profile), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oslogin.LoginProfile()
        )
        await client.get_login_profile(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_login_profile_flattened():
    client = OsLoginServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_login_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oslogin.LoginProfile()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_login_profile(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_login_profile_flattened_error():
    client = OsLoginServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_login_profile(
            oslogin.GetLoginProfileRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_login_profile_flattened_async():
    client = OsLoginServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_login_profile), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oslogin.LoginProfile()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oslogin.LoginProfile()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_login_profile(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_login_profile_flattened_error_async():
    client = OsLoginServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_login_profile(
            oslogin.GetLoginProfileRequest(), name="name_value",
        )


def test_get_ssh_public_key(
    transport: str = "grpc", request_type=oslogin.GetSshPublicKeyRequest
):
    client = OsLoginServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_ssh_public_key), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = common.SshPublicKey(
            key="key_value",
            expiration_time_usec=2144,
            fingerprint="fingerprint_value",
            name="name_value",
        )
        response = client.get_ssh_public_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == oslogin.GetSshPublicKeyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, common.SshPublicKey)
    assert response.key == "key_value"
    assert response.expiration_time_usec == 2144
    assert response.fingerprint == "fingerprint_value"
    assert response.name == "name_value"


def test_get_ssh_public_key_from_dict():
    test_get_ssh_public_key(request_type=dict)


def test_get_ssh_public_key_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = OsLoginServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_ssh_public_key), "__call__"
    ) as call:
        client.get_ssh_public_key()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == oslogin.GetSshPublicKeyRequest()


@pytest.mark.asyncio
async def test_get_ssh_public_key_async(
    transport: str = "grpc_asyncio", request_type=oslogin.GetSshPublicKeyRequest
):
    client = OsLoginServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_ssh_public_key), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            common.SshPublicKey(
                key="key_value",
                expiration_time_usec=2144,
                fingerprint="fingerprint_value",
                name="name_value",
            )
        )
        response = await client.get_ssh_public_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == oslogin.GetSshPublicKeyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, common.SshPublicKey)
    assert response.key == "key_value"
    assert response.expiration_time_usec == 2144
    assert response.fingerprint == "fingerprint_value"
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_get_ssh_public_key_async_from_dict():
    await test_get_ssh_public_key_async(request_type=dict)


def test_get_ssh_public_key_field_headers():
    client = OsLoginServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oslogin.GetSshPublicKeyRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_ssh_public_key), "__call__"
    ) as call:
        call.return_value = common.SshPublicKey()
        client.get_ssh_public_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_ssh_public_key_field_headers_async():
    client = OsLoginServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oslogin.GetSshPublicKeyRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_ssh_public_key), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(common.SshPublicKey())
        await client.get_ssh_public_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_ssh_public_key_flattened():
    client = OsLoginServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_ssh_public_key), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = common.SshPublicKey()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_ssh_public_key(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_ssh_public_key_flattened_error():
    client = OsLoginServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_ssh_public_key(
            oslogin.GetSshPublicKeyRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_ssh_public_key_flattened_async():
    client = OsLoginServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.get_ssh_public_key), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = common.SshPublicKey()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(common.SshPublicKey())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_ssh_public_key(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_ssh_public_key_flattened_error_async():
    client = OsLoginServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_ssh_public_key(
            oslogin.GetSshPublicKeyRequest(), name="name_value",
        )


def test_import_ssh_public_key(
    transport: str = "grpc", request_type=oslogin.ImportSshPublicKeyRequest
):
    client = OsLoginServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_ssh_public_key), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oslogin.ImportSshPublicKeyResponse()
        response = client.import_ssh_public_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == oslogin.ImportSshPublicKeyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, oslogin.ImportSshPublicKeyResponse)


def test_import_ssh_public_key_from_dict():
    test_import_ssh_public_key(request_type=dict)


def test_import_ssh_public_key_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = OsLoginServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_ssh_public_key), "__call__"
    ) as call:
        client.import_ssh_public_key()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == oslogin.ImportSshPublicKeyRequest()


@pytest.mark.asyncio
async def test_import_ssh_public_key_async(
    transport: str = "grpc_asyncio", request_type=oslogin.ImportSshPublicKeyRequest
):
    client = OsLoginServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_ssh_public_key), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oslogin.ImportSshPublicKeyResponse()
        )
        response = await client.import_ssh_public_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == oslogin.ImportSshPublicKeyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, oslogin.ImportSshPublicKeyResponse)


@pytest.mark.asyncio
async def test_import_ssh_public_key_async_from_dict():
    await test_import_ssh_public_key_async(request_type=dict)


def test_import_ssh_public_key_field_headers():
    client = OsLoginServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oslogin.ImportSshPublicKeyRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_ssh_public_key), "__call__"
    ) as call:
        call.return_value = oslogin.ImportSshPublicKeyResponse()
        client.import_ssh_public_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_import_ssh_public_key_field_headers_async():
    client = OsLoginServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oslogin.ImportSshPublicKeyRequest()

    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_ssh_public_key), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oslogin.ImportSshPublicKeyResponse()
        )
        await client.import_ssh_public_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_import_ssh_public_key_flattened():
    client = OsLoginServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_ssh_public_key), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oslogin.ImportSshPublicKeyResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.import_ssh_public_key(
            parent="parent_value",
            ssh_public_key=common.SshPublicKey(key="key_value"),
            project_id="project_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].ssh_public_key == common.SshPublicKey(key="key_value")
        assert args[0].project_id == "project_id_value"


def test_import_ssh_public_key_flattened_error():
    client = OsLoginServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.import_ssh_public_key(
            oslogin.ImportSshPublicKeyRequest(),
            parent="parent_value",
            ssh_public_key=common.SshPublicKey(key="key_value"),
            project_id="project_id_value",
        )


@pytest.mark.asyncio
async def test_import_ssh_public_key_flattened_async():
    client = OsLoginServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.import_ssh_public_key), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = oslogin.ImportSshPublicKeyResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            oslogin.ImportSshPublicKeyResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.import_ssh_public_key(
            parent="parent_value",
            ssh_public_key=common.SshPublicKey(key="key_value"),
            project_id="project_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].ssh_public_key == common.SshPublicKey(key="key_value")
        assert args[0].project_id == "project_id_value"


@pytest.mark.asyncio
async def test_import_ssh_public_key_flattened_error_async():
    client = OsLoginServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.import_ssh_public_key(
            oslogin.ImportSshPublicKeyRequest(),
            parent="parent_value",
            ssh_public_key=common.SshPublicKey(key="key_value"),
            project_id="project_id_value",
        )


def test_update_ssh_public_key(
    transport: str = "grpc", request_type=oslogin.UpdateSshPublicKeyRequest
):
    client = OsLoginServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_ssh_public_key), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = common.SshPublicKey(
            key="key_value",
            expiration_time_usec=2144,
            fingerprint="fingerprint_value",
            name="name_value",
        )
        response = client.update_ssh_public_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == oslogin.UpdateSshPublicKeyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, common.SshPublicKey)
    assert response.key == "key_value"
    assert response.expiration_time_usec == 2144
    assert response.fingerprint == "fingerprint_value"
    assert response.name == "name_value"


def test_update_ssh_public_key_from_dict():
    test_update_ssh_public_key(request_type=dict)


def test_update_ssh_public_key_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = OsLoginServiceClient(
        credentials=ga_credentials.AnonymousCredentials(), transport="grpc",
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_ssh_public_key), "__call__"
    ) as call:
        client.update_ssh_public_key()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == oslogin.UpdateSshPublicKeyRequest()


@pytest.mark.asyncio
async def test_update_ssh_public_key_async(
    transport: str = "grpc_asyncio", request_type=oslogin.UpdateSshPublicKeyRequest
):
    client = OsLoginServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_ssh_public_key), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            common.SshPublicKey(
                key="key_value",
                expiration_time_usec=2144,
                fingerprint="fingerprint_value",
                name="name_value",
            )
        )
        response = await client.update_ssh_public_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == oslogin.UpdateSshPublicKeyRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, common.SshPublicKey)
    assert response.key == "key_value"
    assert response.expiration_time_usec == 2144
    assert response.fingerprint == "fingerprint_value"
    assert response.name == "name_value"


@pytest.mark.asyncio
async def test_update_ssh_public_key_async_from_dict():
    await test_update_ssh_public_key_async(request_type=dict)


def test_update_ssh_public_key_field_headers():
    client = OsLoginServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oslogin.UpdateSshPublicKeyRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_ssh_public_key), "__call__"
    ) as call:
        call.return_value = common.SshPublicKey()
        client.update_ssh_public_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_ssh_public_key_field_headers_async():
    client = OsLoginServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = oslogin.UpdateSshPublicKeyRequest()

    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_ssh_public_key), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(common.SshPublicKey())
        await client.update_ssh_public_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_update_ssh_public_key_flattened():
    client = OsLoginServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_ssh_public_key), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = common.SshPublicKey()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_ssh_public_key(
            name="name_value",
            ssh_public_key=common.SshPublicKey(key="key_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].ssh_public_key == common.SshPublicKey(key="key_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


def test_update_ssh_public_key_flattened_error():
    client = OsLoginServiceClient(credentials=ga_credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_ssh_public_key(
            oslogin.UpdateSshPublicKeyRequest(),
            name="name_value",
            ssh_public_key=common.SshPublicKey(key="key_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_ssh_public_key_flattened_async():
    client = OsLoginServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_ssh_public_key), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = common.SshPublicKey()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(common.SshPublicKey())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_ssh_public_key(
            name="name_value",
            ssh_public_key=common.SshPublicKey(key="key_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"
        assert args[0].ssh_public_key == common.SshPublicKey(key="key_value")
        assert args[0].update_mask == field_mask_pb2.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_ssh_public_key_flattened_error_async():
    client = OsLoginServiceAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_ssh_public_key(
            oslogin.UpdateSshPublicKeyRequest(),
            name="name_value",
            ssh_public_key=common.SshPublicKey(key="key_value"),
            update_mask=field_mask_pb2.FieldMask(paths=["paths_value"]),
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.OsLoginServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = OsLoginServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.OsLoginServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = OsLoginServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.OsLoginServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = OsLoginServiceClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.OsLoginServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = OsLoginServiceClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.OsLoginServiceGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.OsLoginServiceGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.OsLoginServiceGrpcTransport,
        transports.OsLoginServiceGrpcAsyncIOTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, "default") as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = OsLoginServiceClient(credentials=ga_credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.OsLoginServiceGrpcTransport,)


def test_os_login_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.OsLoginServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_os_login_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.oslogin_v1.services.os_login_service.transports.OsLoginServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.OsLoginServiceTransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "delete_posix_account",
        "delete_ssh_public_key",
        "get_login_profile",
        "get_ssh_public_key",
        "import_ssh_public_key",
        "update_ssh_public_key",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


@requires_google_auth_gte_1_25_0
def test_os_login_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.oslogin_v1.services.os_login_service.transports.OsLoginServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.OsLoginServiceTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/compute",
            ),
            quota_project_id="octopus",
        )


@requires_google_auth_lt_1_25_0
def test_os_login_service_base_transport_with_credentials_file_old_google_auth():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch(
        "google.cloud.oslogin_v1.services.os_login_service.transports.OsLoginServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.OsLoginServiceTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/compute",
            ),
            quota_project_id="octopus",
        )


def test_os_login_service_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch(
        "google.cloud.oslogin_v1.services.os_login_service.transports.OsLoginServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.OsLoginServiceTransport()
        adc.assert_called_once()


@requires_google_auth_gte_1_25_0
def test_os_login_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        OsLoginServiceClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/compute",
            ),
            quota_project_id=None,
        )


@requires_google_auth_lt_1_25_0
def test_os_login_service_auth_adc_old_google_auth():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        OsLoginServiceClient()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/compute",
            ),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.OsLoginServiceGrpcTransport,
        transports.OsLoginServiceGrpcAsyncIOTransport,
    ],
)
@requires_google_auth_gte_1_25_0
def test_os_login_service_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/compute",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.OsLoginServiceGrpcTransport,
        transports.OsLoginServiceGrpcAsyncIOTransport,
    ],
)
@requires_google_auth_lt_1_25_0
def test_os_login_service_transport_auth_adc_old_google_auth(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus")
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/compute",
            ),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.OsLoginServiceGrpcTransport, grpc_helpers),
        (transports.OsLoginServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
@requires_api_core_gte_1_26_0
def test_os_login_service_transport_create_channel(transport_class, grpc_helpers):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])

        create_channel.assert_called_with(
            "oslogin.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/compute",
            ),
            scopes=["1", "2"],
            default_host="oslogin.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.OsLoginServiceGrpcTransport, grpc_helpers),
        (transports.OsLoginServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
@requires_api_core_lt_1_26_0
def test_os_login_service_transport_create_channel_old_api_core(
    transport_class, grpc_helpers
):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(quota_project_id="octopus")

        create_channel.assert_called_with(
            "oslogin.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/compute",
            ),
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.OsLoginServiceGrpcTransport, grpc_helpers),
        (transports.OsLoginServiceGrpcAsyncIOTransport, grpc_helpers_async),
    ],
)
@requires_api_core_lt_1_26_0
def test_os_login_service_transport_create_channel_user_scopes(
    transport_class, grpc_helpers
):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)

        transport_class(quota_project_id="octopus", scopes=["1", "2"])

        create_channel.assert_called_with(
            "oslogin.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            scopes=["1", "2"],
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.OsLoginServiceGrpcTransport,
        transports.OsLoginServiceGrpcAsyncIOTransport,
    ],
)
def test_os_login_service_grpc_transport_client_cert_source_for_mtls(transport_class):
    cred = ga_credentials.AnonymousCredentials()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds,
        )
        mock_create_channel.assert_called_once_with(
            "squid.clam.whelk:443",
            credentials=cred,
            credentials_file=None,
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/compute",
            ),
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

    # Check if ssl_channel_credentials is not provided, then client_cert_source_for_mtls
    # is used.
    with mock.patch.object(transport_class, "create_channel", return_value=mock.Mock()):
        with mock.patch("grpc.ssl_channel_credentials") as mock_ssl_cred:
            transport_class(
                credentials=cred,
                client_cert_source_for_mtls=client_cert_source_callback,
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert, private_key=expected_key
            )


def test_os_login_service_host_no_port():
    client = OsLoginServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="oslogin.googleapis.com"
        ),
    )
    assert client.transport._host == "oslogin.googleapis.com:443"


def test_os_login_service_host_with_port():
    client = OsLoginServiceClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="oslogin.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "oslogin.googleapis.com:8000"


def test_os_login_service_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.OsLoginServiceGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_os_login_service_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.OsLoginServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.OsLoginServiceGrpcTransport,
        transports.OsLoginServiceGrpcAsyncIOTransport,
    ],
)
def test_os_login_service_transport_channel_mtls_with_client_cert_source(
    transport_class,
):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = ga_credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=(
                    "https://www.googleapis.com/auth/cloud-platform",
                    "https://www.googleapis.com/auth/compute",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize(
    "transport_class",
    [
        transports.OsLoginServiceGrpcTransport,
        transports.OsLoginServiceGrpcAsyncIOTransport,
    ],
)
def test_os_login_service_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=(
                    "https://www.googleapis.com/auth/cloud-platform",
                    "https://www.googleapis.com/auth/compute",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_posix_account_path():
    user = "squid"
    project = "clam"
    expected = "users/{user}/projects/{project}".format(user=user, project=project,)
    actual = OsLoginServiceClient.posix_account_path(user, project)
    assert expected == actual


def test_parse_posix_account_path():
    expected = {
        "user": "whelk",
        "project": "octopus",
    }
    path = OsLoginServiceClient.posix_account_path(**expected)

    # Check that the path construction is reversible.
    actual = OsLoginServiceClient.parse_posix_account_path(path)
    assert expected == actual


def test_ssh_public_key_path():
    user = "oyster"
    fingerprint = "nudibranch"
    expected = "users/{user}/sshPublicKeys/{fingerprint}".format(
        user=user, fingerprint=fingerprint,
    )
    actual = OsLoginServiceClient.ssh_public_key_path(user, fingerprint)
    assert expected == actual


def test_parse_ssh_public_key_path():
    expected = {
        "user": "cuttlefish",
        "fingerprint": "mussel",
    }
    path = OsLoginServiceClient.ssh_public_key_path(**expected)

    # Check that the path construction is reversible.
    actual = OsLoginServiceClient.parse_ssh_public_key_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "winkle"
    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = OsLoginServiceClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nautilus",
    }
    path = OsLoginServiceClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = OsLoginServiceClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "scallop"
    expected = "folders/{folder}".format(folder=folder,)
    actual = OsLoginServiceClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "abalone",
    }
    path = OsLoginServiceClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = OsLoginServiceClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "squid"
    expected = "organizations/{organization}".format(organization=organization,)
    actual = OsLoginServiceClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "clam",
    }
    path = OsLoginServiceClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = OsLoginServiceClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "whelk"
    expected = "projects/{project}".format(project=project,)
    actual = OsLoginServiceClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "octopus",
    }
    path = OsLoginServiceClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = OsLoginServiceClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "oyster"
    location = "nudibranch"
    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = OsLoginServiceClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "cuttlefish",
        "location": "mussel",
    }
    path = OsLoginServiceClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = OsLoginServiceClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.OsLoginServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = OsLoginServiceClient(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.OsLoginServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = OsLoginServiceClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
