# compiler/Dockerfile
FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y clang python3 && \
    apt-get install -y g++ build-essential && \
    apt-get install -y openjdk-11-jdk && \
    apt-get clean

    
WORKDIR /app

# Allow writing files here
RUN mkdir /app/codes /app/inputs /app/outputs
