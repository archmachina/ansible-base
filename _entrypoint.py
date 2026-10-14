#!/usr/bin/env python3

import os

import build_tool
from build_tool import action, bash, Util

IMAGE = "archmachina/ansible-base"

# Build Session
bs = build_tool.BuildSession([f"0.1.0-rolling+{Util.git_sha()}"])

# Container Session
cs = build_tool.ContainerSession(IMAGE)
cs.docker_file = "src/Dockerfile"
cs.container_dir = "src"

# Testing Session
ts = build_tool.TestingSession([
    "dfbar -f ./src/Dockerfile -m test ./src"
])

# Linting Session
ls = build_tool.LintingSession([
    "docker run --rm -i hadolint/hadolint < ./src/Dockerfile"
])

@action
def test():
    ts.run()

@action
def lint():
    ls.run()

@action
def build():
    cs.build()

@action
def pr_branch_main():

    # pr to main just does a build and test
    build()
    test()

@action
def push_branch_main():

    # Push to main branch should have a rolling version number
    # based on the sha
    cs.build_args = [f"VERSION=0.1.0-rolling+{Util.git_sha()}"]
    cs.tags = ["main", "latest"]
    build()

    # Make sure tests pass for main
    test()

    # Pushes to main become the 'latest' tag for the docker image
    cs.login("docker.io", "archmachina", os.environ["DOCKER_HUB_TOKEN"])
    cs.push()

@action
def push_tag_v():

    # Make sure we have a github version
    ref = os.environ.get("GITHUB_REF", "")
    if ref == "":
        Util.fail("Missing github version reference")

    # Update based on github reference
    bs.update_version([ref])

    # Determine docker image tags and build
    cs.build_args = [f"VERSION={bs.v_full}"]
    cs.tags = [
        bs.v_major,
        f"{bs.v_major}.{bs.v_minor}",
        f"{bs.v_major}.{bs.v_minor}.{bs.v_patch}",
    ]
    build()

    # Push image to docker hub
    cs.login("docker.io", "archmachina", os.environ["DOCKER_HUB_TOKEN"])
    cs.push()

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
