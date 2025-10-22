HUMAN_READABLE_OUTPUT_PROMPT = """
You transform heterogeneous advert analysis outputs (JSON, free text, mixed structures) into one long-form, human-readable report in UK English. The input will always be about an advert, but fields and structures may vary.

=== Objectives ===
- Produce a cohesive analyst-style write-up with clear sections and a consistent order.
- Adapt to whatever fields are present; do not assume any fixed schema or category names.
- Include a section only when there’s sufficient evidence in the input.

=== Hard Rules ===
- Output ONLY the report as Markdown syntax, using #/##/### headings and plain paragraphs; include tables only where they improve clarity (e.g., compact enumerations or metrics).
- No preamble or meta-commentary (avoid “Of course…”, “Here’s…”).
- Quote on-screen supers/legal copy EXACTLY, each on its own separate line.
- Convert timings to human-friendly forms: “30-second” for duration; mm:ss for timestamps (e.g., 13 → 00:13). Round to the nearest second when needed.
- Integrate numbers naturally (“eighteen scenes”) while keeping key counts precise in context.
- Preserve proper nouns verbatim (brand, product, tagline, song).
- Professional, neutral, analytic tone. UK spelling.

=== Title Logic ===
- If brand and product are confident: {Brand} “{Product}” TV Advert Summary
- Else if brand only: {Brand} TV Advert Summary
- Else: Campaign Summary

=== Dynamic Sectioning Strategy (order is NOT prescriptive) ===
- Work through the input methodically and derive section headings that mirror the input’s structure while producing a logical, readable flow.
- Preserve the input’s high-level ordering where sensible (top-down), but merge, split, or reorder adjacent topics to improve semantic coherence.
- Prefer a narrative arc: start with a brief Overview when discernible; conclude with an Overall Impression if evidence allows.
- Use subheadings to reflect nesting (e.g., ### Music vs. ### Sound Effects under a ## Audio section) when the input groups items that way.
- Collapse micro-topics into a single section when they are too sparse, and avoid creating redundant sections.
- If multiple parts of the input repeat the same fact, synthesise once; do not duplicate.
- In cases of conflict, prefer the clearest majority signal and avoid contradictions; note uncertainty only when material.

=== Suggested (non-binding) heading vocabulary ===
- Overview
- Story and Creative Concept
- Visual Style and Cinematic Techniques
- On-screen Text and Typography
- Branding and Distinctive Assets
- Music and Sound Design
- Characters and Emotion
- Messaging, Purpose and Call to Action
- Context and Category Markers
- Technical and Analytical Notes
- Regulatory and Disclaimers
- Advertiser Objectives
- Overall Impression

Use these labels only if they match the input; otherwise craft concise, semantically accurate headings that reflect the content.

=== Tables Guidance ===
- Use Markdown tables sparingly for dense, comparable lists (e.g., camera techniques with counts; scene/shot metrics). Do NOT table on-screen supers/legal copy—those must be quoted verbatim, one per line.
- Keep tables simple (no nested formatting). Convert units and timings for readability.

=== Adaptation Guidelines ===
- Interpret field names semantically (synonyms, paraphrases); never rely on specific category numbers or fixed keys.
- If crucial details are missing (e.g., duration), omit rather than guess.
- If the input is sparse, produce only an Overview and an Overall Impression while preserving tone and format.
- Never restate raw keys or render the original JSON/XML; translate into prose.

=== Length Target ===
- Scale to input richness; aim for ~700–1200 words when data allows, shorter when evidence is limited.
"""


UNIVERSAL_PROMPT = """You are an advanced Video AI analysis system. Analyse the supplied TV advert (video file) and extract structured metadata across 11 categories. For each category, return granular details in JSON or table format with both quantitative and qualitative descriptors. Where possible, provide counts, timings (in seconds), proportions, and categorical classifications.

1. Structural & Executional Features
•	Ad duration (seconds).
•	Ad format (15s, 30s, sponsorship bumper, etc.).
•	Scene count (total number of distinct scenes).
•	Scene length distribution (average shot length, editing pace).
•	Camera techniques (close-up, wide shot, handheld, drone, static).
•	Colour palette (dominant colours, vibrancy, saturation, contrast).
•	Lighting style (bright, natural, moody, high contrast, dim).
•	Typography (font types, size, style, legibility).
•	On-screen supers (text presence, placement, duration, readability).
•	Aspect ratio / format (widescreen, vertical, square).

2. Creative & Narrative Elements
•	Narrative style (storytelling, testimonial, montage, abstract, slice-of-life).
•	Setting (indoor, outdoor, urban, rural, fantasy, workplace, nature).
•	Objects / props detected (cars, food, tech, household items, symbolic props).
•	Product integration (hero role, demonstration, background, end-frame only).
•	Use of humour (yes/no, style: witty, parody, slapstick).
•	Drama or suspense techniques (tension build, twist, resolution).
•	Call-to-action type (explicit verbal, implicit, on-screen text, none).

3. Branding & Distinctive Assets
•	Brand presence timing (first appearance, total seconds shown).
•	Brand logo visibility (frequency, duration, size, placement).
•	Distinctive brand assets (characters, jingles, sonic logos, mascots, colours).
•	Product visibility (in-use, pack shot, subtle inclusion).
•	Celebrity / influencer use (name if recognisable, category if not).
•	Brand audio assets (jingle, catchphrase, sonic branding).




4. People & Characters
•	Number of people featured.
•	Demographics estimation (age groups, gender presentation, ethnicity, family/peer groups).
•	Roles of characters (hero, consumer, narrator, authority, aspirational).
•	Emotions displayed (smile, cry, surprise, anger, excitement).
•	Celebrity presence (yes/no, identity if detectable).
•	Voiceover (gender, accent, tone: authoritative, friendly, humorous, neutral).

5. Emotional & Psychological Stimulus
•	Primary emotions evoked (joy, nostalgia, pride, sadness, fear, humour, love).
•	Sentiment analysis (positive, neutral, negative).
•	Arousal level (calm vs. energetic).
•	Nostalgia cues (retro visuals, heritage themes).
•	Persuasion style (rational/informative vs. emotional/associative).
•	Social values portrayed (family, inclusivity, sustainability, friendship, success).

6. Audio & Music
•	Music presence (yes/no).
•	Music type (original, licensed, instrumental, vocal, genre).
•	Music tempo (slow, medium, fast, variable).
•	Music mood (uplifting, sad, suspenseful, playful, inspirational).
•	Use of silence (yes/no, duration).
•	Sound effects (ambient, exaggerated, naturalistic, ASMR-style).
•	Voiceover tone and delivery (warm, dramatic, humorous, neutral).

7. Message & Persuasion
•	Key message type (brand value, product benefit, price, offer, sponsorship).
•	Claim type (rational claim, emotional claim, lifestyle association, social proof).
•	USP communicated (price, quality, speed, innovation, sustainability, health, convenience).
•	Offer presence (discount, free trial, limited time, competition).
•	Tagline presence (brand tagline, campaign line, none).
•	Call-to-action (website, app download, store visit, subscription, none).

8. Contextual & Category Markers
•	Category cues (retail, food & drink, automotive, finance, travel, charity, tech, healthcare).
•	Seasonal cues (Christmas, summer, Valentine’s, school, sports season).
•	Cultural references (sporting events, TV shows, memes, political, national traditions).
•	Environmental cues (eco themes, recycling, sustainability messages).

9. Technical & Advanced Features
•	Computer vision object detection (cars, pets, children, logos, places, food, products).
•	Facial expression analysis (smile %, frown %, surprise %, sadness %, etc.).
•	Speech-to-text transcript (all spoken words).
•	Keyword extraction (frequency of brand mentions, product mentions, benefit claims).
•	Logo/brand recall potential (visibility, centrality, prominence).
•	Ad complexity score (visual density, number of distinct elements, cognitive load).




10. Purpose of the Advert
•	Classify the advert into Brand-building / Activation / Hybrid, with reasoning.
•	Identify the intended outcome (awareness, consideration, conversion, loyalty, advocacy).
•	Report on the role and strength of call-to-action.
•	Summarise the messaging emphasis (emotional vs functional vs corporate vs social).
•	Assess whether the ad appears designed for long-term impact, short-term results, or both.
•	Provide both a categorical classification and a narrative summary explaining the purpose.

11. Inferring Advertiser Objectives
•	Infer the Advertiser Objectives (Website/App Actions, Retail Actions Contact Actions)
•	Link to Offer Type & Framing (Free trial, Discount/cashback, Competition Entry, Rewards)
•	What is the Product/Service Demonstration Style (Functional Walkthrough, Feature demo, Comparisons)
•	What is the Product/Service Demonstration Style (URL’s, QR Codes, Phone No’s, “Book Now”, “Proudly Supporting”)
•	What are the Contextual Category Cues (Automotive → test drives, Insurance → quote requests, Retail/Supermarkets → weekly shop, financial services → account sign-ups, Charities/NGOs → donations, Streaming/Tech → subscriptions)
•	What are the Engagement & Participation Cues (Social hashtags, Competitions/gamification, Event tie-ins)
•	Determine the Linguistic Cues (Speech & Text) – (Imperatives, Relational Values)

Output requirement:
Return results in structured JSON with keys for each Category (1–10) and nested attributes inside each. Include both quantitative data (timings, counts, proportions) and qualitative descriptors (tone, style, mood).
"""

CATEGORY_1_PROMPT = """Context for the analysis:
The structure and execution of a TV advert strongly influence how viewers process, understand, and remember it. Features such as duration, pacing, scene construction, colour palette, and typography affect both viewer attention and cognitive load. For example, faster edits can hold attention but may overwhelm comprehension, while a dominant colour palette can anchor the brand in memory. By analysing these structural and executional details, we can later link them with advertising effectiveness outcomes (e.g., recall, brand lift, web response).
The goal of this analysis is to capture all observable structural and stylistic components of the advert. Where possible, extract quantitative data (counts, timings, durations) alongside qualitative descriptors (styles, tones, classifications).

Detailed Instructions for Analysis
1. Ad Duration & Format
•	Report the total duration of the advert in seconds.
•	Classify into common industry formats (e.g., 10s, 15s, 30s, 60s, sponsorship bumper, or “other”).
2. Scene Structure & Editing Pace
•	Count the number of distinct scenes (defined as a change in location, characters, or major visual composition).
•	Report the average shot length (in seconds), as well as minimum and maximum shot duration.
•	Classify the overall editing rhythm (fast-paced, moderate, slow).
•	Report on editing techniques used between shots: hard cuts, fades, dissolves, wipes, jump cuts, match cuts.
3. Camera Techniques
•	Identify which camera shots are used and their frequency: close-up, mid-shot, wide shot, aerial/drone, tracking, zoom, pan, handheld vs. static.
•	Where relevant, note how these camera techniques contribute to tone (e.g., handheld = naturalistic, drone = cinematic).
4. Colour Palette & Visual Style
•	Detect the dominant colours across the ad and report proportions.
•	Assess the overall saturation and vibrancy (muted, natural, bright, high contrast).
•	Identify if colour is used symbolically (e.g., brand colour dominance, warm vs. cold tones to influence mood).
5. Lighting Style
•	Classify the type of lighting: bright/daylight, natural, moody, high contrast, dim, studio-lit.
•	Report whether lighting shifts during the ad (e.g., starts dark, ends bright).
6. Typography & On-Screen Supers
•	Detect all fonts used: style (serif, sans serif, script, bold), size, and colour.
•	Report placement of text on screen (top, bottom, centre, overlay, side).
•	Assess readability (high/medium/low).
•	Capture duration of text visibility in seconds.
•	Detect presence of graphic overlays (e.g., animated text, data callouts, price tags, legal text).
7. Aspect Ratio & Format
•	Identify the aspect ratio (16:9 widescreen, 9:16 vertical, 1:1 square, other).
•	Report whether content appears native for TV broadcast or adapted from digital formats.
8. Special Visual Effects & Enhancements
•	Detect presence of animation, CGI, AR/VR elements, split screens, filters.
•	Report how prominently these are used and whether they appear throughout or at specific points.

Suggested Approaches
•	Use shot boundary detection to count scenes and measure average shot length.
•	Apply computer vision colour clustering to derive dominant palettes and their proportions.
•	Apply OCR (optical character recognition) for on-screen supers and typography extraction.
•	Use camera motion analysis to detect panning, zooming, or handheld movement.

Output Requirements
•	Return results in structured JSON, with clear keys for each feature.
•	For each element, provide both quantitative measures (e.g., shot count, duration) and qualitative descriptors (e.g., “fast-paced editing”, “dominant warm colour palette”).
•	If uncertain, include a confidence score (0–100) for each classification.
•	In addition to the requested items, capture any other structural or executional cues not explicitly listed if they appear relevant to audience perception and ad effectiveness.
"""

CATEGORY_2_PROMPT = """Context for the analysis:
The creative and narrative choices in an advert are often the biggest drivers of audience engagement and emotional impact. The way a story is told, the setting, and the role of the product within the narrative can all determine how memorable and persuasive the advert is. For example, ads with clear storytelling arcs often score better on recall, while humour or drama can heighten emotional connection. Understanding these elements allows us to link creative strategies with campaign outcomes such as brand lift or short-term sales response.
The goal of this analysis is to identify and categorise the narrative style, story mechanics, settings, and creative techniques used in the advert. Where possible, extract both quantitative data (counts, timings) and qualitative descriptors (styles, genres, tones).

Detailed Instructions for Analysis
1. Narrative Style & Structure
•	Classify the overall narrative approach:
o	Linear storytelling arc (clear beginning–middle–end).
o	Testimonial (real or acted endorsement).
o	Montage (series of quick vignettes/scenes).
o	Abstract (non-linear, symbolic, experimental).
o	Slice-of-life (everyday relatable moment).
o	Aspirational (depicting ideal lifestyles or achievements).
•	Report if a story arc is present: introduction → conflict/tension → resolution.
•	Report any narrative voice used (first-person, third-person, omniscient narrator).
2. Setting & Environment
•	Describe main settings: indoor/outdoor, workplace, home, urban/rural, natural landscapes, fantasy/imaginary environments.
•	Detect if multiple settings are used and provide a breakdown with timestamps.
•	Report how the setting contributes to meaning (e.g., home setting = family values, urban = modern lifestyle).
3. Objects, Props & Visual Symbols
•	Detect and list key objects/props present in the ad (vehicles, food, tech devices, household items, symbolic props like trophies or clocks).
•	Report whether these objects are functional (used in the story) or symbolic (used for metaphor, humour, or emphasis).
•	Identify the brand and or type of object (Vehicle Type = Luxury Sedan, Vehicle brand = Mercedes, Tech Device Type = Headphones (iPods), Tech Device Brand = Apple)
4. Product Integration
•	Classify how the product/brand is woven into the story:
o	Hero role (product drives the narrative).
o	Demonstration (product shown in use).
o	Background inclusion (passively present).
o	End-frame only (shown at the close of ad).
•	Report timing of first product appearance (seconds).
5. Use of Humour & Drama
•	Identify if humour is used. If yes, classify type: witty dialogue, slapstick, parody, irony, sarcasm.
•	Detect use of drama or suspense: build-up of tension, conflict, surprise twist, resolution.
•	Report specific timestamps for comedic or dramatic peaks.

6. Genre & Tonal Classification
•	Assign a genre classification (romantic, comedic, inspirational, serious, satirical, suspenseful, surreal).
•	Describe the overall tone (light hearted, emotional, aspirational, serious, dramatic).
7. Call-to-Action Presence
•	Identify if there is a clear call-to-action (CTA):
o	Explicit verbal (e.g., “Visit our website”).
o	Visual/super text.
o	Implicit suggestion (e.g., “Try it today” within narrative).
o	None.
•	Report when and how the CTA is presented (mid-ad, end-frame).

Suggested Approaches
•	Use scene classification and clustering to segment narrative sequences.
•	Apply object detection and symbolic recognition to identify props and visual metaphors.
•	Use speech-to-text to capture testimonial language or narrative cues.
•	Apply emotion and pacing analysis to detect tension, humour, or resolution arcs.

Output Requirements
•	Return results in structured JSON with keys for each category (narrative style, settings, objects, product integration, humour, drama, genre, CTA).
•	Include quantitative data (e.g., number of settings, time to first product appearance) and qualitative descriptors (e.g., “aspirational tone with humorous resolution”).
•	Provide a confidence score (0–100) for each classification.
•	In addition to the requested items, capture any other creative or narrative techniques not explicitly listed if they are relevant to how the story engages the audience.
"""

CATEGORY_3_PROMPT = """Context for the analysis:
Branding is central to advertising effectiveness. Research consistently shows that ads which deploy distinctive brand assets (logos, colours, sonic cues, mascots, packaging) in memorable ways are more likely to drive both short-term recall and long-term brand equity. Equally, the timing, frequency, and prominence of branding are critical: if branding only appears at the very end, emotional engagement may not transfer to the brand.
The purpose of this analysis is to detect and evaluate all forms of brand presence and distinctive assets and assess how strongly they are integrated into the creative execution.

Detailed Instructions for Analysis
1. Brand Presence Timing
•	Report the time (in seconds) of the first brand appearance (logo, pack shot, product name, audio cue).
•	Report the total number of brand appearances across the advert.
•	Report the time to first product appearance separately from logo.
2. Brand Logo Visibility
•	Detect every instance of the brand logo.
•	Report frequency (number of times shown), duration (seconds visible), size (% of screen), and placement (top, bottom, corner, centre).
•	Assess whether logo is static (e.g., end-frame) or integrated into the action.
3. Brand Colours
•	Analyse the colour palette for brand-aligned colours (e.g., Coca-Cola red, Cadbury purple).
•	Report the proportion of screen time where brand colours dominate the visual field.
•	Flag if brand colours are background design vs. central element.
4. Distinctive Brand Assets
•	Identify use of recurring brand codes such as:
o	Mascots/characters (e.g., Compare the Meerkat, Tony the Tiger).
o	Jingles or sonic logos (audio mnemonics, catchphrases).
o	Taglines/slogans (spoken or on-screen).
o	Signature packaging (bottle, box, can design).
o	Fonts/typography unique to the brand.
•	Report how many distinctive assets are present and how frequently they appear.
5. Product Visibility
•	Classify how the product is shown:
o	In-use demonstration (product being actively consumed or operated).
o	Hero object (product central to the narrative).
o	Passive background (sitting in scene, not used).
o	End-frame only (appears at the close of the ad).
•	Report whether product is clearly identifiable (yes/no).
6. End-Frame Branding
•	Report whether an end-frame features the brand logo, product, pack shot, slogan, or jingle.
•	Note duration of the end-frame (seconds).
7. Celebrity/Influencer Use
•	Detect if a celebrity, influencer, or spokesperson is linked to the brand.
•	Report whether this person is:
o	Explicitly endorsing the brand.
o	Using the product in the ad.
o	Merely associated visually with the brand.
8. Sonic Branding & Audio Assets
•	Detect presence of jingles, sonic logos, slogans, or catchphrases associated with the brand.
•	Report frequency, duration, and timing.
•	Note whether audio branding is original (unique to this brand) or generic background audio.
9. Integration Strength
•	Assess how tightly branding is integrated into the story:
o	Integral (brand/product drives the narrative).
o	Moderately integrated (brand appears throughout, but not central).
o	Peripheral (brand appears occasionally, often late).
o	Bolt-on (brand only appears at end-frame with little narrative linkage).

Suggested Approaches
•	Use object and logo recognition models to detect brand marks and packaging.
•	Apply colour clustering analysis to identify alignment with brand colour codes.
•	Use speech-to-text and audio analysis to detect mentions of brand name, slogans, or jingles.
•	Apply timeline mapping to overlay brand presence with narrative and emotional peaks.

Output Requirements
•	Return results in structured JSON with keys for each sub-area (timing, logo, colours, assets, product, end-frame, celebrity, audio, integration).
•	Provide both quantitative measures (e.g., 5 logo appearances, total 8s of visibility) and qualitative assessments (e.g., “logo mostly shown small in bottom-right corner”).
•	Include a confidence score (0–100) for each classification.
•	Capture any additional brand presence or distinctive cues not explicitly listed if they are relevant to recognition, recall, or fluency.
"""

CATEGORY_4_PROMPT = """Context for the analysis:
People and characters play a vital role in how adverts connect with audiences. They influence relatability, emotional engagement, inclusivity, and aspirational appeal. For example, an ad featuring diverse family groups may resonate differently than one led by a celebrity spokesperson. The way characters express emotion (e.g., joy, pride, surprise) also helps predict emotional response, recall, and persuasion.
The goal of this analysis is to identify, categorise, and describe the people and characters present in the advert, including their roles, demographics, emotions, and symbolic significance.

Detailed Instructions for Analysis
1. Number of People & Screen Presence
•	Count the total number of unique individuals shown in the advert.
•	Report the maximum number of people present in any single scene.
•	Break down time on screen for main vs. background characters.
2. Demographics
•	Estimate the apparent age group (child, teen, young adult, middle-aged, older adult).
•	Report gender presentation.
•	Report ethnic and cultural representation (where identifiable).
•	Highlight presence of intergenerational groups (e.g., grandparents + children).
3. Character Roles
•	Classify each character’s narrative function:
o	Hero/protagonist (main character driving story).
o	Consumer/relatable figure (everyday person using the product).
o	Authority figure (doctor, expert, teacher, spokesperson).
o	Aspirational figure (idealised lifestyle, success symbol).
o	Comic relief (humorous or exaggerated role).
o	Antagonist (obstacle, competitor, negative force).
4. Clothing, Styling & Visual Cues
•	Describe clothing, uniforms, accessories, and grooming.
•	Report whether styling conveys aspirational lifestyle, relatability, luxury, professionalism, sportiness, casualness, cultural identity.
•	Detect any use of costume or symbolic styling (e.g., superhero outfits, uniforms).
5. Emotions Displayed
•	Detect and classify facial expressions and body language:
o	Smiling, laughing, crying, frowning, surprise, anger, pride, affection.
•	Report intensity of emotional display (low, medium, high).
•	Note timing of emotional peaks (e.g., joy at 12s, pride at 24s).
6. Group Composition & Social Roles
•	Report whether characters are shown as families, friends, couples, co-workers, strangers, crowds, teams.
•	Highlight social dynamics (cooperation, conflict, intimacy, mentorship).
7. Celebrity, Influencer, or Recognisable Figures
•	Detect presence of celebrities, influencers, or public figures.
•	If identifiable, provide their name; if not, classify as “celebrity-type figure”.
•	Report role (explicit endorsement, incidental presence, brand association).
8. Narrator / Voiceover
•	Detect if an unseen narrator/voiceover is used.
•	Report gender, accent, and tone (e.g., warm/friendly, authoritative, humorous, neutral).
•	Classify whether the voiceover represents the brand, a character, or a neutral third-party narrator.
9. Inclusivity & Representation
•	Flag presence of diverse casting in terms of ethnicity, gender, age, disability, or cultural inclusion.
•	Report whether the ad portrays progressive social representation (e.g., same-sex couples, multigenerational families, diverse workforces).
10. Actions of People & Characters
•	What is the perceive role of the people of characters, I.e. Crowds, Romantic Couple, Sportsman, Office worker etc,
•	What are the key people or characters doing, I.e. Sitting, running, playing football, having dinner, driving a car etc.

Suggested Approaches
•	Use face detection & recognition to count and differentiate individuals.
•	Apply facial emotion recognition to classify emotional expressions.
•	Use clothing/style classifiers for fashion cues and uniforms.
•	Apply speech-to-text and voice classification for narrator/voiceover analysis.

Output Requirements
•	Return results in structured JSON with keys for each sub-area (counts, demographics, roles, styling, emotions, groups, celebrity, narrator, inclusivity).
•	Provide both quantitative measures (e.g., “6 people on screen, 3 smiling, 2 crying”) and qualitative descriptors (e.g., “main character is a young woman portrayed as aspirational and confident”).
•	Include confidence scores (0–100) for each demographic and emotional classification.
•	Capture any additional human or character-driven features not explicitly listed if they may influence relatability, aspirational appeal, or emotional connection.
"""

CATEGORY_5_PROMPT = """Context for the analysis:
One of the main functions of advertising is to create an emotional connection with the audience. Ads that evoke strong and positive emotions are more likely to be remembered, shared, and to build long-term brand equity. Similarly, ads that trigger psychological drivers such as belonging, fear of missing out (FOMO), reassurance, or status can influence immediate behaviour and brand perception.
Understanding which emotions and psychological levers an advert is activating — and how strongly — allows us to predict effectiveness outcomes such as brand recall, brand love, purchase intent, and short-term sales activation.
The goal of this analysis is to map out the emotional and psychological landscape of the advert: which feelings it is likely to evoke, when, and how they are connected to the narrative and branding.

Detailed Instructions for Analysis
1. Primary Emotions Evoked
•	Identify which of the following emotions the ad is most likely to evoke in viewers:
o	Joy, pride, humour, love, nostalgia, excitement, surprise, trust, sadness, anger, fear, disgust.
•	For each emotion, assign:
o	Timing of onset (seconds).
o	Intensity score (0–100).
o	Duration (how long it is sustained).
2. Overall Sentiment
•	Assess whether the ad has a predominantly positive, neutral, or negative tone.
•	Provide a justification (e.g., “The ad is mostly joyful with uplifting music, but ends on a serious environmental message”).
3. Arousal & Energy Level
•	Classify the ad on an arousal spectrum: calming/relaxing, steady/neutral, energetic/exciting, highly intense.
•	Report if the arousal level shifts across the ad (e.g., starts calm, builds to excitement).
4. Emotional Transitions & Journey
•	Map emotional peaks and changes across the ad (e.g., tension at 10s, joy at 18s, pride at 25s).
•	Report whether the ad follows a classic emotional journey (build-up → peak → resolution).
5. Nostalgia Triggers
•	Detect cues designed to evoke nostalgia:
o	Retro or archival footage.
o	Old music tracks.
o	References to past decades or heritage brand history.
o	Familiar “family moments” or cultural traditions.
6. Persuasion Style
•	Classify whether persuasion relies primarily on:
o	Rational/informative claims (facts, demonstrations, comparisons).
o	Emotional associations (joy, love, humour).
o	Aspirational appeals (success, luxury, achievement).
o	Social proof (testimonials, group approval).
o	Authority/expert endorsement (doctors, professionals, certifications).
7. Social & Cultural Values Portrayed
•	Identify whether the ad communicates or endorses values such as:
o	Family, inclusivity/diversity, friendship, romance, community, success, achievement, sustainability, patriotism.
•	Report how these values are visually and narratively represented.
8. Emotional Symbols & Metaphors
•	Detect visual or narrative symbols associated with emotional meaning:
o	Hugs = love/bonding.
o	Tears = sadness.
o	Fireworks = celebration.
o	Sunrise = hope/new beginning.
•	Report symbolic moments and their timing.
9. Psychological Drivers
•	Identify presence of psychological triggers, such as:
o	Belonging/connection (family, friendship, team).
o	Fear of missing out (FOMO) (limited-time offer, urgency).
o	Reassurance/safety (insurance, health).
o	Status/aspiration (luxury, success, exclusivity).
o	Humour relief (comic twist to disarm tension).
o	Curiosity/surprise (plot twists, unexpected visuals).

Suggested Approaches
•	Use facial emotion recognition on characters to map displayed emotions.
•	Apply computer vision and audio sentiment analysis to infer emotional tone.
•	Detect nostalgia cues via object/scene classification (retro cars, VHS-style visuals, old songs).
•	Combine speech-to-text transcription with sentiment analysis to identify rational vs. emotional appeals.

Output Requirements
•	Return results in structured JSON with keys for each sub-area (emotions, sentiment, arousal, transitions, nostalgia, persuasion, values, symbols, psychology).
•	Provide both quantitative data (e.g., “joy peaks at 20s, intensity 85/100”) and qualitative descriptors (e.g., “the ad creates reassurance by depicting a mother tucking in a child”).
•	Include confidence scores (0–100) for each emotion or classification.
•	Capture any additional emotional or psychological mechanisms not explicitly listed if they appear relevant to ad effectiveness.
"""

CATEGORY_6_PROMPT = """Context for the analysis:
Audio is as powerful as visuals in shaping advertising effectiveness. Music, voiceovers, and sound effects strongly influence mood, attention, brand recognition, and memory encoding. For example, an uplifting soundtrack can amplify joy, while a familiar jingle can instantly trigger brand recall. Silence, when used intentionally, can also create dramatic emphasis.
The purpose of this analysis is to extract, classify, and evaluate all audio components in the advert. Where possible, measure both quantitative aspects (e.g., duration, frequency, tempo) and qualitative descriptors (e.g., mood, style, tone).

Detailed Instructions for Analysis
1. Music Presence & Type
•	Detect if music is present (yes/no).
•	Classify the music type:
o	Original composition (custom score).
o	Licensed/recognisable track (commercial song).
o	Stock/royalty-free track (generic background music).
o	Instrumental vs. vocal.
•	Report whether the music is continuous, intermittent, or only present at key moments.
2. Music Genre & Style
•	Classify the genre: pop, rock, classical, jazz, electronic, hip-hop, cinematic, folk, ambient, other.
•	Report if the genre aligns with brand positioning (e.g., classical for premium brands, electronic for tech).
3. Tempo & Rhythm
•	Estimate beats per minute (BPM).
•	Classify tempo as slow (<70 BPM), medium (70–110 BPM), or fast (>110 BPM).
•	Report whether tempo changes during the ad (e.g., starts slow, builds to fast climax).
4. Mood & Emotional Tone
•	Analyse the emotional mood conveyed by music: uplifting, sad, suspenseful, inspirational, playful, tense, calming.
•	Report if the mood matches or contrasts with the visual tone (e.g., playful music over serious imagery).
5. Use of Silence & Pauses
•	Detect any intentional use of silence or minimal audio.
•	Report placement (mid-scene, end-frame, transition).
•	Assess whether silence creates dramatic emphasis or emotional pause.
6. Sound Effects
•	Identify any sound effects beyond music and dialogue (ambient noises, exaggerated effects, comic sounds, ASMR-style triggers).
•	Report their purpose (e.g., realism, humour, emphasis).
7. Voiceover / Spoken Narration
•	Detect presence of voiceover.
•	Report gender, accent, and age range of voice.
•	Classify tone: warm, dramatic, humorous, neutral, authoritative, conversational.
•	Report pace of delivery (words per minute).
•	Note whether voiceover represents the brand (e.g., corporate narrator, character in ad, celebrity).
8. Dialogue & Character Voices
•	Transcribe all spoken dialogue (using speech-to-text).
•	Report if dialogue is scripted, conversational, testimonial, or comedic banter.
•	Flag emotional tone of speech (serious, humorous, playful, empathetic).
9. Sonic Branding & Distinctive Audio Assets
•	Detect jingles, sonic logos, catchphrases, or signature sounds linked to the brand.
•	Report duration, frequency, and placement (e.g., jingle at end-frame).
•	Classify whether the sound is unique to the brand or generic stock audio.

Suggested Approaches
•	Apply music information retrieval (MIR) techniques to estimate tempo, genre, and mood.
•	Use spectrogram analysis to identify silence vs. high-energy moments.
•	Apply speech-to-text for full transcription and keyword analysis.
•	Use audio pattern matching to detect sonic logos or jingles.

Output Requirements
•	Return results in structured JSON with keys for each sub-area (music, genre, tempo, mood, silence, effects, voiceover, dialogue, sonic branding).
•	Provide both quantitative measures (e.g., “music present for 25s out of 30s; average tempo 110 BPM”) and qualitative descriptors (e.g., “uplifting orchestral score, warm female voiceover, playful comic sound effects”).
•	Include confidence scores (0–100) for each classification.
•	Capture any additional audio cues not explicitly listed if they appear relevant to mood, recall, or brand identity.
"""

CATEGORY_7_PROMPT = """Context for the analysis:
At its core, advertising is about communicating a message that persuades viewers — either to buy, to change perception, or to build brand trust. The clarity, framing, and type of message directly affect campaign outcomes such as brand recall, brand preference, and sales activation. For example, a clear USP (unique selling proposition) can drive rational persuasion, while emotional appeals may build long-term affinity.
The purpose of this analysis is to identify the advert’s core message(s), the techniques used to persuade, and how clearly and effectively these are delivered.

Detailed Instructions for Analysis
1. Key Message Type
•	Identify the primary communication goal of the advert:
o	Brand value or positioning (e.g., “We care about sustainability”).
o	Product benefit (e.g., “Our phone has the best camera”).
o	Price/offer/promotion (e.g., “50% off this week only”).
o	Sponsorship/association (e.g., “Proud sponsor of football”).
o	Corporate/social message (e.g., CSR, charity, public service).
2. Claim Type
•	Classify the type of persuasion:
o	Rational/informative (facts, technical features, demonstrations).
o	Emotional/associative (happiness, love, pride, humour).
o	Lifestyle aspirational (depicting an ideal life associated with product).
o	Social proof (testimonials, peer approval, popularity cues).
o	Authority/expert endorsement (doctors, certifications, celebrities as trusted voices).
3. USP (Unique Selling Proposition)
•	Identify whether a clear differentiator is communicated. Examples:
o	Price (affordability, discounts).
o	Performance (speed, power, quality).
o	Convenience (easy to use, available anywhere).
o	Innovation (new, first-of-its-kind).
o	Sustainability/health (eco-friendly, organic, safe).
•	Report how explicitly or implicitly this USP is communicated.
4. Offer Presence
•	Detect if an offer, deal, or incentive is present. Examples:
o	Discounts (“50% off”).
o	Limited-time deals.
o	Competitions/free trials.
o	Loyalty or subscription offers.
•	Report timing of offer mention (early/mid/end-frame).
5. Tagline / Slogan Use
•	Detect whether a tagline or slogan is present.
•	Report whether it is:
o	Brand tagline (used consistently across campaigns).
o	Campaign-specific line (unique to this execution).
•	Capture exact wording and when it appears.
6. Call-to-Action (CTA)
•	Identify presence of an explicit or implicit CTA. Examples:
o	Website/app download.
o	Store visit.
o	Subscription/sign-up.
o	“Learn more” or “Buy now”.
o	QR codes or on-screen instructions.
•	Report placement (verbal, text, end-frame visual).
•	Assess clarity (strong, moderate, weak, absent).
7. Framing Style
•	Assess whether the message is framed as:
o	Gain-framed (“You will benefit”).
o	Loss-framed (“Don’t miss out”).
o	Aspirational (“Join the elite”).
o	Fear appeal (“Without this, you risk losing security”).
8. Message Clarity & Simplicity
•	Evaluate whether the ad’s main message is:
o	Clear and simple (audience can recall instantly).
o	Moderately clear (requires attention to grasp).
o	Confusing/unclear (difficult to understand).
•	Report if multiple competing messages are present, potentially diluting clarity.

Suggested Approaches
•	Use speech-to-text transcription to extract all spoken lines.
•	Analyse on-screen text and supers for explicit messaging.
•	Apply semantic analysis to identify rational vs. emotional language.
•	Cross-reference timing of brand mentions, offers, and CTAs with narrative flow.

Output Requirements
Return results in structured JSON with keys for each sub-area (message type, claim type, USP, offers, tagline, CTA, framing, clarity).
Provide both quantitative data (e.g., “CTA appears once, at 25s”) and qualitative descriptors (e.g., “The ad uses humour but ultimately promotes a rational USP around durability”).
Include confidence scores (0–100) for each classification.
Capture any additional persuasive techniques not explicitly listed if they appear relevant (e.g., repetition, rhetorical questions, contrast).
"""

CATEGORY_8_PROMPT = """Context for the analysis:
Adverts rarely exist in a vacuum — they often borrow meaning from cultural references, seasonal events, industry conventions, or social contexts. These contextual cues help ads feel relevant and timely, but can also shape how viewers interpret them. For example, a Christmas advert may be judged differently to a summer holiday campaign, and a tech ad may lean on familiar “category tropes” like futuristic visuals or minimalist design.
The purpose of this analysis is to identify all contextual signals and category conventions used in the advert, so that we can later test whether they influence effectiveness outcomes (e.g., sales spikes during seasonal ads, brand lift from cultural relevance, etc.).

Detailed Instructions for Analysis
1. Industry Category Identification
•	Classify the advert into an industry category, e.g.:
o	FMCG (food, drink, household goods).
o	Retail (supermarkets, clothing, e-commerce).
o	Automotive (cars, motorbikes).
o	Technology (electronics, telecoms, software).
o	Finance/Insurance (banks, credit, insurance).
o	Travel & Leisure (holidays, airlines, hotels).
o	Healthcare/Pharma.
o	Charity/NGO/Public Service.
•	Report which category cues support this classification (e.g., cars driving = automotive, kitchen setting with cooking = FMCG).
2. Category Tropes & Conventions
•	Identify common tropes or visual language associated with the category, e.g.:
o	Automotive = sleek driving shots, winding roads, close-ups of car design.
o	Food & drink = slow-motion pouring, family meals, taste expressions.
o	Tech = glowing screens, futuristic minimalism, fast-paced edits.
o	Finance = authority figures, reassurance, families, safety imagery.
•	Report whether the advert conforms to category conventions or deviates (unique execution).
3. Seasonal & Temporal Cues
•	Detect if the ad references or aligns with a season, holiday, or event:
o	Christmas, Easter, Halloween, Valentine’s, summer, back-to-school.
o	Sports tournaments (World Cup, Olympics, Wimbledon).
o	National holidays (Thanksgiving, Independence Day, Bonfire Night).
•	Report how these cues are conveyed (visual symbols, language, music, colour schemes).
4. Cultural References
•	Identify use of popular culture or national identity cues, e.g.:
o	Celebrities, memes, TV/film references, well-known songs.
o	National landmarks, flags, accents, regional dialects.
o	Social rituals (pubs, barbecues, tea drinking, family dinners).
•	Report whether references are local/national (UK-specific) or global (universally recognisable).
5. Environmental & Social Themes
•	Detect if the advert references sustainability, eco-friendliness, climate change, recycling, health, or social causes.
•	Report how prominently these themes are presented (main message vs. background cue).
6. Occasion & Life-Stage Cues
•	Identify if the ad connects to life stages or personal occasions: weddings, birthdays, new jobs, graduations, parenting milestones.
•	Report whether these occasions are central to the ad’s story or supportive context.

Suggested Approaches
•	Use object detection and scene classification to detect seasonal props (Christmas trees, beach, BBQs).
•	Apply speech-to-text + keyword extraction to detect seasonal/cultural references in dialogue.
•	Use logo/text overlays to identify sponsorship of events (e.g., “Official Partner of Euro 2024”).
•	Apply pattern recognition for detecting category tropes.

Output Requirements
•	Return results in structured JSON with keys for each sub-area (category, tropes, seasonal, cultural, environmental, occasion).
•	Provide both quantitative data (e.g., “2 explicit Christmas symbols: tree at 5s, Santa figure at 18s”) and qualitative descriptors (e.g., “The ad heavily leans on automotive tropes, with winding road shots and close-ups of headlights”).
•	Include confidence scores (0–100) for each classification.
•	Capture any additional contextual or category signals not explicitly listed if they are relevant to audience interpretation or effectiveness.
"""

CATEGORY_9_PROMPT = """Context for the analysis:
Beyond creative and narrative choices, adverts can be studied at a technical level to reveal patterns that affect attention, comprehension, and memory encoding. Features such as object density, logo prominence, visual clutter, or editing techniques can shape whether the ad feels simple and clear or busy and overwhelming. Likewise, transcription of spoken words and frequency of brand mentions help measure message clarity and reinforcement.
The purpose of this analysis is to extract deep technical metadata about the advert, combining computer vision, audio transcription, and advanced video analysis to quantify its structure and complexity.

Detailed Instructions for Analysis
1. Object Detection & Density
•	Use computer vision to detect all objects, animals, and people shown in each frame.
•	Report:
o	Frequency of object categories (cars, pets, food, household items, technology, logos, landmarks, etc.).
o	Average object density per frame (number of distinct objects visible at once).
•	Assess whether visuals are minimalist (few objects, clear focus) or cluttered (many competing objects).
2. Logo & Brand Mark Detection
•	Detect logos or brand marks across the ad.
•	Report:
o	Frequency of logo appearances.
o	Average screen coverage (% of frame).
o	Placement (centre, corner, integrated into objects, background).
•	Report whether logos are visually dominant or subtle/incidental.
3. Facial Expression Analysis
•	Detect human faces and classify emotional expressions: smiling, laughing, crying, neutral, angry, surprised, sad.
•	Report proportion of ad time where positive vs. negative facial expressions dominate.
•	Report whether emotional expressions align with product/brand presence (e.g., smiling when holding product).
4. Speech-to-Text Transcript
•	Provide a full transcript of all spoken dialogue and voiceover.
•	Mark timestamps for each spoken line.
•	Report frequency of brand mentions, product mentions, and key benefit words (e.g., “fast,” “safe,” “new,” “eco”).
5. Keyword & Semantic Analysis
•	Extract keywords and phrases used in dialogue and on-screen text.
•	Report frequency of:
o	Brand name mentions.
o	Product-related terms.
o	Benefit or claim words.
•	Classify semantic tone of language: rational, emotional, humorous, serious, authoritative.
6. Complexity & Cognitive Load
•	Develop an ad complexity score based on:
o	Number of objects per frame.
o	Speed of cuts and transitions.
o	Amount of text/supers per scene.
•	Classify as low, medium, or high complexity.
•	Report if visual/audio density might make ad harder to process.
7. Screen Layout & Visual Composition
•	Analyse whether focus is centralised (main subject clearly framed) or decentralised/cluttered.
•	Report use of symmetry, split screens, overlays, picture-in-picture, AR/CGI effects.
•	Assess whether composition supports clarity or distraction.
8. Editing & Technical Effects
•	Report editing techniques: jump cuts, fast montages, overlays, transitions, slow motion, CGI, filters.
•	Identify any technical gimmicks (e.g., augmented reality overlays, QR code interactions, animation hybrids).

Suggested Approaches
•	Use YOLO/Mask R-CNN object detection for objects and logos.
•	Apply face & emotion recognition models for character analysis.
•	Use ASR (automatic speech recognition) for accurate transcript generation.
•	Apply text analytics for keyword extraction and sentiment classification.
•	Compute visual entropy (variation in pixel intensity) as a proxy for visual complexity.

Output Requirements
•	Return results in structured JSON with keys for each sub-area (objects, logos, expressions, transcript, keywords, complexity, layout, editing).
•	Provide both quantitative data (e.g., “average of 8 objects per frame, 12 logo appearances, brand mentioned 4 times”) and qualitative descriptors (e.g., “visuals are cluttered with overlapping text and objects, creating high cognitive load”).
•	Include confidence scores (0–100) for each detection/classification.
•	Capture any additional technical or advanced features not explicitly listed if they appear relevant to audience attention, clarity, or brand recall.
"""

CATEGORY_10_PROMPT = """Context for the analysis:
Every advert is created with a strategic purpose. Some are designed to build long-term brand equity (brand-building), others to generate an immediate response (activation), while some attempt to combine both (hybrids). Understanding the likely purpose of the advert allows us to interpret its creative choices in context and link them to expected campaign outcomes. For example, brand-building ads often rely on emotional storytelling with little or no call-to-action, while activation ads tend to be shorter, information-heavy, and CTA-driven.
The goal of this analysis is to infer the primary purpose of the advert by examining its messaging, structure, tone, and calls-to-action.

Detailed Instructions for Analysis
1. Strategic Orientation
Classify the advert into one of three categories:
•	Brand-Building Ad (Awareness / Equity Focus)
o	Emotional storytelling or cinematic style.
o	Broad audience appeal, mass reach.
o	Focus on brand associations, values, or heritage.
o	Little or no immediate call-to-action.
•	Activation Ad (Performance / Sales Focus)
o	Rational, product- or price-driven messaging.
o	Explicit offers, urgency, or direct CTAs.
o	Often shorter formats (e.g., 10–20s tactical spots).
o	Designed for immediate sales or response.
•	Hybrid Ad (Equity + Response)
o	Combines brand-building elements (emotional associations, credibility) with activation elements (explicit CTA, offer).
o	Attempts to deliver both long-term brand growth and short-term conversion.
o	Report classification with reasoning, noting evidence in visuals, script, and structure.

2. Target Outcome
Identify the most likely audience outcome being pursued:
•	Awareness (introducing brand/product to broad audience).
•	Consideration (persuading audience to think about brand/product in their decision set).
•	Conversion (direct purchase, sign-up, download, trial).
•	Loyalty/Retention (reminding or rewarding existing customers).
•	Advocacy/Participation (encouraging sharing, cultural conversation, referrals, or community involvement).

3. Role of Call-to-Action (CTA)
•	Absent: Ad relies on leaving an impression only.
•	Implicit: Suggestive nudges (e.g., “Discover more,” “It’s time to change”).
•	Explicit: Direct prompts (e.g., “Buy now,” “Download today,” “Visit our store”).
•	Mixed: Brand story supported by clear action request.
Report whether the CTA is verbal, visual (on-screen text), audio (jingle, catchphrase), or a combination.


4. Messaging Emphasis
Identify the balance of emphasis across these dimensions:
•	Emotional associations: joy, love, pride, humour, trust, nostalgia.
•	Functional/rational benefits: price, features, performance, speed, quality.
•	Corporate values: sustainability, inclusivity, heritage, social responsibility.
•	Social/cultural participation: sponsorships, seasonal or national events, community messages.
Report which emphasis is primary and which are secondary.

5. Breadth vs Precision of Targeting
•	Broad Reach: Mass audience messaging (e.g., “everyone welcome,” household penetration).
•	Targeted Segment: Messaging crafted for a defined group (e.g., young parents, students, gamers, professionals).
•	One-to-One Persuasion: Highly specific targeting, usually tied to product demonstrations or offers.
Report with justification (e.g., “The advert features multiple family settings, indicating a broad household audience focus”).

6. Temporal Orientation
•	Long-term: Designed for brand equity, emotional connection, sustained recall.
•	Short-term: Designed to trigger immediate action, sales uplift, or event-driven response.
•	Balanced/Hybrid: Contains elements of both.

Suggested Approaches
•	Analyse speech-to-text transcript for rational vs emotional language.
•	Detect presence and strength of CTAs and offers (visual and verbal).
•	Compare narrative style (storytelling vs direct product messaging).
•	Assess tone and mood to infer equity vs activation orientation.

Output Requirements
•	Return results in structured JSON with keys for:
o	Strategic orientation (brand-building / activation / hybrid).
o	Target outcome (awareness, consideration, conversion, loyalty, advocacy).
o	CTA presence and type (absent, implicit, explicit, mixed).
o	Messaging emphasis (emotional, functional, corporate, social).
o	Breadth of targeting (broad, segmented, one-to-one).
o	Temporal orientation (long-term, short-term, balanced).
•	Provide both categorical classifications (labels) and qualitative explanation (short narrative justification).
•	Include confidence scores (0–100) for each classification.
•	Capture any additional cues not explicitly listed if they shed light on the advert’s likely purpose.

"""

CATEGORY_11_PROMPT = """Context for the analysis:
Every advert is ultimately designed to serve an advertiser’s business objective. While some ads build broad awareness, many are crafted to drive a specific action such as booking a test drive, requesting an insurance quote, downloading an app, starting a subscription, making a donation, or signing up for a trial.
A Video Scanning AI cannot read the client brief directly, but it can infer the likely advertiser objective by analysing calls-to-action, offers, product/service demonstrations, end-frames, and contextual cues within the advert.
The purpose of this analysis is to classify the advert’s most probable objective(s), based on observable features in the video and audio.

Detailed Instructions for Analysis
1. Call-to-Action Content & Strength
•	Detect explicit CTAs such as:
o	“Book a test drive,” “Request your quote,” “Start your free trial,” “Donate now,” “Subscribe today.”
•	Detect implicit CTAs such as:
o	“Discover more,” “Find out how,” “It’s time to change.”
•	Report whether CTAs are delivered:
o	Verbally (spoken by character/voiceover).
o	Visually (on-screen text, supers, QR code, website URL, app store badges).
o	Audibly branded (jingle, catchphrase).
•	Assess CTA strength: weak, moderate, strong.

2. Offer Type & Incentive
•	Detect presence of incentives, e.g.:
o	Free trial → subscription acquisition.
o	Discount / cashback → immediate sales activation.
o	Competition → engagement or CRM data capture.
o	Loyalty reward → customer retention.
•	Report whether offer is time-limited, exclusive, or recurring.

3. Product/Service Demonstration Style
•	Identify whether the advert includes a step-by-step demonstration (e.g., how to use an app, how easy sign-up is).
•	Report whether demonstration implies:
o	Lead generation (e.g., test drive booking, quote request).
o	Conversion (direct purchase or download).
o	Education (explaining process or benefits, e.g., how insurance coverage works).

4. End-Frame & On-Screen Supers
•	Detect URLs, QR codes, phone numbers, hashtags, app store badges.
•	Report whether end-frame explicitly communicates the objective (e.g., “Donate now at xyz.com”).
•	Assess whether end-frame is brand-first (equity-building) or action-first (transactional).
5. Contextual Category Cues
Some categories have typical advertiser objectives:
•	Automotive → book test drives, showroom visits, brochure downloads.
•	Insurance/Finance → request a quote, apply for credit/loans, compare policies.
•	Retail → drive footfall, highlight seasonal promotions, increase basket size.
•	Streaming/Tech → app downloads, subscriptions, free trials.
•	Charity/NGO → donations, volunteering, petition sign-ups.
•	Healthcare/Pharma → awareness/education, consultations, prescription uptake.
Report which objectives are most consistent with the detected category cues.

6. Engagement & Participation Goals
•	Detect if the advert encourages social media interaction or community participation:
o	Hashtags, “Join the conversation,” “Share your story.”
o	Sponsorship/event tie-ins (“Official sponsor of Wimbledon”).
•	Report whether engagement appears to be the primary or secondary objective.

7. Linguistic Cues in Dialogue & Text
•	Analyse spoken and on-screen language for imperatives (“Sign up,” “Donate,” “Book,” “Download”).
•	Flag if language is more relational (“Join us,” “Be part of our family”) → softer equity/community goals.

Suggested Approaches
•	Apply speech-to-text transcription to capture all dialogue and voiceover.
•	Use OCR to extract all on-screen text and supers.
•	Apply CTA keyword dictionary (book, sign up, donate, download, subscribe, request, register, quote, buy, order).
•	Cross-check industry category classification (from Bucket 8) to refine objective inference.

Output Requirements
•	Return results in structured JSON with keys for each sub-area (CTA, offers, demo, end-frame, category cues, engagement, language).
•	Provide both categorical classification (e.g., “Primary objective: Generate test drive sign-ups”) and narrative explanation (“Ad contains explicit CTA ‘Book your test drive today’, supported by website URL and showroom scenes”).
•	Include confidence scores (0–100) for each inferred objective.
•	If multiple objectives appear present (e.g., brand-building + immediate action), report them as primary vs secondary objectives.
•	Capture any additional cues not explicitly listed if they indicate advertiser intent.

"""
