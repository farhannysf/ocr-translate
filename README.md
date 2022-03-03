# ocr-translate
Discord bot to extract text from image and translate it to English.
## Build and Run Container with Docker Compose
The base image is using python38 DoD Hardened Container (DHC) from `registry1.dso.mil/ironbank/opensource/python/python38:latest` and requires U.S. Department of Defense Platform One credentials.
1. Acquire your U.S. Department of Defense Platform One credentials. ([More Info](https://p1.dso.mil/#/))
2. Install Docker Compose on your machine. ([More Info](https://docs.docker.com/compose/install/))
4. Create Discord bots. You should create two instances of these bots for development and production builds. ([More Info](https://discordpy.readthedocs.io/en/latest/discord.html))
5. Get Discord user ID of the bot maintainer. In Discord, Make sure you have Developer Mode enabled and then **right click on maintainer Discord user -> Copy ID**. ([More Info](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-#))
6. Create a file in this directory with the following format:
```
MAINTAINER_ID="YOUR-BOT-MAINTAINER-DISCORD-ID"
BOT_NAME="YOUR-BOT-NAME"
BOT_TOKEN="YOUR-DISCORD-BOT-TOKEN"
GOOGLE_VISION_KEY="YOUR-GOOGLE-VISION-API-KEY"
```
You should set different values for these keys on different build environment.

6. Depending on the build environment, save the file as either `dev.env` for development build or `prod.env` for production build. 
7. Build and run container by invoking `./build dev` for development build or `./build prod` for production build. Container image will rebuild from scratch on each invocation intentionally.
8. To see logs of running container, invoke `docker logs -f ocr-translate-dev` for development container or `docker logs -f ocr-translate-prod` for production container
9. To shutdown running container, invoke `./shutdown dev` for development container or `./shutdown prod` for production container.