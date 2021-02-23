# discord-showcase [![CodeDay](https://circleci.com/gh/codeday/discord-showcase.svg?style=shield)](<LINK>)
A bot to integrate [showcase.codeday.org](https://showcase.codeday.org/) with the [CodeDay Discord](https://discord.com/invite/codeday)

### Description
<div>
This bot allows for the use of a pod-system. A pod-system is a 
collection of showcase projects/teams where the purpose is to allow
mentors to better help a larger amount of members working on their
projects. This pod system is 
created using the s~create_pods <number_of_pods> command. Each pod 
is also assigned a mentor upon the creation of the pod. After creating
the pods, the administrator must run s~assign_pods to do a GQL query and
retrieve the projects from showcase to fill the pods with teams and
the members within those teams.
</div>

### Noteworthy Commands
The command prefix for any command is s~, for example:
> s~create_pods 3

| command         | arguments                     | summary                                                                                                                                                                                                         |
|-----------------|-------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| help            | none                          | Displays a list of commands and their actions. Less descriptive than this documentation.                                                                                                                        |
| create_pods     | <number_of_pods>              | Creates the pods by adding them to the alembic database and creating the text channels.                                                                                                                         |
| assign_pods     | none                          | Assigns teams from showcase projects that do not have a pod to a pod.                                                                                                                                           |
| add_mentor      | <mentor> <pod_name> OR none   | Gives mentor permissions to a particular discord member for a pod, which could be another mentor. No argument means it will run in the pod channel without the pod name.                                                                                                                                          |
| checkin         | <pod_name>                    | Asks members in a specific pod how they are doing by listening for reactions and reporting it to grafana.codeday.org                                                                                            |
| checkin_all     | none                          | Asks members in ALL pods how they are doing by listening for reactions and reporting it to grafana.codeday.org                                                                                                  |
| send_message    | <pod_name> <message_string>   | Sends a message to a single pod using the bot account.                                                                                                  |
| send_message_all| <message_string>              | Sends a message to every pod using the bot account.                                                                                                  |
| list_pods       | none                          | Displays all the current pods in the channel the command is given.                                                                                                                                              |
| list_teams      | <pod_name> OR none            | Displays all the teams of a particular pod in the channel the command is given or for the given pod name                                                                                                        |
| merge_pods      | <pod_from_name> <pod_to_name> | Will remove the pod_from_name pod and merge it into pod_to_names. This will delete the text-channel for pod_from_name and move all members within that text channel to the new channel in pod_to_names channel. |
| remove_pod      | <pod_name> OR none            | Removes a singular pod specified by its name, removes the text channel and any traces in alembic. No argument means it will run in the pod channel without the name.                                                                                      |
| remove_all_pods | none                          | Removes all pods from alembic and deletes all the text channels under the pods category given in the environment variable.                                                                                      |

### Environment Variables
There are a couple of environment variables that need to be set when switching the bots servers.

| variable            | value | description                                                                 |
|---------------------|-------|-----------------------------------------------------------------------------|
| TEAMS_PER_POD       | int   | The number of projects/teams that should be in a singular pod               |
| ROLE_STAFF          | int   | The role in which the bot will give all permissions to all the pod channels |
| ROLE_MENTOR         | int   | The role in which the bot will pick a mentor from for each pod text channel |
| CATEGORY            | int   | The category in which the pods will reside                                  |
| EVENT_ID            | str   | The eventGroup from GQL for which CodeDay it is                             |
| DB_DB               | str   | available upon request                                                      |
| DB_PASSWORD         | str   | available upon request                                                      |
| DB_USERNAME         | str   | available upon request                                                      |
| DB_HOST             | str   | available upon request                                                      |
| BOT_TOKEN           | int   | available upon request                                                      |
| GQL_SHOWCASE_SECRET | str   | available upon request                                                      |

### Event Listeners

| event                     | action                                                  |
|---------------------------|---------------------------------------------------------|
| on_project_created        | Assigns members of project to a specific pod            |
| on_project_member_added   | Adds member of project to groups pods text channel      |
| on_project_member_removed | Removes member of project from groups pods text channel |