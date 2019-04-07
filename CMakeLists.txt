# ------------------------------------------------------------------------------
# cmake settings
# ------------------------------------------------------------------------------
cmake_minimum_required (VERSION 2.6)

# ------------------------------------------------------------------------------
# project settings
# ------------------------------------------------------------------------------
project(fitness)
set(PROJECT_VERSION 0.0.0)


# ------------------------------------------------------------------------------
# install
# ------------------------------------------------------------------------------
# executables
install(
    DIRECTORY ./bin
    DESTINATION $ENV{RELEASE}/${PROJECT_NAME}/${PROJECT_VERSION}
    PATTERN "*"
    PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE
)

# python libraries
install(
    DIRECTORY ./python
    DESTINATION $ENV{RELEASE}/${PROJECT_NAME}/${PROJECT_VERSION}
    REGEX ".*.py"
    REGEX ".*.py[cod]|.*.DS_Store*" EXCLUDE
    PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE
)

# configuration files
install(
    DIRECTORY ./configs
    DESTINATION $ENV{RELEASE}/${PROJECT_NAME}/${PROJECT_VERSION}
    REGEX ".*"
    REGEX ".*.DS_Store*" EXCLUDE
    PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE
)

# template files
install(
    DIRECTORY ./templates
    DESTINATION $ENV{RELEASE}/${PROJECT_NAME}/${PROJECT_VERSION}
    REGEX ".*"
    REGEX ".*.DS_Store*" EXCLUDE
    PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE
)