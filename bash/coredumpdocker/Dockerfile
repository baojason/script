#################################################################################
# SDX6210 coredump docker image profile                                         #
# Issue docker commands:                                                        #
#   docker images                                                               #
#   docker rmi -f <found image ID in above command>                             #
#   docker build --tag=coredump .                                               #
# The first two are optional for clean up old coredump image                    #
#################################################################################

# Import base image
FROM debian:stable

# Install gdb
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils \
    && apt-get install -y gdb \
    && rm -rf /var/lib/apt/lists/*

# Install wget
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils \
    && apt-get install -y wget \
    && rm -rf /var/lib/apt/lists/*

# Install scp
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils \
    && apt-get install -y openssh-client \
    && rm -rf /var/lib/apt/lists/*

# Install vim
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils \
    && apt-get install -y vim \
    && rm -rf /var/lib/apt/lists/*

# Install tree
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils \
    && apt-get install -y tree \
    && rm -rf /var/lib/apt/lists/*

# Add bash scripts for auto decode coredump file
COPY root /root/
RUN chmod +x /root/decode.sh
RUN chmod +x /root/dump.sh

#CMD ["/bin/bash"]
# Prepare for coredump file, symbol file, tool chain folder mapping
RUN touch /root/coredump.tar.gz
RUN touch /root/symbolfile
RUN mkdir -p /root/tlc
WORKDIR /root

# Update executable PATH
ENV PATH="/root/tlc/usr/bin/:${PATH}"

# set timezone
ENV TZ=America/Chicago
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

