import pkg_resources

package_version = pkg_resources.get_distribution(
    "azure-ai-vision-imageanalysis"
).version
print(package_version)

import sys

print(sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
