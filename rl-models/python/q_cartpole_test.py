import numpy as np
import pandas as pd
import gym
import math
from q import QLearn


def main(
    n_iters=3000,
    n_games_per_update=10,
    n_max_steps=1000,
    n_bins = 50):

    env = gym.make('CartPole-v0')
    model = QLearn(actions=range(2), alpha=0.5, gamma=0.95, epsilon=0.5)

    cart_p_bins = pd.cut([-2.4, 2.4], bins=n_bins, retbins=True)[1][1:-1]
    cart_v_bins = pd.cut([-2.0, 2.0], bins=n_bins, retbins=True)[1][1:-1]
    pole_a_bins = pd.cut([-math.radians(41.8), math.radians(41.8)], bins=n_bins, retbins=True)[1][1:-1]
    pole_v_bins = pd.cut([-3.0, 3.0], bins=n_bins, retbins=True)[1][1:-1]

    # training
    for iter in range(n_iters):
        finished_steps = []
        for game in range(n_games_per_update):
            obs = env.reset()
            cart_p, cart_v, pole_a, pole_v = obs
            state = build_state([to_bin(cart_p, cart_p_bins), to_bin(cart_v, cart_v_bins),
                                 to_bin(pole_a, pole_a_bins), to_bin(pole_v, pole_v_bins)])
            for step in range(n_max_steps):
                action = model.choose_action(state)
                obs, reward, done, info = env.step(action)
                cart_p, cart_v, pole_a, pole_v = obs
                next_state = build_state([to_bin(cart_p, cart_p_bins), to_bin(cart_v, cart_v_bins),
                                          to_bin(pole_a, pole_a_bins), to_bin(pole_v, pole_v_bins)])
                model.update_q(state, action, reward, next_state)
                state = next_state
                if done:
                    finished_steps.append(step)
                    break
        print("[%d / %d]: %.1f" % (iter, n_iters, (sum(finished_steps)/len(finished_steps)) ))    

    # testing
    obs = env.reset()
    cart_p, cart_v, pole_a, pole_v = obs
    state = build_state([to_bin(cart_p, cart_p_bins), to_bin(cart_v, cart_v_bins),
                         to_bin(pole_a, pole_a_bins), to_bin(pole_v, pole_v_bins)])
    done = False
    count = 0
    while not done:
        env.render()
        action = model.choose_action(state, training=False)
        obs, reward, done, info = env.step(action)
        cart_p, cart_v, pole_a, pole_v = obs
        state = build_state([to_bin(cart_p, cart_p_bins), to_bin(cart_v, cart_v_bins),
                             to_bin(pole_a, pole_a_bins), to_bin(pole_v, pole_v_bins)])
        count += 1
    print(count)


def build_state(features):
    return int("".join(map(lambda feature: str(int(feature)), features)))


def to_bin(value, bins):
    return np.digitize(x=[value], bins=bins)[0]


if __name__ == '__main__':
    main()