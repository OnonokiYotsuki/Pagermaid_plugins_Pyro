EMOJI_CLOCK = [f"clock{h}" if m == 0 else f"clock{h}30" for h in range(1, 13) for m in range(0, 60, 30)]

print(EMOJI_CLOCK)