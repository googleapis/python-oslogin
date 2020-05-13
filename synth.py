# Copyright 2018 Google LLC
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

"""This script is used to synthesize generated parts of this library."""
import synthtool as s
from synthtool import gcp

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Generate oslogin GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    service="oslogin",
    version="v1",
    bazel_target="//google/cloud/oslogin/v1:oslogin-v1-py",
    include_protos=True,
)
# pb2's are incorrectly generated into deeper directories, so copy separately into proto/
s.move(
    library,
    excludes=[
        "nox.py",
        "setup.py",
        "README.rst",
        "docs/index.rst",
        library / "google/cloud/oslogin_v1/proto/oslogin/**",
        library / "google/cloud/oslogin_v1/proto/oslogin_v1/**",
    ],
)
s.move(library / "google/cloud/oslogin_v1/proto/**/*.py", "google/cloud/oslogin_v1/proto")
s.move(library / "google/cloud/oslogin/common/**/*.py", "google/cloud/oslogin_v1/proto")

s.replace(
    "google/cloud/oslogin_v1/gapic/os_login_service_client.py",
    "google-cloud-oslogin",
    "google-cloud-os-login",
)

# Fix up imports
s.replace(
    "google/**/proto/*.py",
    "from google.cloud.oslogin.common import common_pb2",
    "from google.cloud.oslogin_v1.proto import common_pb2",
)

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(cov_level=70)
s.move(templated_files)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
