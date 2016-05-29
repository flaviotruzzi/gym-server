import gym
from flask import Flask, jsonify
import os


environment = os.environ['GYM_ENV']


env = gym.make(environment)


app = Flask(__name__)


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/reset")
def reset():
    """
    Reset environment.
    :return: first observation
    """
    return jsonify({'observation': env.reset().tolist()})


@app.route("/step/<int:action>")
def step(action):
    """
    Execute given action.
    :param action: Integer value representing the action.
    :return:
    """
    try:
        observation, reward, done, info = env.step(action)
        return jsonify({
            'observation': observation.tolist(),
            'reward': reward,
            'done': done,
            'info': info
        })
    except AssertionError:
        raise InvalidUsage('Invalid Action')


@app.route("/info")
def info():
    """
    Expose useful information, such as: action_space, and observation_space.
    :return:
    """
    return jsonify({
        'action_space': str(env.action_space),
        'observation_space': {
            'shape': env.observation_space.shape,
            'low': env.observation_space.low.tolist(),
            'high': env.observation_space.high.tolist()
        }
    })


@app.route("/")
def readme():
    """
    :return: Friendly start message.
    """
    def parse_doc(function):
        return function.__doc__.strip().split('\n')[0]

    return jsonify({
        'available_commands': {
            "/reset": parse_doc(reset),
            "/step/<int:action>": parse_doc(step),
            "/info": parse_doc(info)
        }
    })


app.run(host='0.0.0.0')
