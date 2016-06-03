# gym-server

This project provide a rest api for [gym](https://github.com/openai/gym) using docker.
The aim is to provide a simple way to build and test RL algorithms in other languages than python.

Stay tunned for the first client that uses this: [scala-gym](https://github.com/flaviotruzzi/scala-gym)

## Installation

1. Install docker.
2. Build docker image with:
```bash
➜  gym-server git:(master) ✗ docker build -t gym-server:latest .
```

OR

Pull the image form docker hub: flaviotruzzi/gym-server:latest

OR 

Run it locally:

```bash
➜  gym-server git:(master) ✗ pip install -r requirements.txt
➜  gym-server git:(master) ✗ ./start.sh
```

## Usage

Run with:
```bash
➜  gym-server git:(master) ✗ docker run -p 5000:5000 -e "GYM_ENV=CartPole-v0" -t gym-server
```

You can change your environment by change the env variable GYM_ENV.

*Obs: Only tested with CartPole-v0 for now.*

To check the available API:

### Help
```bash
➜  gym-server git:(master) ✗ curl http://192.168.99.100:5000/help
{
  "available_commands": {
    "/info": "Expose useful information, such as: action_space, and observation_space.",
    "/reset": "Reset environment.",
    "/step/<int:action>": "Execute given action.",
    "/help": "Friendly start message."
  }
}%
```

### Reset

Reset the environment, also call render, and generate an image of the current state.

```bash
➜  gym-server git:(master) ✗ curl http://192.168.99.100:5000/reset
{
  "observation": [
    0.04925519339170291,
    0.039513295684822855,
    -0.016974759602974232,
    0.022082220039032124
  ]
}%
```

### Step

Execute one step passing an action.

```bash
➜  gym-server git:(master) ✗ curl http://192.168.99.100:5000/step/0
{
  "done": false,
  "info": {},
  "observation": [
    0.050045459305399366,
    -0.15536115921791527,
    -0.01653311520219359,
    0.30936145003979154
  ],
  "reward": 1.0
}%
```

You may also pass the parameter `?render=true` which will call the 
render method, generating an image of the resulting state.

### Info

Provide some information about the environment, such as, action space and observation space.

```bash
➜  gym-server git:(master) ✗ curl http://192.168.99.100:5000/info
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
