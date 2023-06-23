from gymnasium.envs.registration import register

register(
     id="WcstSession-v0",
     entry_point="wcst_gym.wcst_session_gym:WcstSessionGym",
    #  max_episode_steps=300,
)