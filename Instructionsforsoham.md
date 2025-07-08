## Generate SIP_OUTBOUND_TRUNK_ID
Create a file called outbound.json and fill in the details
```json
{
  "trunk": {
    "name": "My Outbound Calls",
    "address": "SIP Outbound Address",
    "numbers": ["Phone-Number"], 
    "auth_username": "Username",
    "auth_password": "Password"
  }
}
```
Run the following command to generate the `SIP_OUTBOUND_TRUNK_ID`
```bash
lk sip outbound create outbound.json
```
## Set up the environemnt
Set up the environment by filling in the required values:

```
`LIVEKIT_URL`
`LIVEKIT_API_KEY`
`LIVEKIT_API_SECRET`
`OPENAI_API_KEY`
`SIP_OUTBOUND_TRUNK_ID`
```

Run the agent in one shell:

```shell
python3 agent.py dev
```
Open another shell and  dispatch an agent to make a call by :
1. bash/zsh
```bash
lk dispatch create \
  --new-room \
  --agent-name outbound-caller \
  --metadata '{"phone_number": "The Phone Number to Dial", "transfer_to": "Transfer_to_Here"}'
```
2. cmd
```cmd
lk dispatch create --new-room --agent-name outbound-caller --metadata "{\"phone_number\": \"+91123456789\"}"
```
