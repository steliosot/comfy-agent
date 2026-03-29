# Curated Workflows Library

This page lists the curated workflow skill library so users can quickly see what is available.

Total curated workflows: **120**

Each entry includes: purpose, input/output modality, model family hints, runtime profile, and one key warning.

## audio (8)

- `curated_ep47_acestep_v1_3_5b_music_to_music_instrumental`: **EP47 AceStep V1 3.5b music to music - Instrumental**
  I/O: audio -> audio/wav. Models: sd3. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Audio generation may take longer on CPU-only or low-VRAM servers.
- `curated_ep47_acestep_v1_3_5b_text_to_music_instrumental`: **EP47 AceStep V1 3.5b text to music - Instrumental**
  I/O: text_prompt -> audio/wav. Models: sd3. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Audio generation may take longer on CPU-only or low-VRAM servers.
- `curated_ep47_acestep_v1_3_5b_text_to_music_lyrics`: **EP47 AceStep V1 3.5b text to music - Lyrics**
  I/O: text_prompt -> audio/wav. Models: sd3. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Audio generation may take longer on CPU-only or low-VRAM servers.
- `curated_stability_ai_text_to_audio`: **Stability AI Text To Audio**
  I/O: text_prompt -> audio/wav. Models: other. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Audio generation may take longer on CPU-only or low-VRAM servers.
- `curated_stability_ai_text_to_audio_chatgpt_5_nano`: **Stability AI Text To Audio + ChatGPT 5 Nano**
  I/O: text_prompt -> audio/wav. Models: wan. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Audio generation may take longer on CPU-only or low-VRAM servers.
- `curated_vibevoice_1_5b_6gb_vram`: **VibeVoice 1.5B - 6GB VRAM**
  I/O: audio -> audio/wav. Models: other. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Audio generation may take longer on CPU-only or low-VRAM servers.
- `curated_vibevoice_q8_12gb_vram`: **VibeVoice Q8 - 12GB VRAM**
  I/O: audio -> audio/wav. Models: other. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Audio generation may take longer on CPU-only or low-VRAM servers.
- `curated_vibevoice_q8_multi_speaker_12gb_vram`: **VibeVoice Q8 MULTI Speaker - 12GB VRAM**
  I/O: audio -> audio/wav. Models: other. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Audio generation may take longer on CPU-only or low-VRAM servers.

## editing_restyle (18)

- `curated_05_z_image_turbo_txt2img_bf16_lora_style`: **05-Z Image Turbo txt2img bf16 + Lora style**
  I/O: text_prompt -> image/png. Models: qwen, sd3, z_image_turbo. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Medium-high resolution detected; expect moderate extra runtime.
- `curated_ep06_basic_sdxl_txt2img_with_styles_workflow`: **EP06 Basic SDXL TXT2IMG with STYLES Workflow**
  I/O: text_prompt -> image/png. Models: other. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Medium-high resolution detected; expect moderate extra runtime.
- `curated_ep06_basic_sdxl_txt2img_with_two_styles_workflow`: **EP06 Basic SDXL TXT2IMG with TWO STYLES Workflow**
  I/O: text_prompt -> image/png. Models: other. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Medium-high resolution detected; expect moderate extra runtime.
- `curated_ep07_basic_sdxl_txt2img_with_styles_workflow_updated`: **EP07 Basic SDXL TXT2IMG with STYLES Workflow Updated**
  I/O: text_prompt -> image/png. Models: other. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Medium-high resolution detected; expect moderate extra runtime.
- `curated_ep15_flux_dev_q8_gguf_txt2img_with_multi_styles`: **Ep15 Flux Dev Q8 GGUF TXT2IMG with Multi Styles**
  I/O: text_prompt -> image/png. Models: flux, sd3. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_ep15_sdxl_txt2img_with_multi_styles`: **Ep15 SDXL TXT2IMG with Multi Styles**
  I/O: text_prompt -> image/png. Models: other. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Medium-high resolution detected; expect moderate extra runtime.
- `curated_ep15_sdxl_txt2img_with_multi_styles_and_text_overlay`: **Ep15 SDXL TXT2IMG with Multi Styles and Text Overlay**
  I/O: text_prompt -> image/png. Models: other. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Medium-high resolution detected; expect moderate extra runtime.
- `curated_ep15_sdxl_txt2img_with_one_style`: **Ep15 SDXL TXT2IMG with One Style**
  I/O: text_prompt -> image/png. Models: other. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Medium-high resolution detected; expect moderate extra runtime.
- `curated_ep29_flux_dev_replace_complex_background`: **EP29 Flux Dev Replace Complex Background**
  I/O: image, text_prompt -> image/png. Models: flux. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_ep29_flux_dev_replace_simple_or_white_background`: **EP29 Flux Dev Replace Simple or White Background**
  I/O: image, text_prompt -> image/png. Models: flux. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_qwen_image_edit_replace_product_background`: **Qwen Image Edit - Replace Product Background**
  I/O: image -> image/png. Models: qwen. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_qwen_image_edit_replace_text`: **Qwen Image Edit - Replace Text**
  I/O: image -> image/png. Models: qwen. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_qwen_image_edit_restore_photo`: **Qwen Image Edit - Restore Photo**
  I/O: image -> image/png. Models: qwen. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_qwen_image_edit_transform_to_line_drawing`: **Qwen Image Edit - Transform to Line Drawing**
  I/O: image -> image/png. Models: qwen. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_qwen_image_edit_transform_to_pencil_drawing`: **Qwen Image Edit - Transform to Pencil Drawing**
  I/O: image -> image/png. Models: qwen. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_unified_style_flux_dev_fp8_1_style`: **Unified Style Flux Dev FP8 - 1 Style**
  I/O: image, text_prompt -> image/png. Models: flux, sd3. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Medium-high resolution detected; expect moderate extra runtime.
- `curated_unified_style_flux_dev_fp8_1_subject_1_style`: **Unified Style Flux Dev FP8 - 1 Subject +1 Style**
  I/O: image, text_prompt -> image/png. Models: flux, sd3. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Medium-high resolution detected; expect moderate extra runtime.
- `curated_unified_style_flux_dev_fp8_2_style_images`: **Unified Style Flux Dev FP8 - 2 Style Images**
  I/O: image, text_prompt -> image/png. Models: flux, sd3. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Medium-high resolution detected; expect moderate extra runtime.

## img2img_inpaint_outpaint (22)

- `curated_bytedance_seedream_4_img2img`: **ByteDance Seedream 4 - img2img**
  I/O: image -> image/png. Models: other. Runtime: low (fast (usually under 30s on modern GPU)). Warning: No major warnings detected.
- `curated_ep04_basic_sdxl_img2img_two_loras_workflow`: **EP04 Basic SDXL IMG2IMG TWO LORAS Workflow**
  I/O: text_prompt -> image/png. Models: sdxl. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Medium-high resolution detected; expect moderate extra runtime.
- `curated_ep18_sdxl_animationcartoon_img2img_with_controlnet`: **EP18 SDXL AnimationCartoon IMG2IMG with ControlNet**
  I/O: image, text_prompt -> image/png. Models: flux, wan. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_ep18_sdxl_realcartoon_img2img_with_controlnet`: **EP18 SDXL RealCartoon IMG2IMG with ControlNet**
  I/O: image, text_prompt -> image/png. Models: flux, wan. Runtime: low (fast (usually under 30s on modern GPU)). Warning: No major warnings detected.
- `curated_ep29_sdxl_inpaint_replace_complex_background`: **EP29 SDXL Inpaint Replace Complex Background**
  I/O: image, text_prompt -> image/png. Models: other. Runtime: low (fast (usually under 30s on modern GPU)). Warning: No major warnings detected.
- `curated_ep42_sd15_inpaint_epicrealism`: **EP42 SD15 INPAINT EpicRealism**
  I/O: image, text_prompt -> image/png. Models: other. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Uses custom nodes; missing nodes can cause validation/runtime failures.
- `curated_ep42_sd15_outpaint_epicrealism`: **EP42 SD15 OUTPAINT EpicRealism**
  I/O: image, text_prompt -> image/png. Models: other. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Uses custom nodes; missing nodes can cause validation/runtime failures.
- `curated_ep42_sdxl_inpaint_juggernaut`: **EP42 SDXL INPAINT Juggernaut**
  I/O: image, text_prompt -> image/png. Models: other. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Uses custom nodes; missing nodes can cause validation/runtime failures.
- `curated_ep42_sdxl_outpaint_juggernaut`: **EP42 SDXL OUTPAINT Juggernaut**
  I/O: image, text_prompt -> image/png. Models: other. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Uses custom nodes; missing nodes can cause validation/runtime failures.
- `curated_ep52_flux_1_kontext_dev_inpaint`: **EP52 Flux 1 Kontext Dev - Inpaint**
  I/O: image, text_prompt -> image/png. Models: flux. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Uses custom nodes; missing nodes can cause validation/runtime failures.
- `curated_ep52_flux_1_kontext_dev_inpaint_2`: **EP52 Flux 1 Kontext Dev - Inpaint-2**
  I/O: image, text_prompt -> image/png. Models: flux. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Uses custom nodes; missing nodes can cause validation/runtime failures.
- `curated_ep52_flux_1_kontext_dev_remove_items_with_inpaint_precise`: **EP52 Flux 1 Kontext Dev - Remove Items with Inpaint - Precise**
  I/O: image, text_prompt -> image/png. Models: flux. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Uses custom nodes; missing nodes can cause validation/runtime failures.
- `curated_ep52_flux_1_kontext_dev_replace_the_background_with_inpaint`: **EP52 Flux 1 Kontext Dev - Replace the Background with Inpaint**
  I/O: image, text_prompt -> image/png. Models: flux. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Uses custom nodes; missing nodes can cause validation/runtime failures.
- `curated_ep54_flux_dev_image_vector_variation`: **EP54 Flux Dev - Image Vector Variation**
  I/O: image, text_prompt -> image/png. Models: flux. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_ep54_flux_dev_nunchaku_image_vector_variation`: **EP54 Flux Dev (Nunchaku) - Image Vector Variation**
  I/O: image, text_prompt -> image/png. Models: flux. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Uses custom nodes; missing nodes can cause validation/runtime failures.
- `curated_google_gemini_image_nano_banana_img2img`: **Google Gemini Image - Nano Banana - img2img**
  I/O: image -> image/png. Models: other. Runtime: low (fast (usually under 30s on modern GPU)). Warning: No major warnings detected.
- `curated_nunchaku_qwen_edit_lightning_2509_inpaint`: **Nunchaku Qwen Edit Lightning 2509 - Inpaint**
  I/O: image -> image/png. Models: qwen. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Uses custom nodes; missing nodes can cause validation/runtime failures.
- `curated_nunchaku_qwen_edit_lightning_inpaint`: **Nunchaku Qwen Edit Lightning Inpaint**
  I/O: image -> image/png. Models: qwen. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Uses custom nodes; missing nodes can cause validation/runtime failures.
- `curated_nunchaku_qwen_lightning_control_net_inpainting`: **Nunchaku Qwen Lightning + Control Net Inpainting**
  I/O: image, text_prompt -> image/png. Models: qwen. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Uses custom nodes; missing nodes can cause validation/runtime failures.
- `curated_nunchaku_qwen_lightning_outpainting`: **Nunchaku Qwen Lightning - Outpainting**
  I/O: image, text_prompt -> image/png. Models: qwen. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Uses custom nodes; missing nodes can cause validation/runtime failures.
- `curated_nunchaku_qwen_lightning_outpainting_a_folder_of_images`: **Nunchaku Qwen Lightning - Outpainting a Folder of Images**
  I/O: image, text_prompt -> image/png. Models: qwen. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Multiple custom nodes required; verify node installation/version compatibility.
- `curated_qwen_image_edit_inpaint`: **Qwen Image Edit - Inpaint**
  I/O: image -> image/png. Models: qwen. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Large model(s) detected; ensure enough VRAM and disk space.

## txt2img (28)

- `curated_06_z_image_turbo_txt2img_bf16_qwenvl_image`: **06-Z Image Turbo txt2img bf16 + QwenVL Image**
  I/O: image, text_prompt -> image/png. Models: qwen, sd3, wan, z_image_turbo. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Medium-high resolution detected; expect moderate extra runtime.
- `curated_07_z_image_turbo_txt2img_bf16_qwenvl_text`: **07-Z Image Turbo txt2img bf16 + QwenVL Text**
  I/O: text_prompt -> image/png. Models: qwen, sd3, wan, z_image_turbo. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Medium-high resolution detected; expect moderate extra runtime.
- `curated_ep09_sdxl_txt2img_with_control_net_pose_workflow`: **EP09 SDXL TXT2IMG With Control Net Pose Workflow**
  I/O: image, text_prompt -> image/png. Models: sdxl. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Medium-high resolution detected; expect moderate extra runtime.
- `curated_ep09_sdxl_txt2img_with_control_net_workflow_canny_no_custom_nodes`: **EP09 SDXL TXT2IMG With Control Net Workflow - Canny - NO Custom Nodes**
  I/O: image, text_prompt -> image/png. Models: other. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Medium-high resolution detected; expect moderate extra runtime.
- `curated_ep09_sdxl_txt2img_with_control_net_workflow_dense_pose`: **EP09 SDXL TXT2IMG With Control Net Workflow - Dense Pose**
  I/O: image, text_prompt -> image/png. Models: other. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Medium-high resolution detected; expect moderate extra runtime.
- `curated_ep09_sdxl_txt2img_with_control_net_workflow_update`: **EP09 SDXL TXT2IMG With Control Net Workflow Update**
  I/O: image, text_prompt -> image/png. Models: other. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Medium-high resolution detected; expect moderate extra runtime.
- `curated_ep13_sdxl_txt2img_with_prompt_from_image`: **EP13 SDXL TXT2IMG with Prompt from Image**
  I/O: image, text_prompt -> image/png. Models: wan. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Medium-high resolution detected; expect moderate extra runtime.
- `curated_ep20_sdxl_sketch_2_image`: **EP20 SDXL Sketch 2 Image**
  I/O: image, text_prompt -> image/png. Models: flux, sd3, wan. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Medium-high resolution detected; expect moderate extra runtime.
- `curated_ep45_flux_dev_q8_gguf_with_controlnet_canny`: **Ep45 Flux Dev Q8 GGUF with ControlNet Canny**
  I/O: image, text_prompt -> image/png. Models: flux, sd3. Runtime: high (slow (often 2-6 min depending on model/server load)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_ep45_flux_dev_q8_gguf_with_controlnet_depth`: **Ep45 Flux Dev Q8 GGUF with ControlNet Depth**
  I/O: image, text_prompt -> image/png. Models: flux, sd3. Runtime: high (slow (often 2-6 min depending on model/server load)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_ep45_flux_dev_q8_gguf_with_controlnet_depth_dw_pose`: **Ep45 Flux Dev Q8 GGUF with ControlNet Depth + DW Pose**
  I/O: image, text_prompt -> image/png. Models: flux, sd3. Runtime: high (slow (often 2-6 min depending on model/server load)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_ep45_flux_dev_q8_gguf_with_controlnet_dw_pose`: **Ep45 Flux Dev Q8 GGUF with ControlNet DW Pose**
  I/O: image, text_prompt -> image/png. Models: flux, sd3. Runtime: high (slow (often 2-6 min depending on model/server load)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_ep45_flux_dev_q8_gguf_with_controlnet_dw_pose_lora`: **Ep45 Flux Dev Q8 GGUF with ControlNet DW Pose + Lora**
  I/O: image, text_prompt -> image/png. Models: flux, sd3. Runtime: high (slow (often 2-6 min depending on model/server load)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_ep45_fluxmania_v_with_controlnet_dw_pose`: **Ep45 Fluxmania V with ControlNet DW Pose**
  I/O: image, text_prompt -> image/png. Models: flux, sd3. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_hidream_i1_dev_q8_gguf_text2image`: **HiDream i1 Dev Q8 GGUF text2image**
  I/O: text_prompt -> image/png. Models: sd3. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_hidream_i1_fast_fp8_text2image`: **HiDream i1 Fast fp8 text2image**
  I/O: text_prompt -> image/png. Models: sd3. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Medium-high resolution detected; expect moderate extra runtime.
- `curated_hidream_i1_fast_q8_gguf_text2image`: **HiDream i1 Fast Q8 GGUF text2image**
  I/O: text_prompt -> image/png. Models: sd3. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_hidream_i1_full_fp8_text2image`: **HiDream i1 Full fp8 text2image**
  I/O: text_prompt -> image/png. Models: sd3. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Medium-high resolution detected; expect moderate extra runtime.
- `curated_hidream_i1_full_q8_gguf_text2image`: **HiDream i1 Full Q8 GGUF text2image**
  I/O: text_prompt -> image/png. Models: sd3. Runtime: high (slow (often 2-6 min depending on model/server load)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_nunchaku_qwen_lightning_control_net_depth`: **Nunchaku Qwen Lightning + Control Net Depth**
  I/O: image, text_prompt -> image/png. Models: qwen. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Uses custom nodes; missing nodes can cause validation/runtime failures.
- `curated_nunchaku_qwen_lightning_control_net_depth_canny`: **Nunchaku Qwen Lightning + Control Net Depth Canny**
  I/O: image, text_prompt -> image/png. Models: qwen. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Uses custom nodes; missing nodes can cause validation/runtime failures.
- `curated_nunchaku_qwen_lightning_control_net_pose`: **Nunchaku Qwen Lightning + Control Net Pose**
  I/O: image, text_prompt -> image/png. Models: qwen. Runtime: low (fast (usually under 30s on modern GPU)). Warning: Uses custom nodes; missing nodes can cause validation/runtime failures.
- `curated_nunchaku_qwen_lightning_txt2img_gpt5_nano_prompt`: **Nunchaku Qwen Lightning txt2img + GPT5 Nano Prompt**
  I/O: image, text_prompt -> image/png. Models: qwen, sd3, wan. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Medium-high resolution detected; expect moderate extra runtime.
- `curated_z_image_turbo_txt2img_bf16_cn_canny_2`: **Z Image Turbo txt2img bf16 CN Canny-2**
  I/O: image, text_prompt -> image/png. Models: qwen, sd3, z_image_turbo. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Medium-high resolution detected; expect moderate extra runtime.
- `curated_z_image_turbo_txt2img_bf16_cn_depth`: **Z Image Turbo txt2img bf16 CN Depth**
  I/O: image, text_prompt -> image/png. Models: qwen, sd3, z_image_turbo. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Medium-high resolution detected; expect moderate extra runtime.
- `curated_z_image_turbo_txt2img_bf16_cn_depth_2`: **Z Image Turbo txt2img bf16 CN Depth-2**
  I/O: image, text_prompt -> image/png. Models: qwen, sd3, z_image_turbo. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Medium-high resolution detected; expect moderate extra runtime.
- `curated_z_image_turbo_txt2img_bf16_cn_pose`: **Z Image Turbo txt2img bf16 CN Pose**
  I/O: image, text_prompt -> image/png. Models: qwen, sd3, z_image_turbo. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Medium-high resolution detected; expect moderate extra runtime.
- `curated_z_image_turbo_txt2img_bf16_cn_pose_2`: **Z Image Turbo txt2img bf16 CN Pose-2**
  I/O: image, text_prompt -> image/png. Models: qwen, sd3, z_image_turbo. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Medium-high resolution detected; expect moderate extra runtime.

## upscaling (16)

- `curated_ep27_sdxl_image_to_impressionism_oil_painting_with_lora_and_control_net_and_upscaler`: **EP27 SDXL Image to Impressionism Oil Painting with Lora and Control Net and UPSCALER**
  I/O: image, text_prompt -> image/png. Models: other. Runtime: low (fast (usually under 30s on modern GPU)). Warning: No major warnings detected.
- `curated_ep27_sdxl_image_to_oil_painting_with_lora_and_control_net_and_upscaler`: **EP27 SDXL Image to Oil Painting with Lora and Control Net and UPSCALER**
  I/O: image, text_prompt -> image/png. Models: other. Runtime: low (fast (usually under 30s on modern GPU)). Warning: No major warnings detected.
- `curated_ep27_sdxl_image_to_retro_painting_mix_with_lora_and_control_net_and_upscaler`: **EP27 SDXL Image to Retro Painting Mix with Lora and Control Net and UPSCALER**
  I/O: image, text_prompt -> image/png. Models: other. Runtime: low (fast (usually under 30s on modern GPU)). Warning: No major warnings detected.
- `curated_ep27_sdxl_image_to_watercolor_with_lora_and_control_net_and_upscaler`: **EP27 SDXL Image to Watercolor with Lora and Control Net and UPSCALER**
  I/O: image, text_prompt -> image/png. Models: sdxl. Runtime: low (fast (usually under 30s on modern GPU)). Warning: No major warnings detected.
- `curated_ep46_juggernaut_xl_ragnarok_txt2img_with_upscaler`: **EP46 Juggernaut XL Ragnarok TXT2IMG with Upscaler**
  I/O: text_prompt -> image/png. Models: flux, sd3, wan. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Medium-high resolution detected; expect moderate extra runtime.
- `curated_flux_img2img_with_cn_and_lora_and_upscaler_square_2048px_1_1`: **Flux img2img with CN and Lora and Upscaler - Square 2048px 1-1**
  I/O: image, text_prompt -> image/png. Models: flux. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_flux_txt2img_with_cn_and_lora_and_upscaler_square_2048px_1_1`: **Flux txt2img with CN and Lora and Upscaler - Square 2048px 1-1**
  I/O: image, text_prompt -> image/png. Models: flux, sd3. Runtime: high (slow (often 2-6 min depending on model/server load)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_fluxmania_txt2img_with_cn_depth_and_upscaler_portrait_instagram_1080x1350px_4_5`: **Fluxmania txt2img with CN Depth and Upscaler - Portrait Instagram 1080x1350px 4-5**
  I/O: image, text_prompt -> image/png. Models: flux, sd3. Runtime: high (slow (often 2-6 min depending on model/server load)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_fluxmania_txt2img_with_cn_depth_and_upscaler_square_2048px_1_1`: **Fluxmania txt2img with CN Depth and Upscaler - Square 2048px 1-1**
  I/O: image, text_prompt -> image/png. Models: flux, sd3. Runtime: high (slow (often 2-6 min depending on model/server load)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_fluxmania_txt2img_with_cn_pose_and_upscaler_portrait_full_hd_1080x1920px_9_16`: **Fluxmania txt2img with CN Pose and Upscaler - Portrait Full HD 1080x1920px 9-16**
  I/O: image, text_prompt -> image/png. Models: flux, sd3. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_fluxmania_txt2img_with_cn_pose_and_upscaler_portrait_instagram_1080x1350px_4_5`: **Fluxmania txt2img with CN Pose and Upscaler - Portrait Instagram 1080x1350px 4-5**
  I/O: image, text_prompt -> image/png. Models: flux, sd3. Runtime: high (slow (often 2-6 min depending on model/server load)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_fluxmania_txt2img_with_cn_pose_and_upscaler_square_2048px_1_1`: **Fluxmania txt2img with CN Pose and Upscaler - Square 2048px 1-1**
  I/O: image, text_prompt -> image/png. Models: flux, sd3. Runtime: high (slow (often 2-6 min depending on model/server load)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_netayume_v3_5_txt2img_upscaler`: **NetaYume v3.5 txt2img + Upscaler**
  I/O: text_prompt -> image/png. Models: flux, sd3, wan. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Medium-high resolution detected; expect moderate extra runtime.
- `curated_qwen_img2img_with_ligthing_lora_and_upscaler`: **Qwen img2img with Ligthing Lora and Upscaler**
  I/O: image, text_prompt -> image/png. Models: flux, qwen. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_qwen_txt2img_with_ligthing_lora_and_upscaler`: **Qwen txt2img with Ligthing Lora and Upscaler**
  I/O: text_prompt -> image/png. Models: flux, qwen, sd3, wan. Runtime: high (slow (often 2-6 min depending on model/server load)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_shuttle_jaguar_nunchaku_txt2img_with_upscaler`: **Shuttle Jaguar (Nunchaku) txt2img with Upscaler**
  I/O: text_prompt -> image/png. Models: flux, sd3. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Medium-high resolution detected; expect moderate extra runtime.

## video_t2v_i2v_avatar (28)

- `curated_ep28_liveportrait_expression_editor_with_flux_upscale`: **Ep28 LivePortrait Expression Editor with Flux Upscale**
  I/O: image, text_prompt -> image/png. Models: flux. Runtime: high (slow (often 2-6 min depending on model/server load)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_ep55_wan_2_1_i2v_480p_with_fusionx_lora`: **Ep55 Wan 2.1 I2V 480p with FusionX Lora**
  I/O: image, text_prompt -> video/mp4. Models: sd3, wan. Runtime: high (slow (often 2-6 min depending on model/server load)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_ep55_wan_2_1_i2v_480p_with_fusionx_lora_and_extra_lora`: **Ep55 Wan 2.1 I2V 480p with FusionX Lora and Extra Lora**
  I/O: image, text_prompt -> video/mp4. Models: sd3, wan. Runtime: high (slow (often 2-6 min depending on model/server load)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_longcat_img2video`: **LongCat img2video**
  I/O: image -> video/mp4. Models: wan. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Uses custom nodes; missing nodes can cause validation/runtime failures.
- `curated_longcat_img2video_5_to_30s_video`: **LongCat img2video - 5 to 30s Video**
  I/O: image -> video/mp4. Models: wan. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Uses custom nodes; missing nodes can cause validation/runtime failures.
- `curated_longcat_img2video_5_to_30s_video_no_subgraphs`: **LongCat img2video - 5 to 30s Video - No Subgraphs**
  I/O: image -> video/mp4. Models: wan. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Uses custom nodes; missing nodes can cause validation/runtime failures.
- `curated_longcat_img2video_easy_to_extend`: **LongCat img2video - Easy to Extend**
  I/O: image -> video/mp4. Models: wan. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Uses custom nodes; missing nodes can cause validation/runtime failures.
- `curated_longcat_txt2video`: **LongCat txt2video**
  I/O: text_prompt -> video/mp4. Models: wan. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Uses custom nodes; missing nodes can cause validation/runtime failures.
- `curated_ltx_0_95_image2video`: **LTX 0.95 image2video**
  I/O: image, text_prompt -> video/mp4. Models: ltx. Runtime: high (slow (often 2-6 min depending on model/server load)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_ltx_0_95_image2video_with_end_frame`: **LTX 0.95 image2video with End Frame**
  I/O: image, text_prompt -> video/mp4. Models: ltx. Runtime: high (slow (often 2-6 min depending on model/server load)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_ltx_0_95_image2video_with_middle_and_end_frame`: **LTX 0.95 image2video with Middle and End Frame**
  I/O: image, text_prompt -> video/mp4. Models: ltx. Runtime: high (slow (often 2-6 min depending on model/server load)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_ltx_0_95_image2video_with_multi_frames`: **LTX 0.95 image2video with Multi Frames**
  I/O: image, text_prompt -> video/mp4. Models: ltx. Runtime: high (slow (often 2-6 min depending on model/server load)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_ltx_0_95_text2video`: **LTX 0.95 text2video**
  I/O: text_prompt -> video/mp4. Models: ltx. Runtime: high (slow (often 2-6 min depending on model/server load)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_ltxv_13b_0_9_7_fp8_i2v_2frames_landscape_768x512px_to_1536x1024px`: **LTXV 13b 0.9.7-FP8 i2v 2Frames - Landscape 768x512px to 1536x1024px**
  I/O: image, text_prompt -> video/mp4. Models: ltx. Runtime: very_high (heavy (can exceed 6 min; best on high-VRAM GPU)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_ltxv_13b_0_9_7_fp8_i2v_extend_landscape_768x512px`: **LTXV 13b 0.9.7-FP8 i2v EXTEND Landscape 768x512px**
  I/O: image, text_prompt -> video/mp4. Models: ltx. Runtime: very_high (heavy (can exceed 6 min; best on high-VRAM GPU)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_ltxv_13b_0_9_7_fp8_i2v_landscape_768x512px_to_1536x1024px`: **LTXV 13b 0.9.7-FP8 i2v Landscape 768x512px to 1536x1024px**
  I/O: image, text_prompt -> video/mp4. Models: ltx. Runtime: very_high (heavy (can exceed 6 min; best on high-VRAM GPU)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_ltxv_13b_0_9_7_gguf_i2v_landscape_768x512px_to_1536x1024px`: **LTXV 13b 0.9.7-GGUF i2v Landscape 768x512px to 1536x1024px**
  I/O: image, text_prompt -> video/mp4. Models: ltx. Runtime: very_high (heavy (can exceed 6 min; best on high-VRAM GPU)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_qwenvl_video_to_text`: **QwenVL Video to Text**
  I/O: video -> application/json. Models: qwen, wan. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Uses custom nodes; missing nodes can cause validation/runtime failures.
- `curated_sonic_talking_avatar_landscape_1024x576px`: **Sonic Talking Avatar Landscape 1024x576px**
  I/O: audio, image -> image/png, video/mp4. Models: other. Runtime: high (slow (often 2-6 min depending on model/server load)). Warning: Audio generation may take longer on CPU-only or low-VRAM servers.
- `curated_video_upscale_landscape_full_hd_from_832x480px_to_1920x1080px`: **Video Upscale Landscape Full HD from 832x480px to 1920x1080px**
  I/O: video -> video/mp4. Models: wan. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Uses custom nodes; missing nodes can cause validation/runtime failures.
- `curated_video_upscale_square_640px_to_1920px`: **Video Upscale Square 640px to 1920px**
  I/O: video -> video/mp4. Models: wan. Runtime: medium (moderate (about 30-120s depending on server)). Warning: Uses custom nodes; missing nodes can cause validation/runtime failures.
- `curated_wan_2_2_i2i_14b_gguf_4_step_lora_upscale`: **Wan 2.2 I2I 14b GGUF + 4 Step Lora + Upscale**
  I/O: image, text_prompt -> image/png. Models: sd3, wan. Runtime: very_high (heavy (can exceed 6 min; best on high-VRAM GPU)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_wan_2_2_i2v_14b_gguf_lora`: **Wan 2.2 I2V 14b GGUF + Lora**
  I/O: image, text_prompt -> video/mp4. Models: sd3, wan. Runtime: very_high (heavy (can exceed 6 min; best on high-VRAM GPU)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_wan_2_2_i2v_14b_gguf_with_lora_included`: **Wan 2.2 I2V 14b GGUF with Lora Included**
  I/O: image, text_prompt -> video/mp4. Models: sd3, wan. Runtime: very_high (heavy (can exceed 6 min; best on high-VRAM GPU)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_wan_2_2_t2i_14b_gguf_4_step_lora_and_dslr_lora_upscale`: **Wan 2.2 T2I 14b GGUF + 4 Step Lora and DSLR Lora + Upscale**
  I/O: text_prompt -> image/png. Models: flux, sd3, wan. Runtime: very_high (heavy (can exceed 6 min; best on high-VRAM GPU)). Warning: High output resolution detected; generation time/memory use can increase significantly.
- `curated_wan_2_2_t2i_14b_gguf_4_step_lora_upscale`: **Wan 2.2 T2I 14b GGUF + 4 Step Lora + Upscale**
  I/O: text_prompt -> image/png. Models: flux, sd3, wan. Runtime: very_high (heavy (can exceed 6 min; best on high-VRAM GPU)). Warning: High output resolution detected; generation time/memory use can increase significantly.
- `curated_wan_2_2_t2i_14b_gguf_4_step_lora_upscale_insta_portrait`: **Wan 2.2 T2I 14b GGUF + 4 Step Lora + Upscale Insta Portrait**
  I/O: text_prompt -> image/png. Models: sd3, wan. Runtime: very_high (heavy (can exceed 6 min; best on high-VRAM GPU)). Warning: Large model(s) detected; ensure enough VRAM and disk space.
- `curated_wan_2_2_t2i_14b_gguf_4_step_lora_upscale_insta_portrait_dslr`: **Wan 2.2 T2I 14b GGUF + 4 Step Lora + Upscale Insta Portrait - DSLR**
  I/O: text_prompt -> image/png. Models: sd3, wan. Runtime: very_high (heavy (can exceed 6 min; best on high-VRAM GPU)). Warning: Large model(s) detected; ensure enough VRAM and disk space.

## Credits

Curated workflow references by [Pixaroma](https://pixaroma.com) and [Comfy Workflows](https://www.comfy.org/workflows/).
