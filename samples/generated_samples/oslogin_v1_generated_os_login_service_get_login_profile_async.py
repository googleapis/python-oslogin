# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
# Generated code. DO NOT EDIT!
#
# Snippet for GetLoginProfile
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-oslogin


# [START oslogin_v1_generated_OsLoginService_GetLoginProfile_async]
from google.cloud import oslogin_v1


async def sample_get_login_profile():
    # Create a client
    client = oslogin_v1.OsLoginServiceAsyncClient()

    # Initialize request argument(s)
    request = oslogin_v1.GetLoginProfileRequest(
        name="name_value",
    )

    # Make the request
    response = await client.get_login_profile(request=request)

    # Handle the response
    print(response)

# [END oslogin_v1_generated_OsLoginService_GetLoginProfile_async]