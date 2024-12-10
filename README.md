# Vacation Planner (ongoing)

Vacation Planner is a comprehensive tool designed to generate detailed vacation itineraries based on specific budgets and travel durations. By leveraging cutting-edge technologies, this tool aims to simplify travel planning, providing users with a seamless and tailored experience.


## Features

- Create detailed vacation plans based on budget and time constraints.

- Utilize LLM models to recommend destinations and activities.

- Integrate with modern frameworks and technologies for robust performance.


## Getting Started

Follow the steps below to set up the environment. Ensure Docker is installed if not already.

```shell
cd vacation-planner/
bash scripts/docker.sh  # Optional
cp .env.sample .env
```

Update the `.env` file with your desired username and password. Below is an example setup:

```shell
MONGO_INITDB_DATABASE=app
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=admin

ME_CONFIG_MONGODB_SERVER=mongo
ME_CONFIG_MONGODB_PORT=27017
ME_CONFIG_MONGODB_ENABLE_ADMIN=true
ME_CONFIG_MONGODB_ADMINUSERNAME=admin
ME_CONFIG_MONGODB_ADMINPASSWORD=admin
ME_CONFIG_BASICAUTH_USERNAME=admin
ME_CONFIG_BASICAUTH_PASSWORD=admin

GPT_MODEL=gpt-4o-mini-2024-07-18
OPENAI_API_KEY=abcd-abcd-abcd-abcd  # Replace with your API key

API_URL=http://api:8000
```

Once the setup is complete, run the following command to start the application. Only a single command is needed as the application is fully dockerized:

```shell
docker compose up -d
```


## Tech Stack

Vacation Planner is built using the following technologies:

- **TypeScript and Python:** Core programming languages.

- **Next.js:** For creating an interactive and dynamic front-end experience.

- **FastAPI:** For building a fast and efficient back-end API.

- **LangChain:** To incorporate advanced AI capabilities.

- **MongoDB:** As the database solution for storing user data and travel information.

- **Tailwind CSS:** For crafting a sleek and responsive user interface.

- **Docker:** For containerizing the application to ensure portability and scalability.

- **Linux:** The operating system for development and deployment.


## Future Exploration

- **Kubernetes:** For managing containerized workloads and scaling.

- **AWS:** To integrate cloud solutions for enhanced performance and reliability.

- **Terraform:** For automating infrastructure provisioning.