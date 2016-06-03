import gym
from flask import Flask, jsonify, request

from EnvironmentManager import EnvironmentManager
from Exceptions import InvalidUsage

envs = EnvironmentManager()

app = Flask(__name__)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/v1/envs/create/', methods=['POST'])
def create_environment():
    """
    Create Environment. Accept a json with the following format:
    {
      'environment': 'CartPole-v0'
    }

    :return: json with instance_id of the environment
    """
    environment = request.get_json()['environment']
    instance_id = envs.create(environment)
    return jsonify(instance_id=instance_id), 201


@app.route('/v1/envs/<instance_id>/reset/', methods=['POST'])
def reset(instance_id):
    """
    Reset environment. Accept json to say if it should render or not.

    {
      "render": false
    }

    :param instance_id:
    :return: first observation
    """
    render = request.get_json().get('render')
    return jsonify(observation=envs.reset(instance_id, render))


@app.route('/v1/envs/<instance_id>/step/', methods=['POST'])
def step(instance_id):
    """
    Execute given action.

    Accept json with the following format:
    {
      'action': 0,
      'render': true
    }

    The API assumes that action is an integer. Render can be set to expose the rendered image. Render is optional.

    :param instance_id:
    :param action: Integer value representing the action.
    :return: json with environment response.
    """
    request_json = request.get_json()

    try:
        action = request_json['action']
        render = request_json.get('render')
        environment_response = envs.step(instance_id, action, render)
        return jsonify(environment_response)
    except AssertionError:
        raise InvalidUsage('Invalid Action')
    except gym.error.ResetNeeded as ex:
        raise InvalidUsage(ex.message)


@app.route('/v1/envs/<instance_id>/monitor/start/', methods=['POST'])
def monitor_start(instance_id):
    """
    Start monitoring. Accept json with the following format:
    {
        'force': true,
        'resume: false
    }
    :param instance_id:
    :return:
    """
    request_data = request.get_json()

    force = request_data.get('force', False)
    resume = request_data.get('resume', False)

    envs.monitor_start(instance_id, force, resume)
    return jsonify(message=True)


@app.route('/v1/envs/<instance_id>/monitor/close/', methods=['POST'])
def monitor_close(instance_id):
    """
    Stop monitoring.
    :param instance_id:
    :return:
    """
    envs.monitor_close(instance_id)
    return jsonify(message=True)


@app.route('/v1/envs/<instance_id>/upload/', methods=['POST'])
def upload(instance_id):
    """

    :param instance_id:
    :return:
    """
    try:
        request_data = request.get_json()

        algorithm_id = request_data.get('algorithm_id', None)
        writeup = request_data.get('writeup', None)
        api_key = request_data.get('api_key', None)
        ignore_open_monitors = request_data.get('ignore_open_monitors', False)

        envs.upload(instance_id, algorithm_id, writeup, api_key, ignore_open_monitors)

        return jsonify(message=True)
    except Exception as ex:
        raise InvalidUsage(ex.message)


@app.route("/v1/envs/<instance_id>/info", methods=['GET'])
def info(instance_id):
    """
    Expose useful information, such as: action_space, and observation_space.
    :return:
    """
    return jsonify(envs.info(instance_id))


@app.route("/v1/help")
def readme():
    """
    :return: Friendly start message.
    """

    def parse_doc(function):
        return function.__doc__.strip()

    def parse_methods(methods):
        return ','.join(methods)

    return jsonify({
        'v1': {
            rule.rule: {
                'methods': parse_methods(rule.methods), 'doc': parse_doc(globals()[rule.endpoint])
            } for rule in app.url_map.iter_rules() if rule.endpoint != 'static'}})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
