import torch
from misc.train_ppo import train
from unity_env import UnityEnv
from agent_ppo import Agent
from model import ReacherActorCritic

if __name__ == '__main__':
    #pylint: disable=invalid-name
    iterations = 2000
    gamma = 0.99
    timesteps = 100
    ratio_clip = 0.2
    batch_size = int(32*20)
    epochs = 10
    gradient_clip = 10.0
    lrate = 1e-4
    log_each = 10
    beta = 0.01
    gae_tau = 0.95
    decay_steps = None
    solved = 30.0
    out_file = 'saved_models/ppo.ckpt'

    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    env = UnityEnv(env_file='data/Reacher/Reacher.exe')
    policy = ReacherActorCritic(env.state_size, env.action_size).to(device)
    a = Agent(
        env,
        policy,
        timesteps=timesteps,
        gamma=gamma,
        epochs=epochs,
        batch_size=batch_size,
        ratio_clip=ratio_clip,
        lrate=lrate,
        gradient_clip=gradient_clip,
        beta=beta,
        gae_tau=gae_tau
    )

    train(a, iterations=iterations, log_each=log_each, 
          solved=solved, decay_steps=decay_steps, out_file=out_file)
