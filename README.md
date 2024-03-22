# Genial

A PoC for GenAI based content.

## Setup

On Debian Linux run the `setup.sh` in order to setup the program.

For all other systems, kindly read to setup for understanding the requirements.

## Running

For any server based activities, Redis needs to be chruned up first. 

If everything is installed correctly, use `genial --help` on CLI to get all supported activities

## Server Architecture explained

The servers assign a unique ID for every conversation. This is maintained on the redis server.

When a user requests a new prompt, a new service is churned up. This service is closed after a set amount of inactive period.

Every message is sent to the server, where the service layer receives it and forwards it to an agent churned up for servicing the request.


