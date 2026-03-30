# OPENCLAW Tester Prompts

Use this as a copy-paste test suite for OpenClaw.  
Each category has **5 prompts** with a mix of:
- direct execution prompts
- `/plan` prompts
- `/intent` prompts

## TXT2IMG (5)

1. `Generate one 1024x1024 cinematic photo of a rainy Tokyo alley at night, neon reflections, realistic lens blur.`
2. `/plan Create 3 hero image concepts for a fintech landing page (trust, speed, clarity), then execute and return best.`
3. `/intent Create branding moodboard image for a premium coffee brand, earthy palette, editorial style, product + lifestyle elements.`
4. `Generate 6 icon-style illustrations for a productivity app mascot, consistent style, white background.`
5. `/intent Generate poster key visual for "AI Design Summit 2026", space for headline text, high contrast, A3 portrait composition.`

## IMG2IMG (5)

1. `Use img2img on an input photo to convert it into watercolor painting style, preserve composition, output 1 high-quality result.`
2. `/plan Take an input portrait and produce 3 style variants: cinematic, magazine editorial, retro film. Execute all and compare.`
3. `/intent Transform a product photo into premium ad style (matte surfaces, soft shadows, luxury lighting), keep object shape accurate.`
4. `Use img2img to redesign an interior room photo into Japandi style, preserve layout, generate 2 options.`
5. `/intent Convert a sketch/logo draft image into clean polished concept art while preserving silhouette and structure.`

## TXT2VIDEO (5)

1. `Generate a 4-second video using a light model: abstract gradient flow, smooth loop, 16:9, lightweight settings.`
2. `/plan Create a 4-second product ad clip: rotating smartwatch on pedestal, studio lighting, 16 fps, then execute.`
3. `/intent Generate a 4-second cinematic background loop for a website hero section, subtle motion and no abrupt cuts.`
4. `Create 3 separate 4-second text-to-video clips for a perfume ad concept (close-up, wide shot, mood detail).`
5. `/intent Generate a 4-second social teaser video for a startup launch, modern tech aesthetic, minimal camera motion.`

## IMG2VIDEO (5)

1. `Use one portrait image to generate a 4-second subtle motion video (head movement + hair movement), keep identity consistent.`
2. `/plan Create 2 image-to-video variants from the same input image: slow push-in and orbit-like motion. Execute both.`
3. `/intent Turn a static product image into a 4-second ad motion clip with gentle parallax and premium lighting feel.`
4. `Generate a 4-second vertical (1080x1920) clip from one fashion image for reels, smooth motion, no deformation artifacts.`
5. `/intent Convert an illustration into a 4-second animated scene with light camera movement and stable style.`

## TXT2SOUND / TXT2AUDIO (5)

1. `Generate a 5-second simple instrumental clip with soft violins, emotional cinematic tone, no drums.`
2. `/plan Create 3 short 5-second sonic logos for a premium brand: violin-led, clean ending, then choose the best.`
3. `/intent Generate a 5-second audio sting with violins and light piano, modern luxury vibe, WAV output.`
4. `Create a 5-second ambient intro sound for a tech video, minimal, airy, subtle synth + string layer.`
5. `/intent Generate a 5-second calm background audio loop for a product showcase reel, smooth and unobtrusive.`

## COMBO / MULTI-SKILL / OPS (5)

1. `/plan Build and execute a 3-step pipeline: txt2img key visual -> upscale -> crop outputs for 1080x1350 and 1080x1920.`
2. `Match best curated workflow for "luxury skincare product ad", run it, and report selected skill + output path.`
3. `/intent Prepare workflow dependencies for a WAN video test, install missing model(s) if needed, then run a 4-second generation.`
4. `/plan Download and install one lightweight LoRA, run same prompt with and without LoRA, compare result quality and style.`
5. `Run cleanup test: remove a previously installed test model/LoRA, verify it no longer appears in model listings.`

## Optional Stress Tests (5)

1. `/plan Simulate missing dependency scenario: attempt generation, detect missing models/nodes, auto-fix, retry successfully.`
2. `/intent Run same prompt across 3 seeds and summarize variance in composition/style consistency.`
3. `Generate the same scene in txt2img and img2img pipelines and compare visual fidelity + prompt adherence.`
4. `/plan Execute 3 lightweight jobs in sequence (image, video, audio) and return a compact run summary table.`
5. `Use a low-VRAM-friendly setup to generate a valid output and document the parameters used for stability.`

---

## Tips

- Use direct prompts when you already know what to run.
- Use `/plan` when you want OpenClaw to reason first and then execute.
- Use `/intent` to test intent-routing behavior and automatic skill selection.
