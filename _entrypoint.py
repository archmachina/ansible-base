#!/usr/bin/env python3

import os

import build_tool
from build_tool import action, bash, Util

REGISTRY_IMAGE = "archmachina/ansible-base"
REGISTRY_HOST = "docker.io"
REGISTRY_USER = "archmachina"

# Build Session
bs = build_tool.BuildSession([f"0.1.0-rolling+{Util.git_sha()}"])

# Container Session
cs = build_tool.ContainerSession(REGISTRY_IMAGE, "src/Dockerfile", "src")

# Testing Session
ts = build_tool.TestingSession([
    "dfbar -f ./src/Dockerfile -m test ./src"
])

# Linting Session
ls = build_tool.LintingSession([
    "docker run --rm -i hadolint/hadolint < ./src/Dockerfile"
])

def push_image():
    # Push image to registry
    cs.login(REGISTRY_HOST, REGISTRY_USER, os.environ["REGISTRY_TOKEN"])
    cs.push()

@action
def test():
    ts.run()

@action
def lint():
    ls.run()

@action
def clean():
    bash(f"docker image rm {REGISTRY_IMAGE} --force", ignore_rc=True)

@action
def build():

    cs.build_args.append(f"VERSION={bs.v_full}")
    cs.build()

@action
def pr_main():

    # pr to main just does a build and test
    build()
    test()

@action
def push_main():

    # Commits to main update the registry image main and latest tags
    cs.tags = ["main", "latest"]

    # Build and test
    build()
    test()

    # Push image and tags to registry
    push_image()

@action
def release():

    # Make sure we have a github version
    ref = os.environ.get("GITHUB_REF", "")
    if ref == "":
        Util.fail("Missing github version reference")

    # Update based on github reference
    bs.update_version([ref])

    # Determine docker image tags and build
    cs.tags = [
        bs.v_major,
        f"{bs.v_major}.{bs.v_minor}",
        f"{bs.v_major}.{bs.v_minor}.{bs.v_patch}",
    ]

    # Build and test
    build()
    test()

    # Push image and tags to registry
    push_image()

    # Create a github release for this tag
    Util.github_release(
        bs.v_stripped,
        name=f"Version {bs.v_full}",
        prerelease=bs.v_is_prerelease,
        github_token=os.environ["GITHUB_TOKEN"],
        repo=os.environ["GITHUB_REPOSITORY"],
    )


# run_action will run the action and also control the exit of
# the process (i.e. does not return)
build_tool.configure_logging(debug=True)
build_tool.run_action()
