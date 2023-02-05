#syntax = docker/dockerfile:1.2
ARG base_image
FROM ${base_image} AS setup


ARG DEBIAN_FRONTEND=noninteractive
ENV DISPLAY :0
SHELL [ "/bin/bash" , "-c" ]

RUN apt-get update && \
  apt-get install -qqy --no-install-recommends \
  sudo keyboard-configuration software-properties-common \
  openssh-server gnupg2  make wget pciutils git curl
#keyboard-configuration allows to skip the prompted message about the keyboard conf
#software-properties-common: needed in add-apt-repository -y ppa:bar-foo command
#gnupg2  and openssh-server: needed in wget -O - https://bar.foo  command

ARG uid
ARG gid
ARG user
ENV USERNAME $user
ARG group=${user}
ENV HOME /home/${user} 
# sudoers 
RUN groupadd -g ${gid} ${group}
RUN useradd -c "${user} user" -d $HOME -u ${uid} -g ${gid} -m ${user} && \
  usermod -aG sudo ${user} && \
  echo "${user} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

#avoid deletion of apt packages for caching purposes
RUN rm -f /etc/apt/apt.conf.d/docker-clean

#upgrade mesa to allow OpenGL 4.5 on Ubuntu20.04
RUN apt-add-repository  ppa:kisak/kisak-mesa && \
  apt update && \
  apt upgrade -y

CMD ["/bin/bash"]
FROM setup AS install_python 
RUN apt-get install -y build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
    libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl

USER ${user}
RUN curl https://pyenv.run | bash
RUN echo 'export PYENV_ROOT="$HOME/.pyenv/"' >> ~/.bashrc
RUN echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
RUN echo 'export PYENV_VIRTUALENV_DISABLE_PROMPT=1' >> ~/.bashrc
RUN echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
RUN echo 'eval "$(pyenv init -)"' >> ~/.bashrc
RUN echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
RUN source ~/.bashrc
ENV PYENV_ROOT="$HOME/.pyenv/"
ENV PATH="$PYENV_ROOT/bin:$PATH"
RUN eval "$(pyenv init --path)" &&\
    eval "$(pyenv init -)" && \
    eval "$(pyenv virtualenv-init -)" && \
    pyenv install 3.10.0 && \
    pyenv virtualenv 3.10.0 hex && \
    pyenv activate hex && \
    pip install --upgrade pip && \
    pip install wheel && \
    pip install PyOpenGL \
    PyOpenGL_accelerate pyopengl pygame numpy glfw

WORKDIR /home/${user}
CMD ["/bin/bash"]
FROM install_python AS final
CMD ["/bin/bash"]
