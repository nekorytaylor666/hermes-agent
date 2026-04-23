# Stage 1+: Visual Reference Generation

Generate reference images and create elements for consistent characters, locations, and props across all shots.

## Input

- `requirements.json` → characters, locations, props (with image_prompt / location_prompt)
- `storyboard.json` → which characters and locations are actually used
- Read `continuity.md` alongside this file

## Character Elements

### Generation + Element Creation

For each character in `requirements.json.content.characters`:

1. **Generate character image** using soul-cast via `/image-skill` (fire-and-forget, then poll for element creation):
   ```bash
   CREATED=$(higgsfieldcli generate --json '[{"model":"soul_cast","prompt":"<character image_prompt>","width":1152,"height":2048,"batch_size":1,"character_params":{"genre":"<genre>","budget":10}}]')
   JOB_ID=$(echo "$CREATED" | python3 -c "import sys,json; print(json.loads(sys.stdin.read().splitlines()[0])['job_ids'][0])")
   JOB_SET_TYPE=$(echo "$CREATED" | python3 -c "import sys,json; print(json.loads(sys.stdin.read().splitlines()[0])['job_set_type'])")
   # Poll until completed (needed for element creation)
   higgsfieldcli status --job-id "$JOB_ID" --poll
      ```

2. **Save** as `output/images/[character_name].png`

3. **Create element** from the result (reference type is `${JOB_SET_TYPE}_job`):
   ```bash
   higgsfieldcli element create \
     --category character --name "[CharacterName]" \
     --media "id=$JOB_ID;type=${JOB_SET_TYPE}_job"
   ```

4. **Record** the returned element ID in the element registry (see below).

No eye masking or upload needed when using elements — the backend handles references automatically.

## Location Elements

For each location in `requirements.json.content.locations`:

1. **Generate location image** using soul-location via `/image-skill` (fire-and-forget, then poll for element creation):
   ```bash
   CREATED=$(higgsfieldcli generate --json '[{"model":"soul_location","prompt":"<location_prompt>. ABSOLUTELY NO PEOPLE.","width":2048,"height":1152}]')
   JOB_ID=$(echo "$CREATED" | python3 -c "import sys,json; print(json.loads(sys.stdin.read().splitlines()[0])['job_ids'][0])")
   JOB_SET_TYPE=$(echo "$CREATED" | python3 -c "import sys,json; print(json.loads(sys.stdin.read().splitlines()[0])['job_set_type'])")
   # Poll until completed (needed for element creation)
   higgsfieldcli status --job-id "$JOB_ID" --poll
      ```

2. **Save** as `output/images/[location_id].png`

3. **Create element** (reference type is `${JOB_SET_TYPE}_job`):
   ```bash
   higgsfieldcli element create \
     --category environment --name "[LocationName]" \
     --media "id=$JOB_ID;type=${JOB_SET_TYPE}_job"
   ```

4. **Record** element ID in registry.

**ABSOLUTELY NO PEOPLE** in location images.

## Prop Elements

For each prop in `requirements.json.content.props` (if any):

1. **Invoke `/image-skill`** with a prompt:
   - `"[prop description]. Standalone product render, clean background, soft studio lighting. No people, no hands, no characters."`
   - Aspect ratio: `1:1`

2. **Save** as `output/images/[prop_id].png`

3. **Create element** (reference type is `${JOB_SET_TYPE}_job`):
   ```bash
   higgsfieldcli element create \
     --category prop --name "[PropName]" \
     --media "id=$JOB_ID;type=${JOB_SET_TYPE}_job"
   ```

## Element Registry

Maintain a registry for the entire session. Maps entity names to element IDs for use as `<<<element_id>>>` in prompts.

```
Characters:
  [CharacterName] → <<<element_id>>> (character)
  [CharacterName2] → <<<element_id>>> (character)
  ...

Locations:
  [loc_01] → <<<element_id>>> (environment)
  [loc_02] → <<<element_id>>> (environment)
  ...

Props:
  [prop_01] → <<<element_id>>> (prop)
  ...
```

Before EVERY shot in Stage 2, cross-reference `characters_present` and `location_id` against this registry. If any entity has no element ID → STOP → generate → create element → THEN proceed.

## Using Elements in Prompts

Embed `<<<element_id>>>` directly in the prompt text. The backend resolves each element automatically.

```bash
higgsfieldcli generate --json '[{"model":"seedance_2_0","prompt":"<<<char_element_id>>> walks through <<<loc_element_id>>>, dramatic lighting..."}]'
```

Multiple elements can be referenced in a single prompt.

## Character Sheet (Optional)

If the storyboard requires a character to appear from multiple angles, generate a character sheet:

1. Use the character's element in the prompt.
2. Invoke `/image-skill` with:
   ```
   <<<character_element_id>>> Character reference sheet. Three views in single horizontal row: back view full body,
   front view full body, close-up portrait. Same character, identical design/colors/details
   across all three views. No labels, numbers, text, or props. Softly blurred real-world
   background, extreme bokeh. Flat soft studio lighting from above.
   Match exact visual style, render quality, and color palette of input image.
   ```
3. Save as `output/images/[character_name]_sheet.png`

This is optional — use only when multi-angle consistency is critical.

## Listing Existing Elements

Check for previously created elements before generating new ones:

```bash
higgsfieldcli element list --category character
higgsfieldcli element list --category environment
```

## Completion

After all images are generated and elements are created:

1. Show the user a summary:
   ```
   Reference elements created:
   — [CharacterName]: [brief description] → <<<element_id>>> ✓
   — [CharacterName2]: [brief description] → <<<element_id>>> ✓
   — [location_name]: [brief description] → <<<element_id>>> ✓
   — [prop_name]: [brief description] → <<<element_id>>> ✓

   Ready to start generating video shots. Say "continue" to begin with Shot 1.
   ```

2. Proceed to Stage 2 when user confirms.
