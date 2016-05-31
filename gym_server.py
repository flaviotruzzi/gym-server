import os
import gym
from flask import Flask, jsonify, render_template, request, send_file
from cStringIO import StringIO
from PIL import Image


environment = os.environ['GYM_ENV']


env = gym.make(environment)


cached_image = None


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


def get_render_mode(environ):
    if 'rgb_array' in environ.metadata['render.modes']:
        return 'rgb_array'
    elif 'ansi' in environ.metadata['render.modes']:
        return 'ansi'
    else:
        return None


def save_img(img):
    im = Image.fromarray(img)
    im.save("simulation.png")


render_mode = get_render_mode(env)

app = Flask(__name__)


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
    global cached_image
    render = request.args.get('render')

    try:
        observation, reward, done, info = env.step(action)

        if render:
            save_img(env.render(render_mode))


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


@app.route("/help")
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


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/render")
def render():
    return send_file("simulation.png")


if __name__ == '__main__':
    app.run(host="0.0.0.0")
