import uuid
import gym


class EnvironmentManager(object):
    """
    Environment Manager

    Control the environments that will be handled by the server.
    """
    def __init__(self):
        self.envs = {}
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

    def reset(self, instance_id):
        """
        Reset state of a given instance id.
        :param instance_id:
        :return: Array of observations.
        """
        env = self.envs[instance_id]
        obs = env.reset()
        return env.observation_space.to_jsonable(obs)

    def step(self, instance_id, action):
        """
        Execute action given by agent on the given environment
        :param instance_id: instance id of the environment
        :param action: action
        :return: Dictionary with observation, reward, done flag and info.
        """
        env = self.envs[instance_id]

        action_from_json = int(env.action_space.from_jsonable(action))

        try:
            observation, reward, done, info = env.step(action_from_json)

            environment_response = {
                'observation': env.observation_space.to_jsonable(observation),
                'reward': reward,
                'done': done,
                'info': info
            }

            return environment_response
        except gym.error.ResetNeeded as ex:
            return {'error': ex.message}

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

        directory = "monitor/{}".format(instance_id)

        env.monitor.start(directory, force=force, resume=resume)

    def monitor_close(self, instance_id):
        """
        Stop Monitor
        :param instance_id: instance id.
        :return: None.
        """
        env = self.envs[instance_id]
        env.monitor.close()

    def render(self, instance_id):
        env = self.envs[self.envs]

        render_mode = get_render_mode(env)




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
