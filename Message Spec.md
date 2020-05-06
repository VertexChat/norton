# Notification Messaging System (NMS)

The **Notification Service Messaging System** is used to inform Vertex clients of changes to server-side state to allow
inconsistent state to reconciled. The NMS will prevent the need of clients to consistently poll the API for changes and
will instead inform clients of which resources need updating _i.e. A user will only be informed of messages sent in a
channels to which they are a member._ The system will use websockets to communicate with clients where each client will
identify themselves using a session id and receive a set of notifications in return if any exist. The NMS will primarily
be used to inform the client of changes to resources such as new messages being sent, users joining/leaving a channel,
the creation of new channels, ect.

## Notification Structure
Each _notification_ will be sent as JSON and consist of three key/value pairs:
 1. Target: The target is the User's id that the message is intended for. This is used primarily to route messages to each
            user. For all intents and purposes the target is mostly irrelevant from the clients perspective.

 2.   Type: The message type is used to identify the appropriate update method e.g. `get_channels` would indicate that
            clients channels need updating and the payload would indicate which channels need refreshing. 

 3. Payload: The payload is the data needed to complete the update functionality. e.g. a payload of `{"user": 100, "channel": 201}` with a type of
             `add_user_to_channel` would indicate the user `100` has been added to channel `201`
              


## Existing Messages
| Target  | Type                    | Payload                          |
|:-------:|:-----------------------:|:--------------------------------:|
| 101     | `add_user_to_channel`   | {"user": 100, "channel": 201}    |
| 101     | `create_channel`        | {"channel": 1011}                |
| 106     | `delete_channel`        | {"channel": 1015}                |
| 101     | `delete_message`        | {"channel": 201, "message": 320} |
| 101     | `remove_channel_member` | {"channel": 999, "message": 100} |
| 101     | `update_channel`        | {"channel": 999}                 |
| 101     | `update_message`        | {"channel": 999, "message": 321} |
