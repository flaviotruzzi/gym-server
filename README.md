# gym-server

This project provide a rest api for [gym](https://github.com/openai/gym) using docker.

## Installation

1. Install docker.
2. Build docker image with:
```bash
➜  gym-server git:(master) ✗ docker build -t gym-server:latest .
```

## Usage

Run with:
```bash
➜  gym-server git:(master) ✗ docker run -p 5000:5000 -e "GYM_ENV=CartPole-v0" -t gym-server
```

You can change your environment by change the env variable GYM_ENV.

*Obs: Only tested with CartPole-v0 for now.*

To check the available API:

```bash
➜  gym-server git:(master) ✗ curl http://192.168.99.100:5000/
{
  "available_commands": {
    "/info": "Expose useful information, such as: action_space, and observation_space.",
    "/reset": "Reset environment.",
    "/step/<int:action>": "Execute given action."
  }
}%
```

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D
