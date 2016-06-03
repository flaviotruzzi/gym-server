# gym-server

This project provide a rest api for [gym](https://github.com/openai/gym) using docker.
The aim is to provide a simple way to build and test RL algorithms in other languages than python.

Stay tunned for the first client that uses this: [scala-gym](https://github.com/flaviotruzzi/scala-gym)

## Usage

- Running it locally:

```bash
➜  gym-server git:(master) ✗ pip install -r requirements.txt
➜  gym-server git:(master) ✗ ./start.sh
```

- Using docker:

Pull the image form docker hub: flaviotruzzi/gym-server:latest

- Building docker:

1. Install docker.
2. Build docker image with:
```bash
➜  gym-server git:(master) ✗ docker build -t gym-server:latest .
```

## API

### Help
```bash
➜  gym-server git:(master) ✗ curl http://192.168.99.100:5000/v1/help
```
```json
{
  "v1": {
    "/v1/envs/<instance_id>/info": {
      "doc": "Expose useful information, such as: action_space, and observation_space.\n    :return:",
      "methods": "HEAD,OPTIONS,GET"
    },
    "/v1/envs/<instance_id>/monitor/close/": {
      "doc": "Stop monitoring.\n    :param instance_id:\n    :return:",
      "methods": "POST,OPTIONS"
    },
    "/v1/envs/<instance_id>/monitor/start/": {
      "doc": "Start monitoring. Accept json with the following format:\n    {\n        'force': true,\n        'resume: false\n    }\n    :param instance_id:\n    :return:",
      "methods": "POST,OPTIONS"
    },
    "/v1/envs/<instance_id>/reset/": {
      "doc": "Reset environment. Accept json to say if it should render or not.\n\n    {\n      \"render\": false\n    }\n\n    :param instance_id:\n    :return: first observation",
      "methods": "POST,OPTIONS"
    },
    "/v1/envs/<instance_id>/step/": {
      "doc": "Execute given action.\n\n    Accept json with the following format:\n    {\n      'action': 0,\n      'render': true\n    }\n\n    The API assumes that action is an integer. Render can be set to expose the rendered image. Render is optional.\n\n    :param instance_id:\n    :param action: Integer value representing the action.\n    :return: json with environment response.",
      "methods": "POST,OPTIONS"
    },
    "/v1/envs/<instance_id>/upload/": {
      "doc": ":param instance_id:\n    :return:",
      "methods": "POST,OPTIONS"
    },
    "/v1/envs/create/": {
      "doc": "Create Environment. Accept a json with the following format:\n    {\n      'environment': 'CartPole-v0'\n    }\n\n    :return: json with instance_id of the environment",
      "methods": "POST,OPTIONS"
    },
    "/v1/help": {
      "doc": ":return: Friendly start message.",
      "methods": "HEAD,OPTIONS,GET"
    }
  }
}%
```

### Create Environment

Create an Environment, return the instance id.

```bash
curl -H "Content-Type: application/json" -XPOST http://192.168.99.100:5000/v1/envs/create/ -d '{"environment": "CartPole-v0"}'
```
```json
{
  "instance_id": "ce2dbb50"
}%
```

### Reset

Reset the environment, and generate an image of the current state.

```bash
➜  gym-server git:(master) ✗ curl  -XPOST -H "Content-Type: application/json" http://192.168.99.100:5000/v1/envs/ce2dbb50/reset/ -d '{"render": true}'
```
```json
{
  "observation": {
    "observation": [
      0.005304555907637974,
      0.03223077653449176,
      -0.04756061105355254,
      -0.03335494425626853
    ],
    "render": "successfully rendered: 1.png"
  }
}%
```

### Step

Execute one step passing an action.

```bash
curl -XPOST -H "Content-Type: application/json" http://192.168.99.100:5000/v1/envs/ce2dbb50/step/ -d '{"action": true}'
```
```json
{
  "done": false,
  "info": {},
  "observation": [
    0.0059491714383278094,
    0.22800135862141657,
    -0.048227709938677914,
    -0.3406563021698157
  ],
  "reward": 1.0
}%
```

### Monitor

The artifacts generated through the monitor are available through port 8000.

#### Start

Start monitoring.

```bash
curl -XPOST -H "Content-Type: application/json" http://192.168.99.100:5000/v1/envs/ce2dbb50/monitor/start/ -d '{"force": false, "resume": false}'
{
  "message": true
}%
```

#### Close

Stop monitoring.

```bash
curl -XPOST -H "Content-Type: application/json" http://192.168.99.100:5000/v1/envs/ce2dbb50/monitor/stop/
{
  "message": true
}%
```

### Upload

Upload results stored by the monitoring.

```bash
curl -XPOST -H "Content-Type: application/json" http://192.168.99.100:5000/v1/envs/ce2dbb50/upload/ -d '{"algorithm_id": "my_id", "writeup": "http://mygist", "api_key": "my_apikey",_ "ignore_open_monitors": true}'
{
  "message": true
}%
```

### Info

Provide some information about the environment, such as, action space and observation space.

```bash
➜  gym-server git:(master) ✗ curl -XGET -H "Content-Type: application/json" http://192.168.99.100:5000/v1/envs/ce2dbb50/info
{
  "action_space": "Discrete(2)",
  "observation_space": {
    "high": [
      2.4,
      Infinity,
      0.41887902047863906,
      Infinity
    ],
    "low": [
      -2.4,
      -Infinity,
      -0.41887902047863906,
      -Infinity
    ],
    "shape": [
      4
    ]
  }
}%
```

## Accessing the generated images.

The last image generated is always available on: http://192.168.99.100:8000/simulation.png.

You can also access http://192.168.99.100:8000, this is updated every 500ms showing the last generated image.

*Note that all ips depends where your docker is running.*

## Future

* Provide API for recording episodes.
* Provide API to submit simulation to OpenAI.

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

# Contributors

- @catherio: idea of EnvironmentManager, and most of its implementation. Also a lot of influence on the API.
