import os
import uuid
from collections import defaultdict

import gym
from PIL import Image


class EnvironmentManager(object):
    """
    Environment Manager

    Control the environments that will be handled by the server.
    """

    TRAINING_DIRECTORY = "monitor/{}/simulation"
    RENDER_DIRECTORY = TRAINING_DIRECTORY + "/rendered/"

    def __init__(self):
        self.envs = {}
        self.render_counter = defaultdict(int)
        self.id_len = 8

    def create(self, env_id):
        """
        Create a new environment.

        :param env_id: Valid gym environment.
        :return: Instance ID
        """
        env = gym.make(env_id)
        instance_id = str(uuid.uuid4().hex)[:self.id_len]
        self.envs[instance_id] = env
        return instance_id

    def reset(self, instance_id, render=False):
        """
        Reset state of a given instance id.
        :param instance_id:
        :param render: render result of this operation.
        :return: Array of observations.
        """
        env = self.envs[instance_id]
        initial_state = {'observation': env.observation_space.to_jsonable(env.reset())}
        try:
            if render:
                self.render(instance_id)
                initial_state['render'] = 'successfully rendered: {}.png'.format(
                        self.render_counter[instance_id])
        except Exception as e:
            initial_state['render'] = 'Error: {}'.format(e.message)

        return initial_state

    def step(self, instance_id, action, render=False):
        """
        Execute action given by agent on the given environment
        :param instance_id: instance id of the environment
        :param action: action
        :param render: render result of this operation.
        :return: Dictionary with observation, reward, done flag and info.
        """
        env = self.envs[instance_id]

        action_from_json = int(env.action_space.from_jsonable(action))

        observation, reward, done, info = env.step(action_from_json)

        environment_response = {
            'observation': env.observation_space.to_jsonable(observation),
            'reward': reward,
            'done': done,
            'info': info
        }

        try:
            if render:
                self.render(instance_id)
                environment_response['render'] = 'successfully rendered: {}.png'.format(
                        self.render_counter[instance_id])
        except Exception as e:
            environment_response['render'] = 'Error: {}'.format(e.message)

        return environment_response

    def monitor_start(self, instance_id, force, resume):
        """
        Start Monitoring.

        The directory will be the same as the instace_id.

        The video will be available on the port server:8000/instance_id
        :param instance_id: instance id of the desired environment.
        :param force: Clear out existing training data from this directory (by deleting every file prefixed with "openaigym.").
        :param resume: Retain the training data already in this directory, which will be merged with our new data.
        :return:
        """
        env = self.envs[instance_id]

        directory = self.TRAINING_DIRECTORY.format(instance_id)

        env.monitor.start(directory, force=force, resume=resume)

    def monitor_close(self, instance_id):
        """
        Stop Monitor
        :param instance_id: instance id.
        :return: None.
        """
        env = self.envs[instance_id]
        env.monitor.close()

    def upload(self, instance_id, algorithm_id, writeup, api_key, ignore_open_monitors):
        """
        Upload training information created with monitor.
        :param instance_id: Id of the environment that was trained.
        :param algorithm_id: An arbitrary string indicating the paricular version of the algorithm
               (including choices of parameters) you are running.
        :param writeup: A Gist URL (of the form https://gist.github.com/<user>/<id>)
                        containing your writeup for this evaluation.
        :param api_key:  Your OpenAI API key. Can also be provided as an environment variable (OPENAI_GYM_API_KEY).
        :param ignore_open_monitors: Ignore open monitors when uploading.
        :return:
        """
        directory = self.TRAINING_DIRECTORY.format(instance_id)

        gym.upload(directory, algorithm_id, writeup, api_key,
                   ignore_open_monitors)

    def info(self, instance_id):
        """
        Expose useful information, such as: action_space, and observation_space.
        :param instance_id:
        :return:
        """
        env = self.envs[instance_id]
        return {
            'action_space': str(env.action_space),
            'observation_space': {
                'shape': env.observation_space.shape,
                'low': env.observation_space.low.tolist(),
                'high': env.observation_space.high.tolist()
            }
        }

    def render(self, instance_id):
        """
        Take a screenshot of the simulation.

        :param instance_id: id of the environment.
        :return:
        """
        env = self.envs[instance_id]

        if 'rgb_array' in env.metadata['render.modes']:
            render_mode = 'rgb_array'
        elif 'ansi' in env.metadata['render.modes']:
            render_mode = 'ansi'
        else:
            render_mode = None

        if render_mode is None:
            raise Exception("Environment does not support 'rgb_array' or 'ansi' renders.")

        directory = self.RENDER_DIRECTORY.format(instance_id)

        if not os.path.exists(directory):
            os.makedirs(directory)

        img = Image.fromarray(env.render(render_mode))
        img.save(directory + "{}.png".format(self.render_counter[instance_id]))

        self.render_counter[instance_id] += 1
