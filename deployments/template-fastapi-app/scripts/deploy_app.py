#!/usr/bin/env python3
import os
import subprocess
import sys
import shlex
import argparse

# Registry and path to push the docker image
HARBOR_REGISTRY = "http://192.168.0.62:30002"
HARBOR_PATH = "library/template-fastapi-app"

# Path from this scripts location to the docker context
PATH_TO_DOCKER_DIR = "../docker"

# Path from this script to file which will house the pushed image´s tree hash.
PATH_TO_KUSTOMIZATION_FILE = "../kubernetes/kustomization.yaml"

# Remote branch where the amended & updated image´s tree hash will be and pushed
CURRENT_WORKING_REMOTE_BRANCH = "main"


def prompt_user(prompt):
    response = input(prompt).strip().lower()
    return response in ['yes', 'y']


def print_colored(text, color, end='\n'):
    colors = {'red': '\x1b[31m', 'green': '\x1b[32m', 'yellow': '\x1b[33m', 'blue': '\x1b[34m'}
    reset = '\x1b[0m'
    sys.stdout.write(colors.get(color, '') + text + reset + end)


def run_cmd(command, capture_output=False, check=True, print_cmd=False, shell=False):
    """
    Runs a command using subprocess.run.

    Args:
        command (str): The command to run.
        capture_output (bool): If True, capture the command's output.
        check (bool): If True, raise an exception if the command fails.
        print_cmd (bool): If True, print the command before running it.
        shell (bool): If True, run the command in the shell environment.

    Returns:
        str: The command's output if capture_output is True.
        int: The command's return code if capture_output is False.
    """
    if print_cmd:
        print_colored(f"Running: {command}", color="green")

    result = subprocess.run(
        command if shell else shlex.split(command),
        stdout=subprocess.PIPE if capture_output else None,
        stderr=subprocess.PIPE,
        check=check,
        shell=shell  # Allow running commands that use shell features
    )

    if capture_output:
        return result.stdout.decode().strip(), result.stderr.decode().strip()

    return result.returncode


def print_script_information():
    print(" -- To quiet informational prints, pass in -q")
    print("\n\n..")
    print("This is a simple helper script that helps with building and pushing an image of the application to harbor.")
    print("")

def print_dirty_image_warning():
    print("WARNING - It seems like you want to build a Docker image on code which has uncommitted.")
    print("The code in the uncommitted changes will be used in the docker image,")
    print("but unless you commit and push this uncommited code the changes wont be visible in the repo.")
    print("This becomes problematic as there would be a mismatch in the 'running' and the 'stored' code.")
    print("If you choose to continue, the image will be marked as '-dirty' on harbor")


def print_harbor_login_information():
    print("\n" * 3)
    print("Pushing the generated docker image to harbor failed.")
    print("The script tried logging you in automatically but that failed aswell.")
    print("If the error is regarding beeing denied due to permissions, you may have to log in to harbor again.")
    print("You can do so like using this command:")
    print(f"docker login {HARBOR_REGISTRY}")
    print("Then enter your credentials as you would in harbor.")


def print_kustomization_and_image_information(destination_and_tag_name):
    print("Built images and pushed to harbor")
    print("image pushed: " + destination_and_tag_name)
    print("The new tag has been put in the kustomization file")
    print("\n\n")
    print("The new tag in the kustomization file must now be commited and pushed.")


def print_commit_tree_hash_reminder_information():
    print("\n" * 2)
    print("! Now commit and push the modified kustomization.yaml file (important)")
    print(" Important beacuse we want to be able to track which image is currently in use through the repository.")
    print("")


def main():
    parser = argparse.ArgumentParser(
        description="Script to build and push Docker images.")
    parser.add_argument('-q', '--quiet', action='store_true',
                        help="Run script in quiet mode.")
    args = parser.parse_args()

    quiet_mode = args.quiet

    # Move to the docker directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    docker_dir = os.path.join(script_dir, PATH_TO_DOCKER_DIR)
    os.chdir(docker_dir)

    if not quiet_mode:
        print_script_information()

    commit_hash, _ = run_cmd("git rev-parse HEAD:./", capture_output=True)
    tag = f"tree-{commit_hash}"
    if run_cmd("git diff --quiet HEAD ./", check=False):
        tag = tag + "-dirty"
        if not quiet_mode:
            print_dirty_image_warning()
        if not prompt_user("Are you sure you would like to continue with this dirty image? (yes/no)"):
            print("Commit and push your changes, then try again.")
            sys.exit()

    destination_and_tag_name = f"{HARBOR_REGISTRY}/{HARBOR_PATH}:{tag}"

    author_email, _ = run_cmd("git log -1 --pretty=format:%ae", capture_output=True)

    build_command = (
        f"docker build "
        f"-t {destination_and_tag_name} "
        f"--target kubernetes "
        f"-f Dockerfile . "
        f"--label org.opencontainers.image.authors={author_email} "

    )

    run_cmd(build_command, print_cmd=True)

    try:
        stdout, stderr = run_cmd(f"docker push {destination_and_tag_name}",
                                 print_cmd=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        error_message = str(e)
        stderr = e.stderr.decode()
        print("stderr output: ", stderr)
        if stderr and 'unauthorized: unauthorized to access repository' in stderr:
            try:
                print("There was an error regarding acces to harbor. Lets try signing in...")
                print("please enter your harbor credentials in the prompts:")
                run_cmd(f"docker login {HARBOR_REGISTRY}", check=True,
                        print_cmd=True)
                run_cmd(f"docker push {destination_and_tag_name}",
                        print_cmd=True, capture_output=True, check=True)
            except subprocess.CalledProcessError as e:
                error_message = str(e)
                print("Error: " + error_message)
                print("stderr output: ", stderr)
                print_harbor_login_information()
                sys.exit()
        else:
            print("There was an error when pushing to harbor")
            print("Error: " + error_message)
            print("stderr:" + stderr)
            sys.exit()

    # Put the new kustomization hash in the produciton kustomization yaml file.
    run_cmd(f"sed -i -e 's/newTag: [^ ]*/newTag: {tag}/' "
            f"{PATH_TO_KUSTOMIZATION_FILE}", print_cmd=True)

    print_kustomization_and_image_information(destination_and_tag_name)


    # Commands to commit and push kustomization hash to remote branch.
    git_add_cmd = f"git add {PATH_TO_KUSTOMIZATION_FILE}"
    git_commit_cmd = "git commit --amend --no-edit"
    git_push_cmd = f"git push origin {CURRENT_WORKING_REMOTE_BRANCH}"

    print("Would you like to automatically perform the following commands: ")
    print_colored(f"{git_add_cmd}\n{git_commit_cmd}\n{git_push_cmd}",
                  color="yellow")


    if prompt_user("Let script run these git commands automatically? (yes/no)"):
        run_cmd(git_add_cmd, print_cmd=True)
        run_cmd(git_commit_cmd, print_cmd=True)
        run_cmd(git_push_cmd, print_cmd=True)


    else:
        if not quiet_mode:
            print_commit_tree_hash_reminder_information()


if __name__ == "__main__":
    main()
