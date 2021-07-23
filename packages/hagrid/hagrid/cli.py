# stdlib
import hashlib
import os
import subprocess
from typing import Any
from typing import Dict as TypeDict
from typing import List as TypeList
from typing import Optional
from typing import Tuple as TypeTuple

# third party
import click

# relative
from .art import hagrid
from .art import motorcycle
from .auth import AuthCredentials
from .cache import arg_cache
from .deps import DEPENDENCIES
from .deps import MissingDependency
from .grammar import BadGrammar
from .grammar import GrammarVerb
from .grammar import parse_grammar
from .launch import get_launch_verb
from .lib import GRID_SRC_PATH
from .lib import check_docker_version
from .lib import name_tag
from .style import RichGroup


@click.group(cls=RichGroup)
def cli():
    pass


@click.command(help="Start a new PyGrid domain/network node!")
@click.argument("args", type=str, nargs=-1)
@click.option(
    "--username",
    default=None,
    required=False,
    type=str,
    help="Optional: the username for provisioning the remote host",
)
@click.option(
    "--key_path",
    default=None,
    required=False,
    type=str,
    help="Optional: the path to the key file for provisioning the remote host",
)
# @click.option(
#     "--password",
#     default=None,
#     required=False,
#     type=str,
#     help="Optional: the password for provisioning the remote host",
# )
# @click.option(
#     "--mode",
#     default=None,
#     required=False,
#     type=str,
#     help="Optional: mode either provision or deploy, where deploy is a quick code update",
# )
@click.option(
    "--repo",
    default=None,
    required=False,
    type=str,
    help="Optional: repo to fetch source from",
)
@click.option(
    "--branch",
    default=None,
    required=False,
    type=str,
    help="Optional: branch to monitor for updates",
)
def launch(args: TypeTuple[str], **kwargs: TypeDict[str, Any]):
    verb = get_launch_verb()
    try:
        grammar = parse_grammar(args=args, verb=verb)
        verb.load_grammar(grammar=grammar)
    except BadGrammar as e:
        print(e)
        return

    try:
        cmd = create_launch_cmd(verb=verb, kwargs=kwargs)
    except Exception as e:
        print(f"{e}")
        return
    print("Running: \n", cmd)
    subprocess.call(cmd, shell=True)


class QuestionInputError(Exception):
    pass


class Question:
    def __init__(
        self,
        var_name: str,
        question: str,
        kind: str,
        default: Optional[str] = None,
        cache: bool = False,
    ) -> None:
        self.var_name = var_name
        self.question = question
        self.default = default
        self.kind = kind
        self.cache = cache

    def validate(self, value: str) -> str:
        if self.default is not None and value == "":
            return self.default

        if self.kind == "path":
            value = os.path.expanduser(value)
            if not os.path.exists(value):
                error = f"{value} is not a valid path."
                if self.default is not None:
                    error += f" Try {self.default}"
                raise QuestionInputError(error)

        if self.kind == "yesno":
            if value.lower().startswith("y"):
                return "y"
            elif value.lower().startswith("n"):
                return "n"

        return value


def requires_kwargs(
    required: TypeList[Question], kwargs: TypeDict[str, str]
) -> TypeDict[str, Any]:

    parsed_kwargs = {}
    for question in required:
        if question.var_name in kwargs and kwargs[question.var_name] is not None:
            value = kwargs[question.var_name]
        else:
            if question.default is not None:
                value = click.prompt(
                    question.question, type=str, default=question.default
                )
            else:
                value = click.prompt(question.question, type=str)

        value = question.validate(value=value)
        if question.cache:
            setattr(arg_cache, question.var_name, value)

        parsed_kwargs[question.var_name] = value
    return parsed_kwargs


def create_launch_cmd(verb: GrammarVerb, kwargs: TypeDict[str, Any]) -> str:
    host_term = verb.get_named_term_type(name="host")
    host = host_term.host
    if host in ["docker"]:
        version = check_docker_version()
        if version:
            return create_launch_docker_cmd(verb=verb, docker_version=version)
    elif host in ["vm"]:
        if (
            DEPENDENCIES["vagrant"]
            and DEPENDENCIES["virtualbox"]
            and DEPENDENCIES["ansible-playbook"]
        ):
            return create_launch_vagrant_cmd(verb=verb)
        else:
            errors = []
            if not DEPENDENCIES["vagrant"]:
                errors.append("vagrant")
            if not DEPENDENCIES["virtualbox"]:
                errors.append("virtualbox")
            if not DEPENDENCIES["ansible-playbook"]:
                errors.append("ansible-playbook")
            raise MissingDependency(
                f"Launching a VM locally requires: {' '.join(errors)}"
            )
    elif host in ["aws", "azure", "gcp"]:
        print("launch @ cloud")
        return
    else:
        if DEPENDENCIES["ansible-playbook"]:
            username_question = Question(
                var_name="username",
                question=f"Username for {host} with sudo privledges?",
                default=arg_cache.username,
                kind="string",
                cache=True,
            )
            key_path_question = Question(
                var_name="key_path",
                question=f"Private key for [username]@{host}?",
                default=arg_cache.key_path,
                kind="path",
                cache=True,
            )
            repo_question = Question(
                var_name="repo",
                question=f"Repo to fetch source from?",
                default=arg_cache.repo,
                kind="string",
                cache=True,
            )
            branch_question = Question(
                var_name="branch",
                question=f"Branch to monitor for updates?",
                default=arg_cache.branch,
                kind="string",
                cache=True,
            )
            parsed_kwargs = requires_kwargs(
                required=[
                    username_question,
                    key_path_question,
                    repo_question,
                    branch_question,
                ],
                kwargs=kwargs,
            )

            auth = AuthCredentials(
                username=parsed_kwargs["username"], key_path=parsed_kwargs["key_path"]
            )
            if auth.valid:
                return create_launch_custom_cmd(
                    verb=verb, auth=auth, kwargs=parsed_kwargs
                )
        else:
            errors = []
            if not DEPENDENCIES["ansible-playbook"]:
                errors.append("ansible-playbook")
            raise MissingDependency(
                f"Launching a Custom VM requires: {' '.join(errors)}"
            )


def create_launch_docker_cmd(
    verb: GrammarVerb, docker_version: str, tail: bool = False
) -> str:
    host_term = verb.get_named_term_type(name="host")
    node_name = verb.get_named_term_type(name="node_name")
    node_type = verb.get_named_term_type(name="node_type")
    tag = name_tag(name=node_name.input)

    hagrid()

    print(
        "Launching a "
        + str(node_type.input)
        + " PyGrid node on port "
        + str(host_term.free_port)
        + "!\n"
    )

    print("  - TYPE: " + str(node_type.input))
    print("  - NAME: " + str(node_name.input))
    print("  - TAG: " + str(tag))
    print("  - PORT: " + str(host_term.free_port))
    print("  - DOCKER: " + docker_version)
    print("\n")

    cmd = ""
    cmd += "DOMAIN_PORT=" + str(host_term.free_port)
    cmd += " TRAEFIK_TAG=" + str(tag)
    cmd += ' DOMAIN_NAME="' + node_name.input + '"'
    cmd += " NODE_TYPE=" + node_type.input
    cmd += " docker compose -p " + node_name.input.lower().replace(" ", "_")
    cmd += " up"
    if not tail:
        cmd += " -d"
    cmd = "cd " + GRID_SRC_PATH + ";" + cmd
    return cmd


def create_launch_vagrant_cmd(verb: GrammarVerb) -> str:
    host_term = verb.get_named_term_type(name="host")
    node_name = verb.get_named_term_type(name="node_name")
    node_type = verb.get_named_term_type(name="node_type")

    hagrid()

    print(
        "Launching a "
        + str(node_type.input)
        + " PyGrid node on port "
        + str(host_term.port)
        + "!\n"
    )

    print("  - TYPE: " + str(node_type.input))
    print("  - NAME: " + str(node_name.input))
    print("  - PORT: " + str(host_term.port))
    # print("  - VAGRANT: " + "1")
    # print("  - VIRTUALBOX: " + "1")
    print("\n")

    cmd = ""
    cmd += 'ANSIBLE_ARGS="'
    cmd += f"-e 'node_name={node_name.input}'"
    cmd += f"-e 'node_type={node_type.input}'"
    cmd += '" '
    cmd += "vagrant up --provision"
    cmd = "cd " + GRID_SRC_PATH + ";" + cmd
    return cmd


def create_launch_custom_cmd(
    verb: GrammarVerb, auth: AuthCredentials, kwargs: TypeDict[str, Any]
) -> str:
    host_term = verb.get_named_term_type(name="host")
    node_name = verb.get_named_term_type(name="node_name")
    node_type = verb.get_named_term_type(name="node_type")
    node_type = verb.get_named_term_type(name="node_type")
    source_term = verb.get_named_term_type(name="source")

    hagrid()

    print(
        "Launching a "
        + str(node_type.input)
        + " PyGrid node on port "
        + str(host_term.port)
        + "!\n"
    )

    print("  - TYPE: " + str(node_type.input))
    print("  - NAME: " + str(node_name.input))
    print("  - PORT: " + str(host_term.port))
    print("\n")

    playbook_path = GRID_SRC_PATH + "/ansible/site.yml"
    ansible_cfg_path = GRID_SRC_PATH + "/ansible.cfg"

    if not os.path.exists(playbook_path):
        print(f"Can't find playbook site.yml at: {playbook_path}")
    cmd = f"ANSIBLE_CONFIG={ansible_cfg_path} ansible-playbook -i {host_term.host}, {playbook_path}"
    if host_term.host != "localhost":
        cmd += f" --private-key {auth.key_path} --user {auth.username}"
    ANSIBLE_ARGS = {
        "node_type": node_type.input,
        "node_name": node_name.input,
        "github_repo": kwargs["repo"],
        "repo_branch": kwargs["branch"],
    }

    if host_term.host == "localhost":
        ANSIBLE_ARGS["local"] = "true"

    # if mode == "deploy":
    #     ANSIBLE_ARGS["deploy"] = "true"

    for k, v in ANSIBLE_ARGS.items():
        cmd += f" -e '{k}={v}'"

    cmd = "cd " + GRID_SRC_PATH + ";" + cmd
    return cmd


@click.command(help="Build (or re-build) PyGrid docker image.")
def build():
    check_docker_version()

    print("\n")

    cmd = ""
    cmd += " docker compose"
    cmd += " build"

    cmd = "cd " + GRID_SRC_PATH + ";" + cmd
    print(cmd)
    subprocess.call(cmd, shell=True)


@click.command(help="Stop a running PyGrid domain/network node.")
@click.argument("name", type=str, nargs=-1)
@click.option(
    "--type",
    "node_type",
    default="domain",
    required=False,
    type=click.Choice(["domain", "network"]),
    help="The type of node you would like to terminate.",
)
@click.option(
    "--port",
    default=8081,
    required=False,
    type=int,
    help="The public port your node exposes. (Default: 8081)",
)
@click.option(
    "--tag",
    default="",
    required=False,
    type=str,
    help="Optional: the underlying docker tag used (Default: 'domain_'+md5(name)",
)
@click.option(
    "--keep-db/--delete-db",
    default=True,
    required=False,
    type=bool,
    help="""If restarting a node that already existed, don't/do reset the database (Default: deletes the db)""",
)
def land(node_type, name, port, tag, keep_db):

    _name = ""
    for word in name:
        _name += word + " "
    name = _name[:-1]

    if name == "all":
        subprocess.call("docker rm `docker ps -aq` --force", shell=True)
        return

    if tag == "" and name == "":
        raise Exception(
            "You must provide either the --tag or --name of the node you want to land!"
        )

    elif tag == "" and name != "" and node_type != "":
        tag = hashlib.md5(name.encode("utf8")).hexdigest()
        tag = node_type + "_" + tag

    elif tag != "":
        """continue"""

    else:
        raise Exception(
            "You must provide either a type and name, or you must provide a tag."
        )

    version = check_docker_version()

    motorcycle()

    print("Launching a " + str(node_type) + " PyGrid node on port " + str(port) + "!\n")
    print("  - TYPE: " + str(node_type))
    print("  - NAME: " + str(name))
    print("  - TAG: " + str(tag))
    print("  - PORT: " + str(port))
    print("  - DOCKER: " + version)

    print("\n")

    cmd = "DOMAIN_PORT=" + str(port)
    # cmd += " TRAEFIK_TAG=" + tag
    cmd += ' DOMAIN_NAME="' + name + '"'
    cmd += " NODE_TYPE=" + node_type
    cmd += " docker compose"
    cmd += ' --file "docker-compose.override.yml"'
    cmd += ' --project-name "' + tag + '"'
    cmd += " down"

    cmd = "cd " + GRID_SRC_PATH + ";export $(cat .env | sed 's/#.*//g' | xargs);" + cmd
    print(cmd)
    subprocess.call(cmd, shell=True)

    if not keep_db:
        print("Deleting database for node...")
        subprocess.call("docker volume rm " + tag + "_app-db-data", shell=True)
        print()


cli.add_command(launch)
cli.add_command(build)
cli.add_command(land)
