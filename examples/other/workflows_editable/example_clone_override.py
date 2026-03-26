from skills.generate_sd15_image.skill import build


wf = build(prompt="cinematic robot portrait")
wf2 = wf.clone().override({
    "ksampler.cfg": 12,
    "ksampler.steps": 30,
    "save.filename_prefix": "generated_override",
})

print("Original workflow:")
wf.inspect()

print("\nCloned and overridden workflow:")
wf2.inspect()

wf2.run()
