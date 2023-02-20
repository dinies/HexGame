from python_on_whales import docker
import os
import sys
from pathlib import Path


def getUsername() -> str:
    if sys.platform == "linux":
        return os.environ.get("USERNAME")
    elif sys.platform == "darwin":
        return os.getlogin()
    elif sys.platform == "win32":
        raise EnvironmentError("Windows not supported yet")
    raise EnvironmentError("Unknown platform (not linux, macos or windows)")


def getDisplay() -> str:
    if sys.platform == "linux":
        return os.environ.get("DISPLAY")
    elif sys.platform == "darwin":
        return "docker.for.mac.host.internal:0"
    elif sys.platform == "win32":
        raise EnvironmentError("Windows not supported yet")
    else:
        raise EnvironmentError(
            "Unknown platform (not linux, macos or windows)")


def main():
    container_name = "hex_game"
    docker_image_name = container_name + "_img"
    gpus = True
    target_dockerfile_layer = "final"

    username = getUsername()
    if gpus:
        base_image = "nvidia/cuda:12.0.1-devel-ubuntu20.04"
    else:
        base_image = "ubuntu:focal"
    home = Path.home()

    uid = str(os.getuid()) if sys.platform == "linux" else "1000"
    gid = str(os.getgid()) if sys.platform == "linux" else "1000"

    build_args = {k: str(v) for k, v in {
        "uid": uid,
        "gid": gid,
        "base_image": base_image,
        "user": username
    }.items()}

    docker.build(
        build_args=build_args,
        context_path=".",
        file="./Dockerfile",
        ssh="default",
        tags=docker_image_name,
        target=target_dockerfile_layer
    )

    environment = {
        "DISPLAY": getDisplay(),
        "QT_X11_NO_MITSHM": "1"
    }
    if gpus:
        environment["NVIDIA_DRIVER_CAPABILITIES"] = "all"

    devices = [
        "/dev/input:/dev/input:rwm"
    ]

    if sys.platform == "linux":
        devices.append("/dev/dri:/dev/dri:rwm")

    volumes = [
        ("/var/run/docker.sock", "/var/run/docker.sock"),
        (Path(home / "hex_exchange").as_posix(),
         "/home/"+username+"/hex_exchange"),
        ("/tmp/.X11-unix", "/tmp/.X11-unix", "rw"),
        (os.environ.get("XAUTHORITY"),
         "/home/"+username+"/.Xauthority")
    ]

    docker_run_params = {
        "image": docker_image_name,
        "envs": environment,
        "name": container_name,
        "devices": devices,
        "ipc": "host",
        "networks": "host",
        "interactive": True,
        "tty": True,
        "user": uid + ':' + gid,
        "volumes": volumes
    }

    if gpus:
        docker_run_params["runtime"] = "nvidia"
        docker_run_params["gpus"] = "all"

    try:
        docker.run(**docker_run_params)
    finally:
        sys.exit(0)


if __name__ == "__main__":
    main()
