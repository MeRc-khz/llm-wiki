---
source_url: https://www.youtube.com/watch?v=lDf_y-YPELo
ingested: 2026-08-04
sha256: 6fe3f59fd3edb3782e75f7c840661526f92f00ba02323f81a584009dbea5d62b
media_type: video
duration: "00:36:26"
source_title: "From Words to Worlds: Integrating MCP into the Unreal Editor | Unreal Fest Chicago 2026"
---

[00:00:01] All right. Hello everyone, and welcome
[00:00:05] to From Words to Worlds. We really
[00:00:07] appreciate you being here today. I'm
[00:00:09] Nathan.
[00:00:10] >> I'm Jess.
[00:00:11] >> And I'm Quentin.
[00:00:12] >> And today we're going to talk to you
[00:00:14] about the work that our teams did to
[00:00:17] enable an MCP server in the Unreal
[00:00:20] Engine. And hopefully all of you are
[00:00:23] here because, you know, we announced
[00:00:24] yesterday that we've launched official
[00:00:26] MCP support in Unreal with the 5.8
[00:00:29] release. It's open, it's free, and we're
[00:00:32] not releasing not just a server, but
[00:00:34] support out of the box for two dozen
[00:00:37] different engine and editor systems.
[00:00:40] It's something just shy of a thousand
[00:00:42] different APIs that are all ready to go.
[00:00:45] And like we showed in the state of
[00:00:46] Unreal, you can do a lot with those tool
[00:00:49] sets out of the box, things like
[00:00:51] materials, blueprints, PCG, the works.
[00:00:55] And our goal today is going to be to dig
[00:00:57] down, go under the hood, talk about what
[00:01:00] we did to enable that, and then how you
[00:01:01] can extend the MCP for your own games
[00:01:04] and experiences.
[00:01:06] So, before I do that though, I want to
[00:01:07] talk a bit about the philosophy that we
[00:01:09] have and we've tried to embody in
[00:01:11] building this technology, which is what
[00:01:13] we want out of an LLM is that we believe
[00:01:16] it should be an assistant and not a
[00:01:18] magic bullet. This isn't just a
[00:01:20] statement of principle, it's a statement
[00:01:21] of like what we believe the technology
[00:01:23] is good at today.
[00:01:25] And so, in order to make sure that we
[00:01:26] were following this vision, we had three
[00:01:28] principles that we thought about a lot
[00:01:30] during development. And the first was
[00:01:32] that we wanted to make sure that we were
[00:01:33] working with LLMs in a way that was
[00:01:35] directable, where the AI or the model is
[00:01:38] there to amplify your creative intent,
[00:01:41] not to replace it.
[00:01:43] The second principle is that everything
[00:01:45] should be editable. That AI, the LLM, it
[00:01:48] shouldn't get special access, special
[00:01:50] permissions, special formats. That
[00:01:53] everything that an LLM does should be
[00:01:55] inspectable by you while it's doing it.
[00:01:57] And the results of that work should be
[00:02:00] indistinguishable from anything any
[00:02:02] human did with the asset. So that when
[00:02:03] the model is done, you can edit it,
[00:02:06] change it, review it, etc.
[00:02:08] And then finally, we want to make sure
[00:02:10] that we weren't building like a closed
[00:02:12] system or a black box. Unreal has always
[00:02:14] been a tool that you can take and
[00:02:16] customize and extend. And we want to
[00:02:18] make sure that our MCP and LLM work
[00:02:20] embodied that. And there was a very,
[00:02:22] very clear path for customization by all
[00:02:25] of you.
[00:02:26] And then finally, we wanted to do all of
[00:02:28] this not in the context of like a cheap
[00:02:30] demo or a toy example, but a scenario
[00:02:33] that would be really challenging for a
[00:02:35] large language model, something like
[00:02:37] world building. And uh to tell you more
[00:02:39] about that, I'll welcome JS.
[00:02:42] >> Thank you.
[00:02:43] >> [applause]
[00:02:47] >> Thank you, Nita. So, I'd say roughly
[00:02:49] about a year ago, we wanted to explore
[00:02:51] uh
[00:02:52] world building
[00:02:54] would benefit from LLM's reasoning.
[00:02:56] And while staying true to our vision,
[00:02:59] I wanted to handle something really
[00:03:01] complex like building a city
[00:03:02] procedurally.
[00:03:05] But we had a core challenge to deal
[00:03:06] with, spatial operations.
[00:03:09] As you may know, LLM's typically
[00:03:11] struggle with those.
[00:03:12] They're really, really good with words,
[00:03:14] but they're not naturally built for
[00:03:16] treating environment creation or
[00:03:18] low-level spatial operations.
[00:03:20] So, how do we go from the text on the
[00:03:22] left to the city on the right?
[00:03:25] We felt like we had a solution, or at
[00:03:27] least a part of it.
[00:03:29] Unreal Engine excels at this, especially
[00:03:31] with its built-in procedural content
[00:03:33] generation framework, or PCG.
[00:03:36] So, the idea became really, really
[00:03:38] simple. We have a great tool for a
[00:03:40] spatial world building, Unreal,
[00:03:42] and a powerful new tool for reasoning
[00:03:45] and automation, the LLM's.
[00:03:47] What if they became friends?
[00:03:50] To achieve this, we combined key
[00:03:52] elements together. First, tool sets,
[00:03:55] followed by primitives, examples, and
[00:03:57] skills, or in short, documentation.
[00:04:00] Let's dig into each of those to better
[00:04:02] understand the foundation of our
[00:04:04] approach.
[00:04:06] You could think of an LLM as a brain in
[00:04:09] a jar. So, the first prerequisite for
[00:04:12] any of this to work is to give the LLM
[00:04:15] the ability to interact with Unreal.
[00:04:17] And it happens to be that tool sets do
[00:04:19] exactly that. They are APIs for LLMs.
[00:04:23] In our case, we use and combine
[00:04:24] multiple.
[00:04:26] But the most important one for this
[00:04:27] particular challenge is the PCG tool set
[00:04:31] and its set of dedicated functions.
[00:04:34] Mainly, everything to do with creating,
[00:04:37] editing,
[00:04:38] reading, and executing graphs.
[00:04:41] Nitin will cover
[00:04:43] later in this talk how you two can
[00:04:44] extend the collection of tool sets that
[00:04:47] we provide.
[00:04:48] Now that the LLM is able to interact
[00:04:50] with Unreal, we need to give it the best
[00:04:52] context possible for it to succeed.
[00:04:56] It started with providing its
[00:04:58] vocabulary, which we call PCG
[00:05:00] primitives.
[00:05:01] It allows the LLM to build environments
[00:05:04] faster and more reliably without having
[00:05:06] to reason about every single step.
[00:05:09] PCG can be seen as a chain of functions
[00:05:11] to build worlds, but unlike Python,
[00:05:14] which LLMs are way more familiar with,
[00:05:18] PCG is much less represented in their
[00:05:20] training data.
[00:05:22] So, they mainly rely on the
[00:05:23] documentation and what they can
[00:05:25] extrapolate from it,
[00:05:26] which is
[00:05:27] not good.
[00:05:30] So, we went on and created a library of
[00:05:32] over 80 plug-and-play primitive spatial
[00:05:35] operations. It's a mini framework using
[00:05:38] PCG subgraphs on top of all the native
[00:05:40] operations available.
[00:05:42] Simply put, they're streamline bite-size
[00:05:45] functions that the LLMs can string
[00:05:47] together as words to build environment
[00:05:50] scenario.
[00:05:51] And as you can see in this video, these
[00:05:53] functions are being added to the graph
[00:05:56] by asking it to create shapes, compose
[00:05:58] them, applying transforms, or simply
[00:06:02] sampling, filtering, and spawning.
[00:06:04] These subgraphs are fully parameterized
[00:06:07] and documented. They don't need LLMs to
[00:06:09] work at all. But, on the other hand,
[00:06:12] LLMs are much more capable with them.
[00:06:15] Keep those in mind cuz everything we'll
[00:06:17] show next is using these small
[00:06:19] operations combined together.
[00:06:24] Our next step was to build a lot of
[00:06:26] examples. These are complete PCG graph
[00:06:29] built out of the primitives, ranging
[00:06:31] from use case agnostic basics to
[00:06:34] concrete environments of different
[00:06:35] types. If the primitive functions were
[00:06:38] its vocabulary, then the example would
[00:06:41] be the sample
[00:06:43] sentences, paragraphs,
[00:06:45] chapters, and sometimes even entire
[00:06:47] books, as you can see here.
[00:06:49] The LLM can consult them at any point in
[00:06:51] time to build something similar or
[00:06:54] reproduce it. But, it can also learn
[00:06:56] from
[00:06:57] useful patterns that it can apply in
[00:06:59] different situations.
[00:07:01] Since this is all data-driven, you can
[00:07:04] extend the system quite easily by
[00:07:07] providing project-specific primitives
[00:07:08] and examples. But, you can also use the
[00:07:11] LLM to build them if you want, which we
[00:07:13] actually did once we had the everything
[00:07:16] set up.
[00:07:18] The final essential component is skills.
[00:07:21] They contain the information that the
[00:07:23] LLM needs but doesn't have to succeed at
[00:07:25] a given task. But, they also help
[00:07:27] generalizing beyond the examples. To
[00:07:30] stick with the language metaphor, skills
[00:07:32] are the principles of good storytelling.
[00:07:35] And these guidelines These guidelines
[00:07:37] extend way beyond the PCG framework.
[00:07:40] We can create and combine skills for
[00:07:42] anything in the engine including actor
[00:07:45] and asset manipulation, materials,
[00:07:46] lighting,
[00:07:48] Niagara, name it.
[00:07:52] With these four key elements, tool sets,
[00:07:54] primitives, examples, and skills, we're
[00:07:56] now ready to do world building, and
[00:07:58] that's what we're going to showcase.
[00:08:01] Let's look at a small-scale example
[00:08:03] first as a illustrative for illustrative
[00:08:07] purpose.
[00:08:10] On the left here, we have Unreal Engine,
[00:08:12] and on the right is a terminal.
[00:08:14] The key prompts are summarized on the
[00:08:15] lower left corner.
[00:08:17] In this single session, we load the
[00:08:19] required tool sets and skills,
[00:08:21] then define the context. We want to
[00:08:23] furnish this small apartment living
[00:08:24] room.
[00:08:26] The next step
[00:08:28] is to provide a description, such as its
[00:08:30] dimension and whereabouts in the level.
[00:08:33] Then, we want to place props.
[00:08:35] First, a sofa with a rug, then a round
[00:08:38] coffee table, which are all retrieved by
[00:08:41] the LM using semantic search.
[00:08:43] We keep adding more and more to the
[00:08:45] scene and adjusting as we go.
[00:08:47] At any point in time, you can add an
[00:08:50] asset manually to the level and refer to
[00:08:52] it in your session context.
[00:08:55] Spatial relationships are important even
[00:08:58] in such a small space.
[00:09:00] Now, you'll have to expect to adjust
[00:09:02] things because it will definitely fail,
[00:09:05] especially with pivots, overlaps, and
[00:09:07] orientations. A standardized library
[00:09:10] with good information and instructions
[00:09:11] about transforms for your project will
[00:09:14] go a very long way.
[00:09:16] Once we have our basic layout, we can
[00:09:18] start using prompts that have a much
[00:09:20] larger impact.
[00:09:21] We use it here to give a story to the
[00:09:23] scene or try a complete rearrangement.
[00:09:26] At this scale, the gain is obviously not
[00:09:29] in the individual asset placement, but
[00:09:31] in those broader, more impactful changes
[00:09:33] for faster iteration.
[00:09:35] So now, let's move to city scale, where
[00:09:37] things truly starts to shine, Quantum.
[00:09:47] So,
[00:09:49] from the very beginning, we wanted to
[00:09:50] challenge the new PCG system plus the
[00:09:53] LLM reasoning we've connected to it
[00:09:56] with something ambitious and larger,
[00:10:00] something like an entire city.
[00:10:02] And if you remember, we had made a city
[00:10:04] in the last for The Matrix Awakens.
[00:10:07] And this city was a really hard one. It
[00:10:10] was a very complex system
[00:10:12] and was generated outside of Unreal and
[00:10:15] overall was fairly rigid to set up and
[00:10:19] to interact with.
[00:10:21] And we figured that using this would be
[00:10:23] a perfect playground for the PCG
[00:10:25] primitive plus the example workflow that
[00:10:28] we've established.
[00:10:30] Now, what we are going to show is how we
[00:10:33] managed to create this entire procedural
[00:10:35] generation of the city sample through
[00:10:37] PCG and prompting.
[00:10:41] This is its procedural story. Prompt by
[00:10:44] prompt and through manual interaction in
[00:10:46] the viewport, we reshape the city
[00:10:47] layout.
[00:10:49] Starting with splines that define the
[00:10:50] city boundaries, the main roads that
[00:10:52] create districts, lots, roads, and
[00:10:55] buildings through a chain of complex
[00:10:57] relationship and operation.
[00:11:00] And as you can see in the lower right on
[00:11:02] the PCG graph,
[00:11:03] the primitive we talked about earlier
[00:11:05] becomes the spatial vocabularies who
[00:11:07] which the LLM do the city building
[00:11:09] process. It will write brick by brick
[00:11:12] the logic of how we build the city.
[00:11:15] >> [snorts]
[00:11:16] >> We are establishing the rules like the
[00:11:18] highway supersedes building footprints
[00:11:20] or the terrain heals conforms to the
[00:11:23] road and highways.
[00:11:24] Which building style should be used on
[00:11:27] for this or that category of districts?
[00:11:31] And as the same applies to the forest
[00:11:33] that will build itself around the the
[00:11:36] city with its own PCG graph.
[00:11:39] A little later, we
[00:11:41] ask to sparse
[00:11:43] to scatter sparsely building districts
[00:11:46] to make the city skyline. And finally,
[00:11:50] the city rulebook
[00:11:52] is written.
[00:11:53] And the result is a fully parametric
[00:11:55] city
[00:11:56] entirely generated with PCG
[00:11:59] and prompts in Unreal Engine.
[00:12:01] This didn't take weeks like it used to.
[00:12:04] It took a day.
[00:12:05] This is not a black box. This is real
[00:12:08] data that you can open, inspect, edit,
[00:12:12] extend, and that could be shipped in a
[00:12:13] game today.
[00:12:15] Built from a complex and
[00:12:17] network of interdependent PCG graph,
[00:12:20] every part of the city can be adjusted,
[00:12:22] regenerated procedurally in a few
[00:12:24] minutes.
[00:12:25] You can ask to swap an entire district
[00:12:27] to be a park, reserve block to be a
[00:12:29] parking. The LLM understands how the
[00:12:31] graph are organized
[00:12:33] and what needs to be updated.
[00:12:37] And looking a bit closer, we can
[00:12:38] demonstrate the procedural procedural
[00:12:40] nature of the system. Here, you can see
[00:12:42] the
[00:12:44] buildings rebuilding around the highway.
[00:12:46] Or you can ask for a specific building
[00:12:48] to be pro more prominent in the scene,
[00:12:50] and the LLM will scan through the city
[00:12:53] and assess what this means.
[00:12:55] While the system makes the
[00:12:58] building still editable, it's not the
[00:12:59] locked-in actor.
[00:13:05] And this work for an
[00:13:07] for an entire team.
[00:13:09] Here, another artist,
[00:13:11] Jess,
[00:13:12] recreated Central Park in a separate
[00:13:14] session, and we dropped it directly in
[00:13:16] the in the city. And because it's
[00:13:18] procedural, you can see that it rebuilds
[00:13:19] itself around it. And one convenient
[00:13:22] feature of using the LLM is that
[00:13:25] we can refer to
[00:13:27] real-world data. So, for this park, we
[00:13:29] simply ask for the actual size and
[00:13:31] layout of Central Park
[00:13:32] and how to reproduce its key feature at
[00:13:35] the correct scale.
[00:13:39] And
[00:13:40] so as we progressed, we realized that we
[00:13:42] we don't always need to create PCG graph
[00:13:44] for small operation, and we came up with
[00:13:46] what we called instance. It's a
[00:13:48] fire-and-forget function call.
[00:13:51] It's executing a pre-made PCG graph
[00:13:53] without leaving a trace in the level.
[00:13:55] And that means that we can benefit from
[00:13:57] the entire framework without forcing the
[00:13:59] user into a graph.
[00:14:02] Again, this is all data-driven. You can
[00:14:04] extend those as you want.
[00:14:07] And all the the example you see in the
[00:14:09] video are currently using the PCG
[00:14:11] primitives.
[00:14:13] So, we create a spline
[00:14:15] using selected actors. In between that
[00:14:17] spline, we scatter assets.
[00:14:20] We shuffle everything. Then after a few
[00:14:22] manual operation, we can
[00:14:24] save everything as an assembly and spawn
[00:14:27] it back in the level as an optimized
[00:14:28] actor. And keep in mind that this is not
[00:14:31] using any PCG graph that will stay in
[00:14:33] the level. This is just called on the
[00:14:35] fly.
[00:14:39] So, while the LLM can actually make a
[00:14:41] forest
[00:14:42] with the primitive and the example we've
[00:14:44] provided, we wanted to tackle something
[00:14:46] a bit more complex, which is a biome
[00:14:48] core.
[00:14:49] And for for those who have never heard
[00:14:51] of it, biome core is a powerful PCG
[00:14:54] data-driven biome creation tool. It's
[00:14:56] highly complex and kind of requires
[00:14:59] pretty advanced knowledge.
[00:15:01] And here we created a skill to guide the
[00:15:03] LLM on how to use biome core.
[00:15:06] And so now it's aware of all the data
[00:15:08] structure and how to create it from the
[00:15:09] ground up.
[00:15:11] So, it's a a lot more convenient to use.
[00:15:12] It's can
[00:15:14] it's like prompting to ask for it.
[00:15:17] That's a great example where the LLM the
[00:15:19] LLM can help you use a system that
[00:15:21] already exists
[00:15:23] and that has been proven to work. It's
[00:15:25] valuable approach alongside what we've
[00:15:27] shown before.
[00:15:31] Another great example of a skill use was
[00:15:34] for the lighting.
[00:15:35] When we started to
[00:15:38] experiment with lighting and we asked
[00:15:40] the LLM to adjust the default lighting
[00:15:43] setup, we quickly realized that just
[00:15:45] based on the list of parameters and the
[00:15:48] documentation that it knows about the
[00:15:51] LLM wasn't able to do too much of a good
[00:15:53] job.
[00:15:54] And also something else to think about
[00:15:56] is that it can modify parameters on the
[00:15:58] fly, but it doesn't actually visual
[00:16:00] feedback, so it doesn't know if what he
[00:16:01] has done actually worked.
[00:16:04] So as we iterate in on this, not only we
[00:16:06] provided feedback to what he's doing and
[00:16:09] we try to capture all that feedback into
[00:16:11] a skill,
[00:16:13] but we also gave it the ability to to
[00:16:16] take screenshot and iterate on it.
[00:16:18] So now with the skill, it knows the
[00:16:20] subtle detail of the default lighting
[00:16:22] setup of Unreal, which asset are
[00:16:24] composing it, how they work between
[00:16:26] between each other,
[00:16:27] and we gave it some fundamental lighting
[00:16:29] skills like starting from the ground up
[00:16:32] with the light position and the
[00:16:34] intensity, so he has like the overall
[00:16:36] color and mood, the correlation between
[00:16:38] the direct and field lights or something
[00:16:41] like not overcompensating everything in
[00:16:43] the post process to try to
[00:16:45] desperately achieve look.
[00:16:47] And I think most importantly as I
[00:16:48] mentioned is like now he can take
[00:16:51] screenshots, so he will go on a cycle of
[00:16:54] changing parameters, taking a
[00:16:56] screenshot, evaluate and try to converge
[00:16:59] toward the look.
[00:17:02] And that's what we're going to see here.
[00:17:04] So let's say for example, we ask for a
[00:17:05] purple desk,
[00:17:06] not only will adjust the sun position,
[00:17:08] which is kind of expected, but it will
[00:17:09] modify all the parameters at once and
[00:17:12] make it more compelling. It will touch
[00:17:14] the cloud, the sky tint, the post
[00:17:15] process domain and values everything
[00:17:17] together while taking screenshots.
[00:17:20] Now for the overcast, actually an
[00:17:21] interesting attempt where he actually
[00:17:23] got it wrong. He modified the cloud
[00:17:25] material in the wrong way and then he
[00:17:27] was taking a screenshot and then
[00:17:28] assessing that it was good, but it was
[00:17:29] actually because it was fully blown
[00:17:31] white.
[00:17:32] >> [snorts]
[00:17:32] >> But then, you know, you can chat chat
[00:17:35] your way back to correctness like you
[00:17:36] would do with any chatbot.
[00:17:38] Because at the end it's conversation.
[00:17:41] As I mentioned before like for Central
[00:17:42] Park, you can refer to special to
[00:17:44] real-world place. So it finds the
[00:17:46] information that matches that, kind of
[00:17:48] like color temperature, climate, um
[00:17:52] and coordinates. And because we can
[00:17:55] provide images, now we can also ask it
[00:17:57] to hit a precise visual target and it
[00:18:00] will cycle through the screenshot and
[00:18:01] parameters to try to, you know, converge
[00:18:04] and achieve that look.
[00:18:07] So from all of those experimentation,
[00:18:11] exploration, we we have a few insights
[00:18:13] that we would like to share.
[00:18:15] We are quite happy how PCG
[00:18:18] fit naturally to be the spatial language
[00:18:20] for the LLM and that works out pretty
[00:18:22] well.
[00:18:23] But something that we
[00:18:25] realize is that the take us the
[00:18:27] technical artist is the key and that's
[00:18:30] something that should not be
[00:18:31] underestimated. This takes a lot of time
[00:18:34] and experience
[00:18:35] to use it to its full full potential and
[00:18:38] that's not going to be a one prompt
[00:18:40] that's going to give you a result. You
[00:18:41] need to know what you're doing
[00:18:43] and you need to use it to assist you.
[00:18:47] Looking at what we've done and the
[00:18:49] exploration we've done is a good place
[00:18:50] to start because we've already ironed
[00:18:53] out the initial kinks of the of this
[00:18:56] system.
[00:18:57] You should know that all the primitives
[00:18:59] and example
[00:19:00] can be used with or without the LLM.
[00:19:03] It's not a
[00:19:04] closed system.
[00:19:06] And what the LLM helps you create with
[00:19:09] PCG doesn't have to be used with LLM.
[00:19:13] It will always produce deterministic
[00:19:14] results because this is PCG. And I think
[00:19:17] most importantly,
[00:19:19] you can extend it to your proper use
[00:19:21] cases, and that's exactly what we are
[00:19:23] going to cover next with Nathan. Nathan,
[00:19:26] please show them how it's done.
[00:19:29] >> [applause]
[00:19:33] >> Cool. So, our final section is on how
[00:19:37] you can extend the Unreal MCP in a way
[00:19:40] that's particular for your game or
[00:19:42] experience. Um as a little bit of
[00:19:44] context, right, the big picture is that
[00:19:45] we've talked about the MCP server, which
[00:19:48] is the bridge or the gateway between,
[00:19:50] you know, you and your agent and the
[00:19:52] world of Unreal.
[00:19:54] JS and Quentin, right, just talked about
[00:19:56] many of the things that we've done
[00:19:58] inside the existing engine systems and
[00:20:00] what we've learned along the way. And
[00:20:02] now I'm going to talk about how you can
[00:20:03] take some of these principles and
[00:20:05] technologies and extend them yourself.
[00:20:08] We're going to talk about three types of
[00:20:10] extension, tool sets, skills, and
[00:20:12] examples. And uh we'll start with tool
[00:20:14] sets. So, uh in case you've forgotten 15
[00:20:18] minutes ago,
[00:20:19] tool sets, what are they? Uh they are
[00:20:21] really APIs for LLMs. And why APIs? It's
[00:20:25] really about efficiency. If you want to
[00:20:27] have um an LLM interact with an
[00:20:29] application, doing it programmatically
[00:20:32] is, you know, much more token efficient
[00:20:34] and lower latency than trying to, you
[00:20:35] know, move the mouse and click around.
[00:20:38] And there's just one problem, which is
[00:20:40] that like one of the L's in LLM stands
[00:20:42] for language, and so LLMs and the MCP
[00:20:45] standard speak JSON. Uh but as game
[00:20:48] developers, we work with blueprints,
[00:20:51] C++, Python, um and we don't really want
[00:20:54] to worry about JSON conversion and the
[00:20:56] standards behind it. Um and this is
[00:20:58] particularly important because we're
[00:21:00] going to expose like entire domains,
[00:21:03] right, not just one or two functions,
[00:21:05] but like the PCG tool set you can see
[00:21:06] it's many functions. There are many
[00:21:09] domains in Unreal. So, we're going to
[00:21:10] add a lot of tools. And our team, one of
[00:21:13] our goals was to make it as easy as
[00:21:15] possible to add new domains and add new
[00:21:18] tools without worrying about, you know,
[00:21:20] tons of boilerplate logic.
[00:21:22] So, the way we've tackled that is
[00:21:24] leveraging Unreal's reflection system.
[00:21:26] Unreal, you know, going back a long time
[00:21:28] has had a great reflection system with,
[00:21:30] you know, UStruct and FProperty and all
[00:21:32] of that. And we're going to leverage
[00:21:34] that to automatically create the JSON
[00:21:36] that we need. And for MCP, we actually
[00:21:39] need two flavors of JSON. One is called
[00:21:41] JSON schema, and the other is called
[00:21:43] JSON data. And if you're not familiar
[00:21:45] with this, JSON schema is basically the
[00:21:47] type definition. So, you know, if you
[00:21:50] say, "I have a function, and that
[00:21:51] function has an argument, and that
[00:21:52] argument is an integer." Well, the
[00:21:54] schema is what tells you, you know,
[00:21:56] things like the name and type of that
[00:21:58] argument.
[00:21:59] But then, of course, whenever you invoke
[00:22:01] a function or set a property, you need
[00:22:03] its value, and that's that's JSON data.
[00:22:06] And these two things, you know, go
[00:22:07] together, and you need both of them
[00:22:09] working to have an MCP integration.
[00:22:12] The thing is, like, integer, you know,
[00:22:14] looks pretty simple. But of course, in
[00:22:16] Unreal, you know, we need to think about
[00:22:17] supporting enums, and then there's also
[00:22:20] structs, maybe more than a few structs.
[00:22:23] And ultimately, we have to support like
[00:22:24] all of the things, all the types,
[00:22:26] including, you know, pointer-like types
[00:22:28] like UObject and UClass. And then if
[00:22:31] they can be nested, so you have
[00:22:32] containers of arrays of structs. Yeah,
[00:22:35] it goes on and on. Um, but we've done
[00:22:38] that work for you.
[00:22:39] The 5.8 has very, very robust JSON
[00:22:42] schema and JSON data conversion. So,
[00:22:45] hopefully, this is a detail that you'll
[00:22:46] think about now and never again, maybe.
[00:22:49] I hope.
[00:22:51] So, with that, it makes it really,
[00:22:53] really easy for you to build APIs where
[00:22:56] that conversion is handled
[00:22:57] automatically. And so, in 5.8, if you
[00:23:00] want to make uh a new tool set, it's
[00:23:02] very simple. You just derive from UTool
[00:23:04] Set Definition.
[00:23:06] And then when you want to add tools to
[00:23:08] that, they're just static UFunctions,
[00:23:11] just like anything else you would write
[00:23:12] in Unreal. Same type, same signature,
[00:23:15] same metadata, same tool tips. Um
[00:23:18] excuse [clears throat] me, because of
[00:23:19] that, everything is fully type safe, and
[00:23:22] you don't really need to learn anything
[00:23:23] new. You just write your tools exactly
[00:23:25] the way you would write an API for
[00:23:27] anyone else in your game.
[00:23:29] Uh also, because we're leveraging
[00:23:31] Unreal's reflection, all of this stuff
[00:23:33] works in Python as well. I actually
[00:23:35] started my career as a technical artist.
[00:23:37] Uh I love Python. It's a great language.
[00:23:40] And we wanted to make sure that
[00:23:42] exposing, you know, editor features
[00:23:44] wasn't something that only, you know,
[00:23:45] engine programmers could do, but
[00:23:47] technical artists, technical designers,
[00:23:49] software test engineers could all do
[00:23:51] that um in, you know, C++ or in Python.
[00:23:56] Uh and because of that, basically, your
[00:23:57] signature is the schema, and we can
[00:24:00] automatically take that C++ or that
[00:24:02] Python, we'll create the JSON schema for
[00:24:05] you, handle the JSON data bindings. Uh
[00:24:08] we'll also pick up things like metadata,
[00:24:09] so tool tips become documentation, mins
[00:24:12] and maxes, all of that stuff is
[00:24:14] automatically bundled up for you.
[00:24:16] And so basically, what happens is that
[00:24:18] when the LLM now wants to invoke one of
[00:24:21] your tools, it will send some JSON data
[00:24:24] over the wire and something like, "Oh,
[00:24:25] this is the name of the function I want
[00:24:27] to invoke, and this is the JSON data of
[00:24:29] the arguments into that function."
[00:24:32] We convert that transparently, and then
[00:24:34] we call your function. And to you, it
[00:24:36] just looks like your code ran. Um the
[00:24:38] parameters, you know, uh are called in,
[00:24:40] the UFunction is invoked. And then when
[00:24:43] you're done, you return whatever you
[00:24:45] want, just like you normally would in
[00:24:46] Unreal, and we convert that from the
[00:24:49] Unreal types to JSON data and send that
[00:24:51] back over the wire. Super simple. Uh
[00:24:55] really, really fun to work with.
[00:24:57] There's a couple other things that we've
[00:24:58] considered that are worth thinking
[00:25:00] about. Um very often LLMs, you'll ask it
[00:25:03] to do something and then it invokes a
[00:25:04] long-running operation. And you know,
[00:25:07] ideally you don't want to block the
[00:25:08] editor for seconds, minutes, anything
[00:25:10] like that. You want it to be able to
[00:25:11] happen in the background.
[00:25:13] So, we've actually built the tool set
[00:25:15] internals are all inherently
[00:25:18] asynchronous, but U functions are not,
[00:25:20] right? U functions are just fire and
[00:25:22] forget. So, we've built um a little
[00:25:24] bridge which is a class that's designed
[00:25:27] for returning asynchronous results.
[00:25:29] Um the base class is called uh U tool
[00:25:31] call async result. There's a bunch of
[00:25:34] the sub classes for different types,
[00:25:36] like if you want to return a string
[00:25:37] asynchronously or an image, those are
[00:25:39] all built in. You can extend it with
[00:25:41] your own types, super easy. And then you
[00:25:44] can make your own asynchronous functions
[00:25:46] that kind of do whatever they want, use
[00:25:48] whatever async framework uh is best for
[00:25:50] your game, and then return that uh
[00:25:52] result over the wire through the tool
[00:25:55] call async result.
[00:25:57] So, in doing all of these, you know, a
[00:25:59] couple of dozen tool sets, we've learned
[00:26:01] a few things, sometimes uh painfully,
[00:26:03] and we want to share some high-level
[00:26:05] learnings and best practices with you.
[00:26:07] So, one of the first things when you're
[00:26:09] building a tool set is you want to like
[00:26:11] make the API clean, take the time to
[00:26:13] give functions and arguments, you know,
[00:26:15] good names, write tooltips, think a bit
[00:26:18] about the types, right? You want to
[00:26:20] design your API kind of like you're
[00:26:23] designing it for like a a junior
[00:26:24] programmer, you know, somebody who's
[00:26:26] really smart, but maybe isn't an expert
[00:26:28] in your domain. And so, kind of clarity
[00:26:30] of API design really helps that junior
[00:26:32] programmer, which is roughly what LLMs
[00:26:34] are in this domain today.
[00:26:37] You want your APIs to be complete. And
[00:26:39] so, you want to do a kind of a CRUD type
[00:26:41] approach, where you know, if there's a
[00:26:43] setter, there should be a getter, but
[00:26:45] often there might also need to be a list
[00:26:47] function. Um if you look at a lot of
[00:26:50] cases, we say, "Oh, well, I as a human,
[00:26:51] I know what the properties are, but the
[00:26:53] LLM doesn't." And so, you want, you
[00:26:55] know, not just get property and set
[00:26:57] property, but list properties so that
[00:26:59] the LLM even knows what it could get or
[00:27:01] what it could set.
[00:27:03] Uh composability is really, really
[00:27:04] important. LLMs have a lot of knowledge.
[00:27:07] They're really, really good at kind of
[00:27:09] putting building blocks together. So,
[00:27:11] you want to build your APIs not to be
[00:27:13] kind of like monolithic or on rails, but
[00:27:15] to be modular and flexible so that the
[00:27:17] LLM can say, "Okay, you gave me this
[00:27:19] job. I'll put the APIs together in this
[00:27:21] way. Oh, a different job, different
[00:27:22] APIs." Um and so, using kind of like
[00:27:25] types that are combinable, clear, makes
[00:27:27] for uh composable and usable APIs.
[00:27:31] And finally, you really want to be, in a
[00:27:33] sense, communicative. Um modern LLMs are
[00:27:36] really trained to be good problem
[00:27:38] solvers, but that's predicated on
[00:27:39] feedback. And obviously, your API is
[00:27:42] going to include positive feedback,
[00:27:44] like, "Oh, it succeeded." or "It
[00:27:45] failed." or "Here's the actors that were
[00:27:47] selected." But very often, LLMs will
[00:27:49] make mistakes. They'll invoke tools with
[00:27:52] invalid arguments. A system won't be
[00:27:54] available. And you want to not silently
[00:27:57] fail, but actually return a useful error
[00:28:00] that tells the LLM like what went wrong
[00:28:02] and why and maybe even how it might fix
[00:28:03] itself. And we actually have a standard
[00:28:06] error path in tool sets where in Python
[00:28:08] and in C++, you can return informative
[00:28:11] errors, and they'll automatically get
[00:28:12] sent over. And cuz that way, you don't
[00:28:15] have to say, "Well, let's make sure the
[00:28:16] LLM never makes a mistake." Like, it's
[00:28:18] going to make a mistake, but you can
[00:28:20] make sure that it's able to fix the
[00:28:21] mistakes when they happen.
[00:28:24] So, the second thing we want to talk
[00:28:25] about are skills.
[00:28:27] As James mentioned, skills are really a
[00:28:30] distilled information that the LLM
[00:28:32] needs, but doesn't have. You know, the
[00:28:35] LLM has kind of like a fuzzy
[00:28:36] recollection, right, of all of the text
[00:28:38] on the internet. It's got whatever is in
[00:28:40] the context window. Um but I really
[00:28:42] liked uh Quinton's example of the
[00:28:44] lighting skill. Or like, in Unreal, when
[00:28:46] you're doing lighting, you really want
[00:28:48] to set the sun before the sky, right?
[00:28:52] And that's a kind of important gotcha
[00:28:55] that the LLM may not get right much of
[00:28:58] the time, may not know. That's kind of
[00:28:59] like technical artist knowledge, but
[00:29:01] when you write it down in a skill, it
[00:29:02] allows the LLM to perform that task more
[00:29:05] reliably.
[00:29:06] So, we've added a native kind of skill
[00:29:09] to Unreal. It's this new class called U
[00:29:11] Agent Skill, and it's based on an open
[00:29:13] standard called Agent Skills. If you've
[00:29:16] ever worked with like Claude Code, the
[00:29:19] skill definition is the same one, and
[00:29:22] we've basically just taken the same
[00:29:23] semantics and spirit and tried to make
[00:29:25] it Unreal native.
[00:29:27] So, because this is a new U class,
[00:29:30] making a new skill is just a matter of
[00:29:32] deriving from U Agent Skill. You can do
[00:29:34] that in C++, Python, or in blueprints.
[00:29:38] And the blueprints part is kind of neat
[00:29:40] because you it becomes a U asset. And
[00:29:42] so, if you want to say, like, have a
[00:29:43] skill and check it in and share it with
[00:29:46] other people on your project, you just
[00:29:47] add it to your project like anything
[00:29:49] else and check it in like anything else,
[00:29:50] and now it's shareable.
[00:29:53] One of the other cool things, though, is
[00:29:54] you can see the base of a skill is just
[00:29:56] like a big bucket of text, and that's
[00:29:58] great. But, because we're in the world
[00:30:01] of, you know, U objects, we actually
[00:30:03] allow for programmatic skill text
[00:30:05] construction. So, if you want, there's a
[00:30:08] function that you can override that
[00:30:10] whenever we read the skill text out, we
[00:30:12] invoke the function, and that way you
[00:30:14] can modify, edit, append to your skill,
[00:30:17] basically programmatically getting some
[00:30:19] extra context, you know, out of your
[00:30:20] project before the LLM sees the final
[00:30:23] skill text.
[00:30:26] So, again, best practices, things that
[00:30:27] we've found work best. The first is that
[00:30:29] you really want to focus on skills that
[00:30:31] are novel, that are adding information
[00:30:34] that the LLM can't get anywhere else.
[00:30:36] So, if a tool already returns that info,
[00:30:40] don't put it in the skill. If it's a
[00:30:42] million times over on the internet,
[00:30:43] don't put it in a skill. Focus on the
[00:30:46] things that are proprietary, novel,
[00:30:48] surprising, right?
[00:30:50] Secondly, you want your information,
[00:30:52] your skill to be written in a kind of
[00:30:53] collegial form. Uh often when people
[00:30:56] encounter skills for the first time,
[00:30:57] they think it was like I'm going to I'm
[00:30:59] going to script the LLM and be very
[00:31:01] didactic and pedagogical and write a lot
[00:31:03] of text and this do this and not that.
[00:31:06] But LLMs again, they're pretty smart and
[00:31:08] tokens are precious. So you want to
[00:31:11] actually write them like it doesn't need
[00:31:13] to be that elaborate. Like the same way
[00:31:15] you would talk to a colleague. Hey, when
[00:31:17] you're lighting the sun or when you're
[00:31:18] doing outdoor lighting, set the sun
[00:31:20] before the sky and then maybe look at
[00:31:22] the clouds, right? Literally, that's the
[00:31:23] kind of text that works well in skills.
[00:31:27] Um you want skills to be durable and so
[00:31:30] another gotcha is that you want to be
[00:31:32] careful about embedding things like
[00:31:34] names of properties or names of
[00:31:36] functions that could easily change out
[00:31:38] from underneath the skill. And because
[00:31:40] skills are at the end of the day pure
[00:31:41] text, it's hard to programmatically
[00:31:43] verify things like oh, I renamed this
[00:31:45] property but I didn't update the skill
[00:31:48] and now the skill is kind of a lie.
[00:31:50] Um so again, in being novel and
[00:31:53] collegial actually helps you avoid
[00:31:55] writing things uh that are that
[00:31:57] specific.
[00:31:58] And then finally, uh you want to be
[00:31:59] parsimonious, right? Context is
[00:32:02] precious. Every token counts. So take
[00:32:05] the time to like write a shorter letter
[00:32:07] and really focus on those previous best
[00:32:09] practices which will result in like just
[00:32:11] the information you need and no more.
[00:32:15] Finally, I will talk briefly about
[00:32:16] examples. We had lots of good
[00:32:18] demonstration of that earlier. So the
[00:32:20] thing I'll touch on here is how do you
[00:32:22] find examples or how do you help the LLM
[00:32:24] find them? And there's two models we've
[00:32:26] seen work well. One are what we call
[00:32:28] static examples and these are like
[00:32:29] templates where you decide up front,
[00:32:31] hey, for effects, you know, it maybe
[00:32:34] it's like an explosion, maybe it's like
[00:32:35] a spell, maybe it's like a tracer, and
[00:32:38] you decide, "Great, there's you know
[00:32:39] these are my effects, these are my
[00:32:41] templates, go for it." But that works
[00:32:43] well in some domains, but there are
[00:32:45] other domains that like say gameplay
[00:32:47] programming where the best example for a
[00:32:50] weapon might be different than a
[00:32:51] power-up and might be different than an
[00:32:53] NPC, even though they're kind of all
[00:32:55] blueprints. And so you in those cases
[00:32:58] dynamic examples work really well, where
[00:33:01] essentially you want to make sure that
[00:33:02] your tool set is able to you know
[00:33:04] inspect and read your assets. And then
[00:33:06] the skill will tell the LLM, "Hey,
[00:33:08] actually, you know, if you're doing
[00:33:09] this, go find an example and read it.
[00:33:12] And maybe here's the rules for what good
[00:33:14] examples look like or where you might
[00:33:16] find them." Again, it's the way you
[00:33:17] would talk to a new colleague, and the
[00:33:19] dynamic example discovery helps the LLM
[00:33:22] work in more complex and kind of
[00:33:24] fungible domains.
[00:33:26] So hopefully that gave you an
[00:33:27] understanding of how we extend tool
[00:33:29] sets, skills, and examples. And to bring
[00:33:32] us home, I'm going to hand it back to
[00:33:33] JS.
[00:33:36] >> [applause]
[00:33:40] >> All right. In conclusion, uh let's wrap
[00:33:43] this up.
[00:33:44] Here are some of our of our key
[00:33:46] takeaways.
[00:33:47] The LLM and ThickenSide Unreal, such as
[00:33:50] PCG,
[00:33:51] can be used in ways that are really
[00:33:53] complementary.
[00:33:54] They can truly be friends after all.
[00:33:58] We're already seeing benefits in our own
[00:34:00] internal productions, but this is still
[00:34:03] experimental. Interaction, reliability,
[00:34:06] speed, cost, there's a lot of work still
[00:34:09] to go.
[00:34:11] And you can follow the work on GitHub.
[00:34:13] Uh it's quite like self-contained, so
[00:34:16] you can expect to be able to integrate
[00:34:18] in your projects or cherry-pick,
[00:34:20] whatever you want.
[00:34:22] We also generally like to think that if
[00:34:24] it's useful for users,
[00:34:26] it will be for LLMs.
[00:34:29] And vice versa.
[00:34:31] With or without using LLMs in the end,
[00:34:34] features get developed and improved for
[00:34:37] use cases.
[00:34:39] As example for 5.8 in this well-building
[00:34:42] exploration context, we worked on the
[00:34:45] primitive library,
[00:34:47] manual edits,
[00:34:49] performance, and stability across the
[00:34:51] board. So, these are all crucial for all
[00:34:53] Unreal Engine users uh and PCG users.
[00:34:57] If you recall, our vision was to build
[00:34:59] an extensible system that was
[00:35:03] uh characterable
[00:35:04] and that would produce editable output
[00:35:07] just like everything else in Unreal.
[00:35:09] And we're exactly here today.
[00:35:11] The LLM assists you,
[00:35:13] but true art skills are required to make
[00:35:15] the most out of it.
[00:35:17] But once you do,
[00:35:18] you can start iterating faster.
[00:35:22] This is what is actually available for
[00:35:24] you. The MCP server, tool sets, and
[00:35:26] skills that we've talked about,
[00:35:27] including uh example implementation of
[00:35:29] the semantic search.
[00:35:32] The PCG primitives plugin with all of
[00:35:34] its special operations, examples, and
[00:35:37] the instant fire-and-forget function
[00:35:38] calls.
[00:35:40] Unreal Engine skills for cloud code
[00:35:42] plugin.
[00:35:43] And we're planning on releasing the city
[00:35:46] sample PCG plugin as a
[00:35:48] later this year. Uh we're targeting end
[00:35:50] of summer.
[00:35:51] Uh so you can load and explore
[00:35:53] everything. It might contain a few more
[00:35:55] primitives in that exact city that we've
[00:35:58] showed today.
[00:36:00] To get going, you can use and uh scan
[00:36:03] this QR code. Uh it should get you to
[00:36:05] the official documentation where there's
[00:36:06] more detailed guidelines. But you can
[00:36:08] also search for MCP in Unreal Editor on
[00:36:11] our official docs page.
[00:36:15] But before we open the discussion in
[00:36:17] this Q&A session, I would like to say a
[00:36:19] very big thank you to everyone who's
[00:36:21] working on this with us. And thank you
[00:36:23] for coming to this talk.
[00:36:26] >> [applause]
[00:36:27] >> Woo!
